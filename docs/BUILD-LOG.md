# Build log and evidence

## September 2026 checkpoints

These results describe the builds identified in the original YoRHa compendium. The GitHub migration records them as historical evidence. A source archive must match its reported hash before it inherits a report.

| Checkpoint | Recorded implementation | Recorded evidence |
| --- | --- | --- |
| A0.1 | Fresh `nyto_automata` extension, Terran dependency, Earth Bunker, founding Kyushu and persistent schema 2. Operational AI disabled. | Bounded checks covered 22 package files, XML, supported MD actions, selectors, localisation, asset dimensions and the 18-entry Bunker plan. Early diplomacy values are superseded. |
| A0.2 | Territory request guards, native empty station shell and Admin build queue, real Builder reservation/deployment, 13 concurrent infrastructure registrations. | Static pass. Two construction plans and 25 connection entries checked against source. Industrial execution was still pending at this checkpoint. |
| A0.3 | Cluster membership, ideal and usable Core selection, existing-Admin expansion to High Command, relocation recommendations. | Historical 74-check static pass. A separate reconstructed checkpoint was later recovered and inspected. |
| A0.4 | Persistent player relations, 18 requested-job templates, paid player-yard procurement, Builder continuity, trader/miner allocation and retained construction/High Command logic. Operational planners default paused. | 1,372 bounded checks passed, zero failed, in 0.277 s. Archive contains 24 extension files and a source manifest. |
| A0.5 | Progress reports mention security, fleet templates, Builder escort relief, servicing and Rapier reconnaissance. | Two source archives located, dated September 12 and 13. Contents, coverage and latest archive hash await inspection. |
| A1.0 | First integrated test candidate. | No verified package located. |

### Known source identities

| Artifact described in original build log | SHA-256 |
| --- | --- |
| A0.3 recovered construction/core source used for A0.4 | `c439d938bba159649fab6efe31df93f60570ec01e9c980d67219358d6fb2263e` |
| A0.4 September 12 verified-source checkpoint | `27f677fb32be339d9408f7704e6280361796a425fc6fcb4bc669fe0b645c939c` |

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