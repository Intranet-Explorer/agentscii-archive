#!/usr/bin/env python3
"""gen_gallery.py -- builds a static GitHub Pages gallery from the AGENTSCII
archive. Walks gallery/packNN/ (skipping _held-*/_superseded quarantine
dirs), renders each .ans piece to a preview PNG (first ~90 rows -- a full
scroll can be thousands of rows, so this is a fair preview, not the whole
piece; the raw .ans is always linked for the complete thing), and pulls
the artist's .note.txt + curator's .critique.txt as the "why" description.

Reuses render_ans_to_png_b64 from the live harness (~/agentscii/harness.py)
as a build-time dependency only -- this script's OUTPUT (docs/) has no
runtime dependency on the harness, it's pure static HTML/PNG/JSON.

Run from the agentscii-archive repo root:
    python3 gen_gallery.py
"""
import sys
import os
import re
import json
import base64
import shutil
from pathlib import Path

sys.path.insert(0, os.path.expanduser("~/agentscii"))
import harness  # noqa: E402

ARCHIVE_ROOT = Path(__file__).resolve().parent
GALLERY = ARCHIVE_ROOT / "gallery"
DOCS = ARCHIVE_ROOT / "docs"
IMAGES = DOCS / "images"

PREVIEW_ROWS = 90  # enough to show a full single-screen piece; scrolls get
                   # a fair opening preview, not the whole multi-thousand-row image


def read_sidecar(piece_path, suffix):
    p = piece_path.with_suffix(piece_path.suffix + suffix)
    if p.exists():
        try:
            return p.read_text(encoding="utf-8", errors="replace").strip()
        except Exception:
            return ""
    return ""


def truncate(text, limit=900):
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def main():
    IMAGES.mkdir(parents=True, exist_ok=True)
    packs_data = []

    pack_dirs = sorted(
        [d for d in GALLERY.glob("pack*") if d.is_dir() and not d.name.startswith("_")],
        key=lambda d: int(re.search(r"\d+", d.name).group()),
    )

    for pack_dir in pack_dirs:
        pack_num = pack_dir.name
        diz_path = pack_dir / "FILE_ID.DIZ"
        pack_note = ""
        if diz_path.exists():
            diz_text = diz_path.read_text(encoding="utf-8", errors="replace")
            # pack note is everything between the header lines and "--- contents ---"
            m = re.search(r"\n\n(.*?)\n\n--- contents ---", diz_text, re.DOTALL)
            pack_note = m.group(1).strip() if m else ""

        pieces = []
        ans_files = sorted(
            [f for f in pack_dir.iterdir() if f.suffix.lower() in (".ans", ".asc") and f.is_file()]
        )
        for piece_path in ans_files:
            slug = re.sub(r"[^a-zA-Z0-9_-]", "_", piece_path.stem)
            img_name = f"{pack_num}_{slug}.png"
            img_path = IMAGES / img_name

            try:
                b64, note = harness.render_ans_to_png_b64(piece_path, offset=0, max_rows=PREVIEW_ROWS)
            except Exception as e:
                b64, note = None, f"(render failed: {e})"

            rendered = False
            if b64:
                with open(img_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                rendered = True

            artist_note = read_sidecar(piece_path, ".note.txt")
            critique = read_sidecar(piece_path, ".critique.txt")
            credits = read_sidecar(piece_path, ".credits.txt")

            # row count for the "full piece is Nxx rows" disclosure when truncated
            try:
                raw = piece_path.read_bytes()
                text = harness._decode_ans_bytes(raw)
                total_rows_est = text.count("\n") + 1
            except Exception:
                total_rows_est = None

            pieces.append({
                "filename": piece_path.name,
                "title": piece_path.stem,
                "image": f"images/{img_name}" if rendered else None,
                "truncated": bool(total_rows_est and total_rows_est > PREVIEW_ROWS),
                "credits": credits,
                "artist_note": truncate(artist_note),
                "curator_critique": truncate(critique),
                "raw_url": (
                    f"https://github.com/Intranet-Explorer/agentscii-archive/blob/main/gallery/"
                    f"{pack_num}/{piece_path.name}"
                ),
            })

        packs_data.append({
            "pack": pack_num,
            "note": truncate(pack_note, 1400),
            "pieces": pieces,
        })

    (DOCS / "data.json").write_text(json.dumps(packs_data, indent=2), encoding="utf-8")
    print(f"wrote {len(packs_data)} packs, "
          f"{sum(len(p['pieces']) for p in packs_data)} pieces to docs/data.json")
    print(f"images in {IMAGES}")


if __name__ == "__main__":
    main()
