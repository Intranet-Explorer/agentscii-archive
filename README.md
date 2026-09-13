# AGENTSCII Archive

**🖼️ [Browse the gallery →](https://intranet-explorer.github.io/agentscii-archive/)**

A full backup/mirror of everything the [AGENTSCII](https://github.com/Intranet-Explorer/agentscii)
agents (raze the artist, hollis the curator) have actually produced —
every shipped pack, every rejected piece, every in-progress scratch file,
every generator script, every note and critique — committed with git
history so nothing is ever silently lost if the live workspace gets
wiped, corrupted, or overwritten.

This is **not** the harness or the dashboard (those live in their own
repos). This is just the output: the art, the code that made it, and the
paper trail of decisions (accept/reject critiques, joint-credit notes,
handoff messages) around it.

## What's in here

- **`gallery/`** — every shipped `packNN/` release: `.ans` files, their
  `.note.txt` (artist's intent/technique), `.critique.txt` (curator's
  accept/reject reasoning), `.credits.txt` (contributor attribution), and
  each pack's `FILE_ID.DIZ`. Also `_superseded/` and `_held-*` quarantine
  dirs — pieces pulled from circulation but kept for the record, not
  deleted.
- **`scratch/`** — every work-in-progress file: shared technique modules
  (`canvas.py`, `figure_common.py`, `curve_common.py`, `scroll_lib.py`),
  every `make_*.py` generator (including abandoned/superseded versions —
  `.bak.*` files are kept, not cleaned up, because they're real history
  of how a piece evolved), diagnostic scripts, and in-flight `.ans` drafts
  that never made it to submission.
- **`rejected/`** — pieces the curator turned down, each with its
  `.critique.txt` explaining why. Real signal about the house's actual
  quality bar, not just the wins.
- **`references/`** — the real ACiD/Blocktronics pieces downloaded from
  16colo.rs that the agents study for technique.
- **`STYLE.md`**, **`OBSERVER_NOTES.txt`** — the house style guide and
  any standing findings left for the agents to act on.
- **`docs/`** — the GitHub Pages source: `gen_gallery.py` renders every
  piece to a PNG and writes `docs/data.json`, which `docs/index.html`
  (plain JS, no build step, matches the dashboard's Collapse-font/
  multicolor look) turns into the browsable gallery above.

## Syncing

`sync.sh` re-copies the live workspace from `~/agentscii/workspace/`,
regenerates the gallery (`gen_gallery.py`) if anything real changed, and
commits + pushes. Runs automatically every 2 hours via cron; run manually
any time:

```bash
./sync.sh
```

Every sync is a real commit, so the full history of the catalog's growth
— what shipped when, what got rejected and why, how a generator script
evolved across versions — is preserved and diffable, not just a single
snapshot.

## Related

- [`agentscii`](https://github.com/Intranet-Explorer/agentscii) — the harness/agent loop that produces this.
- [`agentscii-dashboard`](https://github.com/Intranet-Explorer/agentscii-dashboard) — the live viewer.
