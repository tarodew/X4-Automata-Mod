#!/usr/bin/env python3
"""Check and package the Automata extension without starting X4."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import md5, sha256
import json
from pathlib import Path, PurePosixPath
import re
from shutil import which
import subprocess
import sys
import tempfile
from zipfile import BadZipFile, ZipFile, ZipInfo

from lxml import etree

EXTENSION_ID = "nyto_automata"
PACKAGE_ROOT = "Automata"
SCHEMA_NS = {"xs": "http://www.w3.org/2001/XMLSchema"}
SYMBOL = re.compile(r"^md\.(Nyto_Automata_\w+)\.(\w+(?:\.\w+)*)$")
LOCAL_TEXT = re.compile(r"\{985700,(\d+)\}")
LITERAL_ORDER = re.compile(r"^'([\w.]+)'$")
LITERAL_MACRO = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*_macro\b")
LITERAL_WARE = re.compile(r"\bware\.([A-Za-z][A-Za-z0-9_]*)\b")
REFERENCE_INDEXES = ("index/macros.xml", "libraries/wares.xml")
FABRICATION = re.compile(r"(?:^|\.)buildmodule_\w*(?:ships_|shipbuilding|shipfab|wharf|shipyard)", re.I)


def parse_xml(data: bytes):
    return etree.fromstring(data, parser=etree.XMLParser(resolve_entities=False, no_network=True))


class Report:
    def __init__(self):
        self.results: list[dict] = []

    def add(self, name: str, ok: bool | None, detail: str = ""):
        self.results.append(
            {"check": name, "status": {True: "pass", False: "fail", None: "skipped"}[ok], "detail": detail}
        )

    @property
    def failed(self):
        return any(result["status"] == "fail" for result in self.results)


def scan_source(source: Path, report: Report):
    files = {}
    roots = {}
    for path in sorted(source.rglob("*")):
        name = path.relative_to(source).as_posix()
        if path.is_symlink():
            report.add("package member", False, f"symlink: {name}")
            continue
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in PurePosixPath(name).parts):
            report.add("package member", False, f"hidden file: {name}")
            continue
        if path.suffix not in {".xml", ".json", ".md"}:
            report.add("package member", False, f"unreviewed file type: {name}")
            continue
        data = path.read_bytes()
        try:
            data.decode("utf-8")
            files[name] = data
            if path.suffix == ".xml":
                roots[name] = parse_xml(data)
                report.add("XML", True, name)
            elif path.suffix == ".json":
                json.loads(data)
                report.add("JSON", True, name)
        except (ValueError, etree.XMLSyntaxError) as exc:
            report.add("parse source", False, f"{name}: {exc}")
    folded = [name.casefold() for name in files]
    report.add("case-insensitive member names", len(folded) == len(set(folded)), f"{len(files)} files")
    return files, roots


def check_source(files, roots, report: Report):
    manifest = roots.get("content.xml")
    dependency = None if manifest is None else manifest.find("dependency[@id='ego_dlc_terran']")
    report.add(
        "extension and Terran dependency",
        manifest is not None
        and manifest.tag == "content"
        and manifest.get("id") == EXTENSION_ID
        and manifest.find("dependency[@version='900']") is not None
        and dependency is not None
        and dependency.get("optional") == "false",
    )
    scripts = {}
    for path, root in roots.items():
        if not path.startswith("md/"):
            continue
        name = root.get("name", "")
        if root.tag != "mdscript" or not name or name in scripts:
            report.add("unique MD script name", False, f"{path}: {name}")
        scripts[name] = root
        names = [node.get("name") for node in root.xpath(".//cue | .//library")]
        report.add("unique MD cue and library names", None not in names and len(names) == len(set(names)), path)

    calls = 0
    unresolved = []
    for script_name, root in scripts.items():
        for node in root.iter():
            if not isinstance(node.tag, str):
                continue
            fields = ("ref",) if node.tag == "run_actions" else ("cue",)
            for field in fields:
                value = node.get(field, "")
                if not value:
                    continue
                target = SYMBOL.fullmatch(value)
                if target:
                    namespace, qualified_name = target.groups()
                elif node.tag == "run_actions" and re.fullmatch(r"\w+", value):
                    namespace, qualified_name = script_name, value
                else:
                    continue
                calls += 1
                target_root = scripts.get(namespace)
                location = f"{script_name}:{node.sourceline} {value}"
                target_nodes = [] if target_root is None else [target_root]
                for name in qualified_name.split("."):
                    target_nodes = [
                        candidate for parent in target_nodes
                        for candidate in parent.xpath("cues/cue[@name=$name] | cues/library[@name=$name]", name=name)
                    ]
                if len(target_nodes) != 1:
                    unresolved.append(location)
                    continue
                if node.tag != "run_actions":
                    continue
                library = target_nodes[0]
                if library.tag != "library" or library.get("purpose") != "run_actions":
                    unresolved.append(f"{location}: target is not a run_actions library")
                    continue
                provided = node.xpath("param/@name")
                expected = set(library.xpath("params/param/@name"))
                required = set(library.xpath("params/param[not(@default)]/@name"))
                if not required <= set(provided) <= expected or len(provided) != len(set(provided)):
                    unresolved.append(f"{location}: invalid arguments {provided}")
    report.add("internal MD references", not unresolved, ", ".join(unresolved) or f"{calls} references")

    texts = roots.get("t/0001-l044.xml")
    text_ids = [] if texts is None else texts.xpath("page[@id='985700']/t/@id")
    refs = set().union(*(set(LOCAL_TEXT.findall(data.decode("utf-8"))) for data in files.values()))
    report.add("YoRHa text references", len(text_ids) == len(set(text_ids)) and refs <= set(text_ids),
               ", ".join(sorted(refs - set(text_ids))) or f"{len(refs)} used IDs")

    ship_creations = [(name, node.get("macro")) for name, root in scripts.items() for node in root.iter("create_ship")]
    report.add(
        "sole direct ship creation is the founding Kyushu",
        ship_creations == [("Nyto_Automata_State", "macro.ship_ter_xl_builder_01_a_macro")],
        str(ship_creations),
    )
    station_creations = [(name, node) for name, root in scripts.items() for node in root.iter("create_station")]
    territory = scripts.get("Nyto_Automata_Territory")
    report.add(
        "native station shell and expansion path",
        len(station_creations) == 1
        and station_creations[0][0] == "Nyto_Automata_Territory"
        and station_creations[0][1].get("owner") == "faction.yorha"
        and territory is not None
        and all(territory.find(f".//{tag}") is not None for tag in (
            "create_construction_sequence", "add_build_to_expand_station"
        )),
    )

    job_root = roots.get("libraries/jobs.xml")
    tickets = [] if job_root is None else job_root.findall(".//job")
    ids = [job.get("id", "") for job in tickets]
    report.add(
        "18 unique requested manufacturing tickets",
        len(ids) == len(set(ids)) == 18 and all(name.startswith("nyto_auto_ticket_") for name in ids),
    )
    bad_tickets = [job.get("id") for job in tickets if any(job.find(path) is None for path in (
        "quota[@galaxy='0']", "modifiers[@rebuild='false']", "environment[@buildatshipyard='true']",
    ))]
    report.add("zero-quota non-rebuilding yard-only tickets", bool(tickets) and not bad_tickets, str(bad_tickets))
    default_orders = [
        job.get("id") for job in tickets
        if job.find("orders/order[@order='Wait'][@default='true']") is None
        or job.find("order") is not None
    ]
    report.add("native job default order structure", bool(tickets) and not default_orders, str(default_orders))
    fabricators = [name for name, data in files.items() if name.endswith(".xml") and FABRICATION.search(data.decode())]
    report.add("no YoRHa fabrication module references", not fabricators, ", ".join(fabricators))

    diplomacy = scripts.get("Nyto_Automata_Diplomacy")
    attributes = [] if diplomacy is None else [value for node in diplomacy.iter() for value in node.attrib.values()]
    report.add(
        "diplomacy uses persistent player faction standing",
        any("faction.player.relationto." in value for value in attributes)
        and any("faction.player.hasrelation.kill." in value for value in attributes)
        and not any(re.search(r"player\.ship\.owner|defaultrelationto|faction\.xenon", value) for value in attributes),
    )
    factions = roots.get("libraries/factions.xml")
    report.add(
        "fixed sponsor standing and no extra hard-coded YoRHa relations",
        factions is not None
        and factions.xpath(".//faction[@id='yorha']/relations/relation/@faction") == ["player"]
        and factions.xpath(".//faction[@id='yorha']/relations/relation/@relation") == ["1.0"],
    )
    check_doctrine(files, roots, scripts, report)
    return scripts


def check_doctrine(files, roots, scripts, report: Report):
    try:
        doctrine = json.loads(files["config/doctrine.json"])
        station_contracts = json.loads(files["config/station_contracts.json"])
        policy = doctrine["forces"]
        fleet = scripts["Nyto_Automata_Fleets"]
        actual = {}
        for node in fleet.xpath(".//set_value[starts-with(@name, '$S.$force_templates.$')]"):
            label = node.get("name").split("$")[-1]
            actual[label] = {
                kind: int(count)
                for kind, count in re.findall(r"\$(\w+)\s*=\s*(\d+)", node.get("exact", ""))
            }
        mismatches = [
            name for name, counts in policy.items() if actual.get(name) != counts
        ]
        report.add("MD formation templates match doctrine counts", not mismatches, ", ".join(mismatches))

        catalog = scripts["Nyto_Automata_Catalog"]
        expected_blueprints = station_contracts["blueprints"]
        macros = station_contracts["modules"]
        mismatches = []
        for name, counts in expected_blueprints.items():
            wanted = Counter({macros[key]: count for key, count in counts.items()})
            blueprint = catalog.xpath(".//set_value[@name=$name]/@exact", name=f"$S.$blueprints.${name}")
            if len(blueprint) != 1 or Counter(LITERAL_MACRO.findall(blueprint[0])) != wanted:
                mismatches.append(name)
        report.add("MD station blueprints match station contract", not mismatches, ", ".join(mismatches))

        loadouts = roots["libraries/loadouts.xml"]
        expected_turrets = {
            "turret_ter_l_beam_01_mk1_macro": "l_meson",
            "turret_ter_l_gatling_01_mk1_macro": "l_proton",
            "turret_ter_m_gatling_02_mk1_macro": "m_proton",
        }
        mismatches = []
        for fit in ("osaka", "osaka_travel", "syn", "asgard"):
            nodes = loadouts.xpath("loadout[@id=$id]/macros/turret/@macro", id=f"nyto_auto_loadout_{fit}")
            got = Counter(expected_turrets.get(macro, macro) for macro in nodes)
            if got != Counter(doctrine["turrets"][fit.removesuffix("_travel")]):
                mismatches.append(fit)
        report.add("fixed capital turret counts match doctrine", not mismatches, ", ".join(mismatches))
    except (KeyError, TypeError, ValueError) as exc:
        report.add("doctrine and blueprint contracts", False, str(exc))


def load_catalogue(path: Path):
    selected = {}
    with ZipFile(path) as archive:
        names = sorted(name for name in archive.namelist() if re.fullmatch(r"\d{2}\.cat", name))
        if not names:
            raise ValueError("no numbered base catalogues in supplied archive")
        for name in names:
            for line in archive.read(name).decode("utf-8-sig").splitlines():
                match = re.fullmatch(r"(.*) (\d+) \d+ ([a-fA-F0-9]{32})", line)
                if match:
                    member, size, digest = match.groups()
                    selected[member.lower()] = (int(size), digest.lower())
    return selected


def reference_entries(archive: ZipFile):
    return {name.replace("\\", "/").lower(): name for name in archive.namelist()}


def check_game_data(roots, scripts, args, report: Report):
    if not args.catalogue:
        report.add("catalogue-verified game data", None, "provide --catalogue and --base-reference")
        return

    selected = load_catalogue(args.catalogue)
    verified = {}
    with ZipFile(args.base_reference) as base:
        for normalized, original in reference_entries(base).items():
            record = selected.get(normalized)
            if record is None or record[0] != base.getinfo(original).file_size:
                continue
            if not (
                normalized.startswith("aiscripts/") or normalized in roots
                or normalized.endswith(".xsd") or normalized in REFERENCE_INDEXES
            ):
                continue
            data = base.read(original)
            if md5(data).hexdigest() == record[1]:
                verified[normalized] = data

    check_orders(scripts, verified, report)
    check_md_surface(scripts, verified, report)
    terran = {}
    if args.terran_reference:
        with ZipFile(args.terran_reference) as archive:
            entries = reference_entries(archive)
            terran = {
                path: archive.read(entries[key])
                for path in (*roots, *REFERENCE_INDEXES)
                if (key := f"ego_dlc_terran/{path.lower()}") in entries
            }
            check_capital_mounts(roots, archive, entries, report)
    library_fixtures = check_diff_targets(roots, verified, terran, report)
    check_literal_references(roots, verified, terran, report)
    if args.xsd_timeout:
        check_xsd(scripts, roots, library_fixtures, verified, args.xsd_timeout, report)
    else:
        report.add("full MD XSD", None, "optional bounded compile: --xsd-timeout SECONDS")


def check_capital_mounts(roots, archive, entries, report: Report):
    loadouts = roots.get("libraries/loadouts.xml")
    if loadouts is None:
        report.add("historical Terran capital mounts", False, "loadouts library missing")
        return
    component_paths = {
        "osaka": "size_l/ship_ter_l_destroyer_01",
        "osaka_travel": "size_l/ship_ter_l_destroyer_01",
        "syn": "size_l/ship_atf_l_destroyer_01",
        "asgard": "size_xl/ship_atf_xl_battleship_01",
        "tokyo": "size_xl/ship_ter_xl_carrier_01",
        "honshu": "size_xl/ship_ter_xl_resupplier_01",
    }
    for fit, path in component_paths.items():
        original = entries.get(f"ego_dlc_terran/assets/units/{path}.xml")
        if original is None:
            report.add("historical Terran capital mounts", None, f"{fit}: fixture unavailable")
            continue
        component = parse_xml(archive.read(original))
        mounts = {node.get("name"): node for node in component.xpath(".//connection[@name]")}
        turrets = {name for name, node in mounts.items() if "turret" in node.get("tags", "").split()}
        planned = loadouts.xpath("loadout[@id=$id]/macros/*", id=f"nyto_auto_loadout_{fit}")
        if fit in {"tokyo", "honshu"} and not planned:
            medium = {name for name in turrets if "medium" in mounts[name].get("tags", "").split()}
            expected = {"tokyo": 28, "honshu": 14}[fit]
            report.add("historical Terran support hull turret count", len(medium) == expected,
                       f"{fit}: {len(medium)} medium mounts; native loadout delivery untested")
            continue
        configured_turrets = {}
        errors = []
        for node in planned:
            mount = node.get("path", "").removeprefix("../")
            reference = mounts.get(mount)
            if reference is None or node.tag not in reference.get("tags", "").split():
                errors.append(f"{node.tag}: {mount}")
                continue
            if node.tag == "turret":
                size = "medium" if "_m_" in node.get("macro", "") else "large"
                if size not in reference.get("tags", "").split() or mount in configured_turrets:
                    errors.append(f"{size} turret: {mount}")
                configured_turrets[mount] = node.get("macro")
        for mount in turrets ^ configured_turrets.keys():
            errors.append(f"unmatched turret: {mount}")
        for mount, macro in configured_turrets.items():
            if "_l_" not in macro:
                continue
            position = mounts[mount].find("offset/position")
            if position is None:
                errors.append(f"no offset: {mount}")
                continue
            use_meson = float(position.get("y" if fit.startswith("osaka") else "z", "0")) < 0
            if use_meson != ("_beam_" in macro):
                errors.append(f"Meson placement: {mount}")
        report.add("historical Terran capital mounts", bool(planned) and not errors,
                   f"{fit}: {', '.join(sorted(errors)) or f'{len(configured_turrets)} turret paths'}")


def check_literal_references(roots, verified, terran, report: Report):
    definitions = {
        "index/macros.xml": ("macro", ".//entry/@name", LITERAL_MACRO),
        "libraries/wares.xml": ("ware", ".//ware/@id", LITERAL_WARE),
    }
    for index, (kind, selector, pattern) in definitions.items():
        if index not in verified:
            report.add(f"literal {kind} references", None, f"missing catalogue-verified {index}")
            continue
        base_names = set(parse_xml(verified[index]).xpath(selector))
        terran_names = set(parse_xml(terran[index]).xpath(selector)) if index in terran else set()
        uses = {}
        for path, root in roots.items():
            for element in root.iter():
                for attribute, value in element.attrib.items():
                    names = pattern.findall(value)
                    if kind == "ware" and attribute in {"ware", "wareid"} and re.fullmatch(r"[A-Za-z]\w*", value):
                        names.append(value)
                    for name in names:
                        uses.setdefault(name, f"{path}:{element.sourceline}")
        unresolved = uses.keys() - base_names - terran_names
        if index not in terran:
            report.add(f"literal {kind} references", None,
                       f"{len(uses.keys() & base_names)} base references, Terran index unavailable")
            continue
        detail = ", ".join(f"{name} at {uses[name]}" for name in sorted(unresolved))
        if not detail:
            detail = (
                f"{len(uses.keys() & base_names)} catalogue-verified base, "
                f"{len(uses.keys() - base_names)} historical Terran index references"
            )
        report.add(f"literal {kind} references", not unresolved, detail)


def check_orders(scripts, verified, report: Report):
    native = {}
    for name, data in verified.items():
        if not name.startswith("aiscripts/") or not name.endswith(".xml"):
            continue
        root = parse_xml(data)
        for order in root.findall("order"):
            native[order.get("id")] = (
                set(order.xpath("params/param/@name")),
                set(order.xpath("params/param[@required='true']/@name")),
            )
    for script_name, root in scripts.items():
        for node in root.iter("create_order"):
            detail = f"{script_name}:{node.sourceline} {node.get('id')}"
            order = LITERAL_ORDER.fullmatch(node.get("id", ""))
            if order is None:
                report.add("native order", None, f"{detail} (dynamic ID)")
                continue
            expected = native.get(order[1])
            if expected is None:
                report.add("native order", None, f"{detail} (no catalogue-verified base definition)")
                continue
            provided = node.xpath("param/@name")
            known, required = expected
            unexpected = set(provided) - known
            missing = required - set(provided)
            duplicates = [name for name, count in Counter(provided).items() if count > 1]
            report.add(
                "native order parameter names",
                not (unexpected or missing or duplicates),
                f"{detail} unknown={sorted(unexpected)} missing={sorted(missing)} duplicate={sorted(duplicates)}",
            )


def check_md_surface(scripts, verified, report: Report):
    paths = ["libraries/md.xsd", "libraries/common.xsd"]
    if any(path not in verified for path in paths):
        report.add("MD action and condition names", None, "missing catalogue-verified schema sources")
        return
    schemas = [parse_xml(verified[path]) for path in paths]
    names = set().union(*(set(schema.xpath("//xs:element/@name", namespaces=SCHEMA_NS)) for schema in schemas))
    groups = {
        group.get("name"): group
        for schema in schemas for group in schema.xpath("xs:attributeGroup[@name]", namespaces=SCHEMA_NS)
    }
    types = {
        declaration.get("name"): declaration
        for schema in schemas for declaration in schema.xpath("xs:complexType[@name]", namespaces=SCHEMA_NS)
    }

    def attributes(declaration):
        named_type = declaration.get("type")
        if named_type:
            return attributes(types[named_type]) if named_type in types else None
        scopes = [declaration]
        for prefix in ("", "xs:complexType/"):
            scopes.extend(declaration.xpath(
                prefix + "xs:complexContent/xs:extension | " + prefix + "xs:simpleContent/xs:extension",
                namespaces=SCHEMA_NS,
            ))
        scopes.extend(declaration.xpath("xs:complexType", namespaces=SCHEMA_NS))
        allowed, required = set(), set()
        for scope in scopes:
            if scope.find("xs:anyAttribute", namespaces=SCHEMA_NS) is not None:
                return None
            for attribute in scope.findall("xs:attribute", namespaces=SCHEMA_NS):
                name = attribute.get("name")
                if name is None:
                    return None
                allowed.add(name)
                if attribute.get("use") == "required":
                    required.add(name)
            bases = list(scope.xpath("xs:attributeGroup/@ref", namespaces=SCHEMA_NS))
            for base in bases:
                if base not in groups:
                    return None
                signature = attributes(groups[base])
                if signature is None:
                    return None
                allowed.update(signature[0])
                required.update(signature[1])
            parent = scope.get("base")
            if parent in types:
                signature = attributes(types[parent])
                if signature is None:
                    return None
                allowed.update(signature[0])
                required.update(signature[1])
        return allowed, required

    # Compare direct uses of actions/conditions. Their nested records have distinct
    # declarations, and a global lookup can silently select the wrong one.
    groups_by_section = {
        "actions": {"specificactions", "commonactions"},
        "conditions": {
            "specificconditions_event", "specificconditions_nonevent",
            "commonconditions_event", "commonconditions_nonevent",
        },
    }
    declarations = {section: {} for section in groups_by_section}
    for section, group_names in groups_by_section.items():
        for schema in schemas:
            for group in schema.xpath("xs:group[@name]", namespaces=SCHEMA_NS):
                if group.get("name") not in group_names:
                    continue
                for declaration in group.xpath("xs:choice/xs:element[@name]", namespaces=SCHEMA_NS):
                    signature = attributes(declaration)
                    if signature is not None:
                        declarations[section].setdefault(declaration.get("name"), []).append(signature)

    for script_name, root in scripts.items():
        tags = set()
        unexpected = []
        for section in root.xpath(".//actions | .//conditions"):
            for node in section.iterdescendants():
                if not isinstance(node.tag, str):
                    continue
                tags.add(node.tag)
                if node.getparent().tag not in (section.tag, "do_if", "do_elseif", "do_else", "do_all", "do_while"):
                    continue
                signatures = declarations[section.tag].get(node.tag, [])
                provided = set(node.attrib)
                if signatures and not any(required <= provided <= allowed for allowed, required in signatures):
                    details = [
                        f"unknown={sorted(provided - allowed)} required={sorted(required - provided)}"
                        for allowed, required in signatures
                    ]
                    unexpected.append(f"{node.sourceline} {node.tag}: {' or '.join(details)}")
        missing = tags - names
        report.add("MD action and condition names", not missing, f"{script_name} {sorted(missing)}")
        report.add("MD action and condition attribute surface", not unexpected,
                   f"{script_name} {', '.join(unexpected)}".rstrip())


def resolve_selector(document, selector):
    if not selector:
        raise ValueError("missing selector")
    result = document.xpath(selector)
    if not isinstance(result, list):
        raise ValueError("selector does not return nodes")
    return result


def check_diff_targets(roots, verified, terran, report: Report):
    # Base bytes are verified by catalogue. Terran XML here is only a fixture for selector
    # resolution, since the input reference lacks the equivalent Terran catalogue.
    fixtures = {}
    for path, root in roots.items():
        if root.tag != "diff":
            continue
        data = verified.get(path.lower())
        if data is None:
            report.add("XML patch selectors", None, f"{path}: missing catalogue-verified base")
            continue
        document = parse_xml(data)
        if path in terran:
            apply_terran_additions(document, parse_xml(terran[path]))
        append_only = True
        for node in root:
            if not isinstance(node.tag, str):
                continue
            if node.tag != "add" or node.get("pos") or node.get("type"):
                append_only = False
            selector = node.get("sel")
            try:
                matches = resolve_selector(document, selector)
            except (ValueError, etree.XPathError) as exc:
                report.add("XML patch selector", False, f"{path} {selector}: {exc}")
                continue
            if not matches and path == "libraries/factions.xml" and not terran and "[@id=" in selector:
                report.add("XML patch selector", None, f"{path} {selector}: Terran fixture absent")
            else:
                report.add("XML patch selector", len(matches) == 1, f"{path} {selector}: {len(matches)} match(es)")
        if append_only and (path != "libraries/factions.xml" or path in terran):
            apply_terran_additions(document, root)
            fixtures[path] = document
    report.add("effective DLC order and Terran hashes", None,
               "Terran additions are a fixture. Full extension load order is not simulated.")
    return fixtures


def apply_terran_additions(document, patch):
    # These are the simple append operations relevant to Automata's fixture.
    # Unrelated replacement, removal, and attribute selectors are left to the engine.
    if patch.tag != "diff":
        return
    for node in patch.findall("add"):
        if node.get("pos") or node.get("type"):
            continue
        for target in resolve_selector(document, node.get("sel")):
            if not isinstance(target, etree._Element):
                continue
            for child in node:
                if isinstance(child.tag, str):
                    target.append(deepcopy(child))


def check_xsd(scripts, roots, fixtures, verified, timeout: int, report: Report):
    groups = {
        "full MD XSD": (
            "md/md.xsd", {f"{name}.xml": root for name, root in scripts.items()}
        ),
        "authored diff XSD": (
            "libraries/diff.xsd", {path: root for path, root in roots.items() if root.tag == "diff"}
        ),
        "merged game library fixture XSD": (
            "libraries/libraries.xsd", {
                path: fixtures[path] for path in (
                    "libraries/characters.xml", "libraries/god.xml", "libraries/jobs.xml"
                ) if path in fixtures
            }
        ),
        "merged faction fixture XSD": (
            "libraries/factions.xsd", {path: fixtures[path] for path in ("libraries/factions.xml",) if path in fixtures}
        ),
    }
    report.add("content, localisation, construction-plan and loadout XSD", None,
               "no matching standalone schemas in provided sources; structural and focused checks apply")
    for name, (schema, documents) in groups.items():
        if not documents:
            report.add(name, None, "no compatible input documents")
            continue
        paths = [schema]
        if name != "authored diff XSD":
            paths.append("libraries/common.xsd")
        if name == "full MD XSD":
            paths.append("libraries/md.xsd")
        run_xsd(name, documents, paths, verified, timeout, report)


def run_xsd(name, documents, paths, verified, timeout: int, report: Report):
    if not set(paths) <= set(verified):
        report.add(name, None, "missing catalogue-verified schema dependencies")
        return
    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        for schema_path in paths:
            path = work / schema_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(verified[schema_path])
        for original, root in documents.items():
            (work / Path(original).name).write_bytes(etree.tostring(root))
        validator = """
from pathlib import Path
import sys
from lxml import etree
schema = etree.XMLSchema(etree.parse(sys.argv[1]))
valid = True
for file in sorted(Path('.').glob('*.xml')):
    tree = etree.parse(str(file), parser=etree.XMLParser(resolve_entities=False, no_network=True))
    if not schema.validate(tree):
        print(file, schema.error_log, sep=': ')
        valid = False
raise SystemExit(0 if valid else 1)
"""
        java = which("java")
        commands = []
        if java:
            java_source = """
import java.io.File;
import javax.xml.XMLConstants;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.SchemaFactory;
import org.xml.sax.SAXException;

class ValidateMd {
    public static void main(String[] args) throws Exception {
        var factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
        factory.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        factory.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "file");
        var schema = factory.newSchema(new File(args[0]));
        var valid = true;
        for (int i = 1; i < args.length; ++i) {
            try {
                schema.newValidator().validate(new StreamSource(new File(args[i])));
            } catch (SAXException error) {
                System.err.println(args[i] + ": " + error.getMessage());
                valid = false;
            }
        }
        System.exit(valid ? 0 : 1);
    }
}
"""
            java_path = work / "ValidateMd.java"
            java_path.write_text(java_source, encoding="utf-8")
            command = [java, java_path.name, paths[0], *sorted(path.name for path in work.glob("*.xml"))]
            commands.append(("Java JAXP", command))
        commands.append(("lxml", [sys.executable, "-c", validator, paths[0]]))
        for backend, command in commands:
            try:
                result = subprocess.run(
                    command,
                    cwd=work,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                report.add(name, None, f"{backend} compile/validation exceeded {timeout}s")
                return
            if backend == "Java JAXP" and (
                "Could not find or load main class" in result.stderr
                or "Source option" in result.stderr
                or "java.compiler" in result.stderr
            ):
                continue
            break
        detail = result.stdout.strip() or result.stderr.strip()
        report.add(name, result.returncode == 0, detail or f"{backend}, {len(documents)} documents")


def make_package(files, destination: Path):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as temporary:
        temp_path = Path(temporary.name)
    try:
        with ZipFile(temp_path, "w") as archive:
            for name, data in sorted(files.items()):
                member = ZipInfo(f"{PACKAGE_ROOT}/{name}", (1980, 1, 1, 0, 0, 0))
                member.create_system = 3
                member.external_attr = 0o100644 << 16
                archive.writestr(member, data)
        with ZipFile(temp_path) as archive:
            if archive.testzip() is not None or {
                name.removeprefix(f"{PACKAGE_ROOT}/"): archive.read(name) for name in archive.namelist()
            } != files:
                raise ValueError("package read-back differs from source")
        temp_path.replace(destination)
    finally:
        temp_path.unlink(missing_ok=True)
    return sha256(destination.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1] / "Automata")
    parser.add_argument("--catalogue", type=Path)
    parser.add_argument("--base-reference", type=Path)
    parser.add_argument("--terran-reference", type=Path)
    parser.add_argument("--xsd-timeout", type=int, default=0)
    parser.add_argument("--package", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if bool(args.catalogue) != bool(args.base_reference) or (args.terran_reference and not args.catalogue):
        parser.error("--catalogue and --base-reference are required together")
    if args.xsd_timeout < 0 or (args.xsd_timeout and not args.catalogue):
        parser.error("--xsd-timeout requires game inputs and a nonnegative duration")
    if not args.source.is_dir():
        parser.error(f"source directory does not exist: {args.source}")
    for path in (args.report, args.package):
        if path and path.resolve().is_relative_to(args.source.resolve()):
            parser.error("write outputs outside the extension source directory")
    if args.package and args.report and args.package.resolve() == args.report.resolve():
        parser.error("package and report must be different files")

    report = Report()
    files, roots = scan_source(args.source, report)
    scripts = check_source(files, roots, report)
    try:
        check_game_data(roots, scripts, args, report)
    except (BadZipFile, OSError, ValueError, etree.LxmlError) as exc:
        report.add("game data input", False, str(exc))
    report.add("X4 runtime, expression execution and save/reload", None, "X4 was not started")
    package = None
    if args.package and not report.failed:
        package = {"path": str(args.package), "sha256": make_package(files, args.package), "files": len(files)}
        report.add("archive integrity and exact member bytes", True, package["sha256"])
    counts = dict(Counter(result["status"] for result in report.results))
    evidence = {
        "counts": counts,
        "source_manifest": {name: sha256(data).hexdigest() for name, data in files.items()},
        "package": package,
        "results": report.results,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    for result in report.results:
        if result["status"] != "pass":
            print(f"{result['status'].upper()} {result['check']}: {result['detail']}")
    print(json.dumps(counts, sort_keys=True))
    if package:
        print(f"{package['sha256']}  {package['path']}")
    return int(report.failed)


if __name__ == "__main__":
    raise SystemExit(main())
