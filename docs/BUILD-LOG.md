# Build log and evidence

## September 2026 checkpoints

These results describe the builds identified in the original YoRHa compendium. The GitHub migration records them as historical evidence. A source archive must match its reported hash before it inherits a report.

| Checkpoint | Recorded implementation | Recorded evidence |
| --- | --- | --- |
| A0.1 | Fresh `nyto_automata` extension, Terran dependency, Earth Bunker, founding Kyushu and persistent schema 2. Operational AI disabled. | Bounded checks covered 22 package files, XML, supported MD actions, selectors, localisation, asset dimensions and the 18-entry Bunker plan. Early diplomacy values are superseded. |
| A0.2 | Territory request guards, native empty station shell and Admin build queue, real Builder reservation/deployment, 13 concurrent infrastructure registrations. | Static pass. Two construction plans and 25 connection entries checked against source. Industrial execution was still pending at this checkpoint. |
| A0.3 | Cluster membership, ideal and usable Core selection, existing-Admin expansion to High Command, relocation recommendations. | Historical 74-check static pass. A separate reconstructed checkpoint was later recovered and inspected. |
| A0.4 | Persistent player relations, 18 requested-job templates, paid player-yard procurement, Builder continuity, trader/miner allocation and retained construction/High Command logic. Operational planners default paused. | 1,372 bounded checks passed, zero failed, in 0.277 s. Archive contains 24 extension files and a source manifest. |
| A0.5 | Progress reports mention security, fleet templates, Builder escort relief, servicing and Rapier reconnaissance. | Both September archives are recovered. The later archive has a 52-check historical report and passed a new structural audit. See the recovery entry below. |
| A1.0 | First integrated test candidate. | No verified package located. |

### Known source identities

| Artifact described in original build log | SHA-256 |
| --- | --- |
| A0.3 recovered construction/core source used for A0.4 | `c439d938bba159649fab6efe31df93f60570ec01e9c980d67219358d6fb2263e` |
| A0.4 September 12 verified-source checkpoint | `27f677fb32be339d9408f7704e6280361796a425fc6fcb4bc669fe0b645c939c` |
| A0.5 September 12 security source | `ead5a840a488906e1bf2b146c9687789b3cf374cfbe5a0d80c9d4ef8c0ebce1e` |
| A0.5 September 13 verified source | `1e1eea0353d27eebbfe2af72124001179cbaf958cf3c8904d55015958f77e477` |

Multiple archives carry the same A0.x version. The original 74-check report and later recovered A0.3 archive are distinct provenance records. Tie any new result to its exact artifact.

### Source authority

The original audit checked `version.dat` value `900`, numbered base catalogues 01–09 and Terran catalogues ext_01–ext_03. It selected the latest numbered entry per path and accepted older extracted bytes only when length and catalogue MD5 matched. The broader harvest verified 5,077 base and 401 Terran text files, with 1,477 base and 251 Terran text payloads still unmaterialized. A narrower reconstruction verified 1,113 base and 401 Terran text files. Other DLC patch effects remained outside the certified scope. Apply current extension diffs in their effective order before validating selectors and merged references.

The earlier Envoy Pack reference extracts and v1.14/RC3 and v1.15 prototypes are historical references. The current implementation uses the clean 9.0 line. Retired approaches include the old staged station identity, old fixed 20-station Core limit, broad player-space FactionLogic mutation, legacy construction probes and standing fleet Jobs quotas.

### A0.4 implementation details

The build log records native `Job_Helper` / `build.shiptrader` use, yard `buildbuyprices`, `add_build_to_construct_ship` and `requested_ship_built` reconciliation. It records the correction of the food ware to `terranmre`, separate from the `prod_ter_mre_macro` production module. It also records replacing an unsupported `isconnected` check with documented waiting-job-ship and sector checks and resetting assignment flags on delivery.

The 1,372 checks covered XML, MD actions and attributes, native order parameters, literal macro and ware references, diff selectors and selected rules for procurement and diplomacy. Full upstream MD XSD compilation did not complete within the earlier bounded attempts. Engine expression execution, collision, pathing and gameplay were untested.

## November 12, 2026 migration

- Moved current decisions, the roadmap and historical build evidence into GitHub. The original YoRHa compendium remains the full archival record.
- Located the September 12 and 13 A0.5 archives. The execution workspace was unavailable for extracting and testing the archives. No new offline mod result or source import was completed.
- In-game validation remains pending.

### A0.5 source recovery and build planning

- Recovered A0.4 and both A0.5 archives. All three passed ZIP integrity and path checks, and all 24/28/28 extension-file hashes matched their respective source manifests. The September 12 A0.5 adds four MD scripts for security, fleets, service and reconnaissance. The September 13 archive retains all four and revises core, fleets, security, recon and package metadata.
- Fresh checks on September 13 A0.5 passed for 22 XML files, JSON parsing, script and cue name uniqueness, 42 qualified internal MD action references, and parameter names at 33 native order call sites across 15 order IDs. The order definitions were matched by size and MD5 against the selected numbered base catalogue entries. The bundled 52-check report is earlier evidence and was inspected separately.
- The recovered source includes regular and strategic fleet templates and a report-only conversation menu. World-changing planners start paused. Audit the actual triggers and their cross-system handoffs before enabling them.
- Full effective base/DLC patch application, XSD validation, engine expression evaluation and runtime behaviour remain open. These checks did not launch X4. Gameplay source import is the first implementation step.

## November 12, 2026 A1.0 integration candidate

- Imported all 28 manifest-matched A0.5 extension files as the build branch baseline. Integrated the Mission Director strategy, operator menu, paid yard and Builder reconciliation, station supply, fleet readiness, security, reconnaissance and servicing.
- Added explicit sponsor buildout, lawful claim and security handoff, separate war authorization and expansion policy, and Accelerator-linked Front Gate construction. The Arsenal uses the approved standard project envelope and special fleet staging. Additional Arsenal station plans up to the documented 40-station ceiling are open.
- Kept the persistent player-relation mirror, +30 sponsor relationship, Earth Bunker, 14-Builder ceiling, no YoRHa fabrication, and locked formation and station counts. The delivered capital-fit check measures installed turret families. Nimcha and Jian use provisional Proton loadouts while exact launcher compatibility is open.
- Integrated the full MD XSD and bounded diff/library checks. Base schema and native order files were matched to the numbered catalogue. Available Terran library and component data serve as historical fixtures. The exact effective X4 9.0 DLC patch order and engine expressions remain unverified.
- Exceptional Asgard deployment, additional Arsenal station planning, and final geometry remain open. Provisional thresholds cover force concentration and two physically present Nimcha wings plus police for a claim handoff. They require in-game evidence. A paid order and an assigned Builder crossing save/reload are the first persistence test.

Final offline package evidence for source commit `b8bb85d63b3cfdc44b72005ec4bf995dda31dc21`:

- **145 passed, 0 failed, 3 skipped.** Full Mission Director XSD passed for 15 scripts. Five authored diffs and four materialized library fixtures also passed XSD checks.
- The skipped groups cover exact effective DLC patch order and Terran payload provenance, standalone schemas unavailable for four file types, and X4 engine behaviour.
- Two independent ZIP builds were byte-identical. Package SHA-256 is `fbf62cb020034f27ebb073fe091c21db29640c94216eab379ce91e0a5224f470`.
