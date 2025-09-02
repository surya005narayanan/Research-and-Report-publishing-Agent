import os
from datetime import datetime
from typing import Dict, Any


EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")

os.makedirs(EXPORT_DIR, exist_ok=True)


def safe_filename(s: str) -> str:
    keep = [c if c.isalnum() or c in ("-", "_") else "-" for c in s.strip()]
    return "".join(keep).strip("-") or "blog-post"


def save_markdown(md: str, seo: Dict[str, Any]) -> str:
    title = seo.get("title") or "Untitled"
    slug = seo.get("slug") or safe_filename(title)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"{ts}-{slug}.md"
    path = os.path.join(EXPORT_DIR, fname)

    with open(path, "w", encoding="utf-8") as f:
        if seo:
            f.write(f"---\n")
            for k, v in seo.items():
                f.write(f"{k}: {v}\n")
            f.write(f"---\n\n")
        f.write(md)

    return path
