#!/usr/bin/env python3
"""
Dump per-state extract data for downstream analysis by agents.
Lee de output/posts/*.json, construye los extractos relevantes por estado,
y los guarda en output/intel/state-{slug}.json con todo el contexto que un
agente analista necesita.
"""

import json
import re
from pathlib import Path
from collections import Counter

# Reutiliza la lógica del state_intel
import sys
sys.path.insert(0, str(Path(__file__).parent))
from state_intel import (
    ZONA_ESTADOS, ESTADOS_PATTERNS, CRM_DATA, PPT_FAMILIAS,
    SECTORES, EVENTOS, load_posts, split_topics, clean_excerpt,
    find_entities, find_ppt_families, match_taxonomy, slugify,
    build_state_intel,
)

OUT = Path("./output")
INTEL_DIR = OUT / "intel"


def main():
    INTEL_DIR.mkdir(parents=True, exist_ok=True)
    posts = load_posts()
    print(f"Loaded {len(posts)} posts")

    for st in ZONA_ESTADOS:
        intel = build_state_intel(st, posts)
        slug = slugify(st)
        out_path = INTEL_DIR / f"state-{slug}.json"

        # PPT families lookup
        ppt_fams = []
        for label, aliases in PPT_FAMILIAS.get(st, []):
            ppt_fams.append({
                "label": label,
                "aliases": aliases,
                "mentioned_in_whitepaper": label in intel["ppt_families_mentioned"],
                "mention_count": len(intel["ppt_families_mentioned"].get(label, [])),
                "mention_dates": [m["date"] for m in intel["ppt_families_mentioned"].get(label, [])],
            })

        payload = {
            "state": st,
            "crm_context": intel["crm"],
            "ppt_families_full_list": ppt_fams,
            "stats": {
                "total_excerpts": intel["total_excerpts"],
                "ppt_families_hit": intel["ppt_families_hit"],
                "ppt_families_total": intel["ppt_families_total"],
                "top_sectors": intel["top_sectors"],
                "top_events": intel["top_events"],
                "new_entities_detected": intel["new_entities"],
            },
            "excerpts": intel["excerpts"],
        }
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print(f"  ✓ {out_path} ({len(intel['excerpts'])} excerpts, {len(payload['excerpts'])} chars≈)")


if __name__ == "__main__":
    main()
