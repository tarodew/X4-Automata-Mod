# Automata V9.0.0A0.1

**Reconstructed source checkpoint, not a gameplay release. No in-game test has been performed.**

This is a fresh YoRHa implementation based on the supplied X4 9.0 game source. It is not a renamed v1.14 or v1.15 archive. Earlier checkpoint reports survive in the YoRHa authority, but their source packages were not recovered in this session.

## Implemented in this checkpoint

- Independent `yorha` faction and stable `nyto_automata` extension identity.
- Terran technological donor, deliberate player +30 relation, Xenon/Kha'ak hostility.
- One Earth Bunker, declared through the native GOD station mechanism. Its provisional native Terran maintenance blueprint has no claim module or hull fabrication modules.
- One latched founding Kyushu creation. All later ships must pass the forthcoming procurement adapter; there is no generic free fleet spawn.
- Versioned persistent state and a single resettable heartbeat.
- Ready-report conversation entry for player/YoRHa actors.
- Fixed design and station-module contracts for subsequent stages, without executing them yet.

## Safety and verification boundary

All operational planners are paused. Loading this extension does create the founding faction/station/Builder state, so use only a **fresh disposable test save**, never the real campaign. Do not install alongside older mods that also define faction `yorha`. Do not remove the extension from a save and assume that reverses its world changes.

No X4 process was launched during creation. XML parsing is not evidence of successful initialization, UI operation, docking, claiming, or save/reload. See `docs/verification.md` for actual checks.

The Terran banner and icons are temporary native placeholders. Final player-designed station geometry remains deferred. Installation is a manual user action; this package contains no installer and changes no local game files by itself.
