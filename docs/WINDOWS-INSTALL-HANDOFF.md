# Automata Windows install handoff

## Candidate

| Field | Value |
| --- | --- |
| Mod | Automata V9.0.0A1.0 test candidate |
| Repository | `tarodew/X4-Automata-Mod` |
| Handoff branch | `build/automata-a1` |
| Exact package source | Commit `b8bb85d63b3cfdc44b72005ec4bf995dda31dc21`, directory `Automata/` |
| Extension identity | `nyto_automata`, version `100` in `content.xml` |
| Game | X4: Foundations 9.0 and Terran DLC (`ego_dlc_terran`) |
| Package SHA-256 | `fbf62cb020034f27ebb073fe091c21db29640c94216eab379ce91e0a5224f470` |

[Exact candidate source](https://github.com/tarodew/X4-Automata-Mod/tree/b8bb85d63b3cfdc44b72005ec4bf995dda31dc21/Automata) · [Build evidence](BUILD-LOG.md) · [Test plan](TESTING.md)

The build passed 145 offline checks. Runtime and save/reload remain unverified. Initial engine validation is intended for a fresh disposable save.

## Installation procedure

1. Locate the Windows Steam library containing X4 by reading Steam's library folders and the X4 app manifest (AppID `392160`), or use Steam's Browse local files command. Verify `X4.exe` and the game's `extensions` directory. Respect any drive exclusions in the current request. Check that X4 is closed before writing extension files.
2. Inspect the local Automata folders and their `content.xml` files. Match by extension ID, version and name, since folder names can vary. If an older installation identifies itself as `automata` or any ID other than `nyto_automata`, treat it as a separate extension identity. A folder rename does not migrate a save. Report a legacy-only or conflicting installation before replacing or disabling it.
3. Use the files from the pinned candidate's `Automata/` directory. If using the prepared ZIP, verify its SHA-256 before extraction. Stage the complete extension outside the active extensions directory. For an identified `nyto_automata` update, back up the existing folder outside `extensions` and replace it as a whole, preserving the old copy. Restore the backup if the swap or verification fails. A new install, when requested, should place the candidate under `extensions\Automata`.
4. Verify that the destination contains `content.xml` directly at its root with ID `nyto_automata` and version `100`. Compare the installed files with the staged source and report the destination, previous ID/version and backup path. Leave X4 closed and existing saves untouched.

This handoff authorizes no source changes by itself. Follow the current user's installation request.
