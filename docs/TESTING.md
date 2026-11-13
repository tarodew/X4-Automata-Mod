# Testing X4 Automata with the game closed

Use offline validation for every source change. Group the tests that need the X4 engine into a planned disposable-save session when a bounded or integrated candidate is ready.

## Game files used as test inputs

Use the matching X4 9.0 base files and Terran DLC data when checking schemas, XML patches, equipment mounts and native orders. A fresh extraction is needed only for files missing from the verified source set. Resolve numbered catalogue precedence and relevant DLC diffs for each tested path. Treat older reference extracts as historical until their bytes match the selected current catalogue entry.

The GitHub repository tracks the mod's own code, decisions, and validation evidence. Keep the bulk game files with the external references. See [Build log](BUILD-LOG.md) for the coverage of the existing source harvest.

## Offline acceptance

| Check | What to verify |
| --- | --- |
| Archive and provenance | Compute SHA-256 and compare to the recorded checkpoint. Check ZIP integrity, normalized safe paths, case collisions, manifest entries and the expected extension root. Record input and output hashes. |
| XML structure | Parse each extension XML file. Check unique MD script names across the loaded set and unique cue names within each script. Validate metadata, localisation and the Terran dependency. |
| Version-matched schema | Use the XSDs extracted from the target build, including MD and AI schemas and their imports. Validate complete scripts and materialized XML against the corresponding schema. A schema timeout is a skipped check. |
| Patches and references | Resolve diff targets against the effective base/DLC files in load order. Check the expected target count and the result after applying the patch. Resolve macros, wares, jobs, cue signals, localisation, construction snaps and order parameters against the appropriate source. |
| Behavior that can be tested outside X4 | Use the actual pure decision logic where extractable. Cover sponsor protection, the persistent relation mirror, ideal/usable Core selection, Builder eligibility, one order per deficit, and independent station blockers. State explicitly when a fixture tests a model of MD behavior. |
| Packaging | Rebuild the ZIP twice with fixed file ordering and metadata. Compare hashes and confirm that it contains only the intended extension files. |

### Run the repository checker

From the repository root with Python 3 and `lxml` installed:

```text
python tools/automata_check.py --catalogue /path/to/X4-Catalogue.zip --base-reference /path/to/X4-Supplemental-Reference.zip --terran-reference /path/to/X4-DLC-Reference.zip --report /path/to/validation.json --package /path/to/Automata_V9.0.0A1.0.zip
```

The checker records passes, failures and skips. Use `--xsd-timeout 45` to attempt full MD XSD validation. A bounded timeout leaves the check open. The Terran reference archive in this workflow is a historical fixture. Its selector and mount checks do not establish the effective 9.0 DLC load order. Use the exact target game's data to close that gap.

For an available source ZIP, basic checks can start with Python 3 and PowerShell while X4 stays closed:

```powershell
$checkpoint = "Automata_V9.0.0A0.5_2026-09-13_verified_source.zip"
Get-FileHash -Algorithm SHA256 $checkpoint
py -3 -m zipfile -t $checkpoint
py -3 -m zipfile -l $checkpoint
```

Use the actual archive filename if it differs. The commands above cover the hash, basic archive readability and inventory. XML, schemas, diff application and references are separate checks. Use privately extracted current game data where needed. [Egosoft X Catalog Tool](https://wiki.egosoft.com/X%20Foundations%20Wiki/Modding%20Support/X%20Catalog%20Tool/)

Record every check as passed, failed or skipped. Include the source commit/archive hash, game and DLC builds, checker version and relevant output. See [Build log](BUILD-LOG.md) for the existing A0.4 result and its scope.

## First in-game session

Static success leaves Mission Director import and expression evaluation, engine events and save persistence to be verified. A fresh disposable save and scripting logs make it possible to check several milestones during one controlled session. Use `-debug scripts -logfile debuglog.txt` to collect the engine evidence. [Egosoft Mission Director Guide](https://wiki.egosoft.com/X%20Rebirth%20Wiki/Modding%20support/Mission%20Director%20Guide/)

| Order | Engine checks |
| --- | --- |
| 1. Foundation | Confirm one YoRHa faction, one Earth Bunker and one founding Kyushu. Check sponsor +30, planner pause defaults and reload without duplicate startup effects. |
| 2. Procurement | Exercise an eligible player yard, blueprint/access blockers, real prices, materials and queue, delivery, duplicate prevention on reload, and the zero-Builder continuity exception. |
| 3. Construction | Follow one Admin and one independent infrastructure project through build storage, assignment, ware waits and completion. Verify claim eligibility, one active reservation per Builder, and same-station High Command promotion. |
| 4. Security and service | Verify wing and police assignments, reserve backfill, civilian rescue and restoration, Rapier observation, Builder escort relief, and docking/repair/rearm. |
| 5. Fleet behavior | Test fixed formations, commander loss and succession, carrier and Honshu throughput, understrength reporting, replacement and recovery. |
| 6. Diplomacy and expansion | Verify real standing and peace changes, disguise independence, local incident handling, allied/player protection, claim feasibility and security handoff. |
| 7. Controls and scale | Check map selection and current-sector fallback, pause/resume, sponsor and claim directives, restrictions, blocker reporting, repeated reload, concurrent incidents and increasing sector/fleet scale. |

Capture the initial state, action and expected observation for each scenario. Confirm persistent state before and after reload. A successful offline pass does not change the status of these engine checks.