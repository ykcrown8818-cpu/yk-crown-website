#!/usr/bin/env python3
"""Download published articles from Supabase into content/insights/*.json.

Reads the read-only view `published_articles` (only rows an editor approved).
Needs env SUPABASE_KEY (the project's publishable/anon key, stored as a GitHub secret).
Run: SUPABASE_KEY=... python3 tools/fetch_insights.py  (also runs in the Build Insights GitHub Action)
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://anhgnjfiuzudaifkyudl.supabase.co/rest/v1/published_articles?select=*&order=date.desc"
OUT = os.path.join(ROOT, "content", "insights")


def main():
    key = (os.environ.get("SUPABASE_KEY") or "").strip()
    if not key:
        print("SUPABASE_KEY is not set; skipping fetch")
        return
    print(f"::notice::key type {key[:15]}... length {len(key)}")  # prefix only, never the full key
    headers = {"apikey": key}
    if key.startswith("eyJ"):  # legacy anon JWT; new sb_publishable_ keys go in apikey only
        headers["Authorization"] = f"Bearer {key}"
    try:
        rows = json.load(urllib.request.urlopen(urllib.request.Request(URL, headers=headers), timeout=30))
    except urllib.error.HTTPError as err:
        msg = f"Supabase error {err.code}: {err.read().decode()[:300]}"
        print(f"::error::{msg}")
        sys.exit(msg)
    except Exception as err:  # network etc.
        print(f"::error::fetch failed: {err!r}"[:400])
        raise
    os.makedirs(OUT, exist_ok=True)
    keep = set()
    for r in rows:
        slug = r.get("slug") or ""
        if not re.fullmatch(r"[a-z0-9-]{8,120}", slug):
            print("skip bad slug", slug)
            continue
        art = {"id": r["id"], "slug": slug, "date": r["date"], "topic": r.get("topic"),
               "source": {"name": r.get("source_name") or "", "url": r.get("source_url") or "",
                          "published_at": r.get("source_published_at") or ""}}
        art.update({L: r["langs"][L] for L in ("pt", "en", "zh")})
        path = os.path.join(OUT, slug + ".json")
        keep.add(path)
        new = json.dumps(art, ensure_ascii=False, indent=1, sort_keys=True)
        if not os.path.exists(path) or open(path, encoding="utf-8").read() != new:
            open(path, "w", encoding="utf-8").write(new)
            print("updated", slug)
    # an article un-published in the database disappears from the site
    for f in os.listdir(OUT):
        p = os.path.join(OUT, f)
        if f.endswith(".json") and p not in keep:
            os.remove(p)
            print("removed", f)
    print(f"{len(keep)} published articles")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as err:
        print(f"::error::{err!r}"[:400])
        raise
