#!/usr/bin/env python3
"""Assemble a self-contained explainer HTML page for the `explain-code` skill.

Reads the page template (assets/template.html), fills in title / subtitle / path and the body
content fragment, and INLINES the bundled Tailwind (assets/tailwind.js) and Mermaid
(assets/mermaid.min.js) libraries so the resulting single HTML file renders fully offline with
NO CDN dependency.

Usage:
    python build_explainer.py --title "X" --path "src/.../Foo.java#bar" --content body.html --out page.html

`--content` is a file holding the inner HTML for <main> (the 8 prescribed <section> blocks).
Defaults for --template / --tailwind / --mermaid resolve to this skill's assets/ directory.
If a library file is missing, the page is still written (Tailwind/Mermaid features degrade).
"""
import argparse
from pathlib import Path


def inject(html: str, marker: str, lib_path: Path) -> str:
    if lib_path.exists():
        return html.replace(marker, "<script>\n" + lib_path.read_text(encoding="utf-8") + "\n</script>")
    return html.replace(marker, f"<!-- {lib_path.name} not bundled -->")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--path", default="", help="file path / breadcrumb shown in the top nav")
    ap.add_argument("--content", required=True, help="path to the body HTML fragment")
    ap.add_argument("--out", required=True)
    ap.add_argument("--template", default=None)
    ap.add_argument("--tailwind", default=None)
    ap.add_argument("--mermaid", default=None)
    a = ap.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    template = Path(a.template) if a.template else skill_dir / "assets" / "template.html"
    tailwind = Path(a.tailwind) if a.tailwind else skill_dir / "assets" / "tailwind.js"
    mermaid = Path(a.mermaid) if a.mermaid else skill_dir / "assets" / "mermaid.min.js"

    html = template.read_text(encoding="utf-8")
    content = Path(a.content).read_text(encoding="utf-8")

    html = (html
            .replace("__TITLE__", a.title)
            .replace("__SUBTITLE__", a.subtitle)
            .replace("__PATH__", a.path)
            .replace("__CONTENT__", content))

    html = inject(html, "<!--__TAILWIND_LIB__-->", tailwind)
    html = inject(html, "<!--__MERMAID_LIB__-->", mermaid)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    tw = "inlined" if tailwind.exists() else "MISSING"
    mm = "inlined" if mermaid.exists() else "MISSING"
    print(f"wrote {out} ({len(html):,} bytes; tailwind {tw}, mermaid {mm})")


if __name__ == "__main__":
    main()
