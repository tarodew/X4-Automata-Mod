# YoRHa design

YoRHa is an autonomous client faction sponsored by the player. The player sets strategic direction. Automata runs routine expansion, construction, economy, security, intelligence and fleet assignments. Terran technology, equipment and native execution patterns provide the foundation. YoRHa has its own strategy, identity and fleet establishments.

## Player relationship and diplomacy

- YoRHa remains at **+30** with the player. Player sectors are sponsor space. YoRHa may build and provide support there under the relevant permissions. It can never claim them.
- YoRHa mirrors the player's **persistent faction standing and formal war/peace state**, including Xenon and Yaki. If the player's real Yaki relationship improves, YoRHa follows it. The earlier permanent Xenon hostility decision is superseded.
- Cloaking, disguise, apparent ship ownership, scan refusal and temporary local aggression have no effect on faction-wide diplomacy. YoRHa can still respond locally to a threat.
- The A0.4 implementation record identifies `faction.player.relationto` and `faction.player.hasrelation.kill` as the source expressions. Whether peace changes safely reconcile existing orders remains an engine test.

## Territory and headquarters

Bunker is the permanent faction headquarters on Earth. Regional High Commands serve individual clusters and leave the Bunker's headquarters identity intact.

| Concept | Decision |
| --- | --- |
| Cluster | Adjacent holdings, with a planning limit of roughly four active sectors. |
| Ideal Core | The strategically best candidate, potentially a sector held by an ally. Record the candidate and preserve allied ownership. |
| Usable Core | A registered, YoRHa-owned sector with operational administration. Use connectivity, travel distances, accessibility and stability to select it. |
| Promotion | The preferred path expands the chosen sector's existing Administration Base into a maintenance-capable High Command. Administration and other infrastructure begin in parallel, subject to each project's own prerequisites. |
| Relocation | Keep future relocation possible if a better sector becomes available. Build and verify the replacement before any transfer of authority. Safe dismantling and refunds remain research. An old High Command can serve as a local support base if dismantling proves impractical. |

Core scoring should reflect the actual gate and accelerator network. Consider route length, access to logistics and industrial capacity, exposure, strategic junctions and future growth. Stability matters once the region has an operating High Command. A0.3 recorded a 250-point hysteresis threshold for pre-HQ provisional selection. That threshold is implementation history and can be tuned from evidence.

## Expansion and war policy

- **Defensive** prioritizes readiness, sponsor protection and regional defence. **Balanced** attacks when ready and completes the handoff before advancing. **Aggressive** permits successive offensives while forces can sustain them.
- Default expansion considers discovered, viable unclaimed sectors within about two safe jumps of contiguous holdings. A player-directed claim overrides the distance preference and still requires safe access, a Builder, feasible administration and supply. Galaxy-Wide expansion is opt-in.
- A formal war operation can clear confirmed enemy military ships and enemy-faction stations. Allied and neutral assets stay protected. Foreign or allied administration that blocks a claim remains a blocker. Player territory is always protected from claims.
- Claiming after a war operation follows confirmed clearing, resource-backed administration and a handoff to permanent security. Claim authorization launches administration and infrastructure as independent project branches. Local police, piracy and temporary hostility cases use incident handling.
- Scrap recovery is outside the current design.

## Player interface

The Operations Board is sector-first. It should show operation phase, assigned assets, readiness, blockers and the observed result.

| Command | Purpose |
| --- | --- |
| Founding Buildout | Begin or resume the bounded founding chain. |
| Claim Sector | Evaluate the selected sector for a claim or conquest. |
| Prioritize Front | Raise priority for a selected front. |
| Restrict Sector | Exclude a sector from ordinary operations, construction or expansion. |
| Clear Directive | Clear the player directive and preserve normal faction duties. |
| Operations Report | Show active work, blockers and outcomes. |

Emergency ideas include suspending expansion, recalling expeditionary forces, defending sponsor space and halting new construction. A minimal control surface and report are the first integration target. A full map and board can follow.