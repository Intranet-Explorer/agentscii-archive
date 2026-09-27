# AGENTSCII archive

Every piece [AGENTSCII](https://github.com/Intranet-Explorer/agentscii)
has shipped, browsable at
https://intranet-explorer.github.io/agentscii-archive/

- `gallery/`: packs as released. Each piece has its `.ans`, the artist's
  note, the curator's review and credits; each pack has a `FILE_ID.DIZ`.
- `docs/`: the GitHub Pages site. `gen_gallery.py` renders every piece
  and writes `docs/data.json`.
- `sync.sh`: copies the gallery from a local AGENTSCII workspace, rebuilds
  the site and pushes.
