# Automata project instructions

This repository contains the Automata extension for X4: Foundations. The extension source is under `Automata/`.

## Start here

- For a Windows install or update, read [the install handoff](docs/WINDOWS-INSTALL-HANDOFF.md) and inspect the installed extension's `content.xml` before changing files. Use the pinned candidate for this installation.
- For design or code changes, read [design](docs/DESIGN.md), [stations and economy](docs/STATIONS-AND-ECONOMY.md), and [fleets and operations](docs/FLEETS-AND-OPERATIONS.md) as relevant. Use [the build log](docs/BUILD-LOG.md) for implementation status and [testing](docs/TESTING.md) for evidence requirements. The roadmap describes intended work. The build log records what has been checked.
- Use the user's latest decisions to resolve scope. If an older checkpoint or comment differs from the design documents, use the current decisions. State material discrepancies and record the source for any approved design change.

## Preserve the design

- YoRHa is the player's +30 sponsor faction. Mirror persistent player faction relations, including Xenon and Yaki. Cloak, cover identity and local aggression do not change faction-wide diplomacy. Player sectors can receive sponsor infrastructure and are never claim targets.
- Bunker stays on Earth. Use native X4 systems for construction, trade, procurement, fleet orders and servicing. Preserve paid player-yard procurement, the single founding Kyushu, the documented Terran continuity exception and the 14-Builder limit. YoRHa has no wharf or shipyard.
- Keep the approved station and fleet counts, player directives, saved identities and paused startup. Preserve the distinction between an ideal Core and one YoRHa can use. Keep regional High Command promotion on the existing station.
- Report offline and in-game evidence separately. An install request covers installing the specified package and verifying its files. Launching the game, migrating a legacy extension or modifying saves requires its own request.
