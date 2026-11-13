# Roadmap to V9.0.0A1.0

The first integrated candidate should let YoRHa establish itself, build stations, buy and assign ships, defend holdings, organize clusters, manage fleets, mirror player diplomacy and expand under the documented rules. The candidate is intended for a controlled in-game test.

| Stage | Scope | Evidence at migration |
| --- | --- | --- |
| A0.1 Foundation | Identity, Earth Bunker, founding Kyushu, persistent registries | Historical static pass |
| A0.2 Territory bootstrap | Resource-backed Administration Base, Builder reservation, concurrent infrastructure registration | Historical static pass |
| A0.3 Cluster Core and High Command | Topology scoring, ideal/usable Core, same-station promotion | Historical static pass and recovered source |
| A0.4 Economy and procurement | Paid player-yard orders, continuity Builder, real industry, mining/trade and diplomacy | Durable checkpoint and bounded static pass recorded |
| A0.5 Security and readiness | Nimcha reserves, patrol and police, escort relief, recon, service | Two source archives located. Contents and coverage await audit. |
| A0.6 Military formations | Regional capital response, heavy defence, Rapid Response, regular and Asgard divisions | Design recorded. Audit A0.5 overlap before implementing. |
| A0.7 War and expansion | Extend the A0.4 relation mirror into actual war/peace, target selection, claim and handoff | Design recorded. Integrated behavior remains open. |
| A0.8 Controls and integration | Pause/resume, directives, diagnostics, state reconciliation and basic status view | Earlier control work is reported. Verify the imported source and close remaining gaps. |
| A1.0 Test candidate | Integrated source, reproducible package, offline report and controlled runtime checklist | No verified package located during migration. |

## Immediate sequence

1. Inspect both A0.5 archives. Hash them and compare against the durable A0.4 source. Inventory the extension and its assets, then import the applicable mod-authored source. Record archive-to-commit provenance and any omitted files.
2. Reproduce structural and version-matched checks from [Testing](TESTING.md). Verify the actual behavior represented in source. Use one small regression check for each resolved invariant that can be exercised offline.
3. Close security, fleet, strategic, expansion and control gaps based on the audit. Preserve the defaults and state schema across checkpoints. Keep production of ships and infrastructure resource-backed.
4. Build a reproducible A1.0 candidate. Record its commit, artifact hash, exact X4/DLC version, offline results and remaining engine-only assertions.
5. Run the first disposable-save session when authorized. Use the acceptance order in [Testing](TESTING.md).

## Later work

Final player-authored station geometry, full Operations Board polish, expansion balancing and scale tuning can follow the test candidate. The design keeps regional High Command relocation possible, including a preferred Core currently held by an ally. Completed-station dismantling, correct refunds and relocation require separate proof before activation. Bunker stays on Earth.