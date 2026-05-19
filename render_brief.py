#!/usr/bin/env python3
"""
========================================================================
RENDER BRIEF — Documento maestro estilo LCG
========================================================================
Lee output/posts/*.json (producidos por extract_whitepaper.py) y genera:

    output/brief.html  — Documento HTML autocontenido con design system LCG
    output/brief.txt   — Versión plaintext del mismo brief

Uso:
    python render_brief.py

Requisitos:
    pip install markdown
========================================================================
"""

import json
import re
import html
from pathlib import Path
from datetime import datetime

import markdown as md_lib

OUTPUT_DIR = Path("./output")
POSTS_DIR = OUTPUT_DIR / "posts"
BRIEF_HTML = OUTPUT_DIR / "brief.html"
BRIEF_TXT = OUTPUT_DIR / "brief.txt"

# ========================================================================
# DATA LOAD
# ========================================================================

def load_posts() -> list[dict]:
    """Carga todos los .json de posts, ordenados por fecha desc."""
    files = sorted(POSTS_DIR.glob("*.json"))
    posts = []
    for f in files:
        try:
            posts.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  ! No pude leer {f.name}: {e}")
    posts.sort(key=lambda p: p.get("post_date", ""), reverse=True)
    return posts


def date_range(posts: list[dict]) -> tuple[str, str]:
    dates = [p.get("date") for p in posts if p.get("date")]
    if not dates:
        return ("—", "—")
    return (min(dates), max(dates))


# ========================================================================
# HTML RENDER — LCG design system
# ========================================================================

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,200;9..144,300;9..144,400;9..144,400&family=Manrope:wght@400;500;600;700&display=swap');

:root {
    --lcg-dark:   #085E54;
    --lcg-green:  #03B585;
    --lcg-mint:   #8AF4E9;
    --lcg-cream:  #F2EEE8;
    --lcg-ink:    #1A1E1B;
    --lcg-ink-60: rgba(26,30,27,0.62);
    --lcg-line:   rgba(8,94,84,0.18);
}

* { box-sizing: border-box; }

html, body {
    margin: 0;
    padding: 0;
    background: var(--lcg-cream);
    color: var(--lcg-ink);
    font-family: 'Manrope', -apple-system, sans-serif;
    font-size: 18px;
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

/* ====== Section frame ====== */
.section {
    position: relative;
    min-height: 100vh;
    padding: 80px 100px;
    border-bottom: 1px solid var(--lcg-line);
    page-break-after: always;
}
.section.dark {
    background: var(--lcg-dark);
    color: var(--lcg-cream);
}
.section.dark .meta,
.section.dark .eyebrow,
.section.dark .chrome-top,
.section.dark .chrome-bottom { color: rgba(242,238,232,0.72); }

/* ====== Chrome (top + bottom institutional) ====== */
.chrome-top, .chrome-bottom {
    position: absolute;
    left: 100px; right: 100px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Manrope', sans-serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--lcg-ink-60);
}
.chrome-top { top: 32px; }
.chrome-bottom { bottom: 32px; }

.emblem {
    display: inline-block;
    width: 10px; height: 10px;
    background: var(--lcg-green);
    border-radius: 999px;
    margin-left: 12px;
    vertical-align: middle;
}

/* ====== Typography ====== */
h1, h2, h3 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 300;
    letter-spacing: -0.03em;
    line-height: 1.0;
    margin: 0;
}
h1.display {
    font-weight: 200;
    font-size: clamp(80px, 11vw, 156px);
    line-height: 0.98;
}
h2.section-title {
    font-weight: 300;
    font-size: clamp(64px, 7vw, 96px);
    line-height: 1.02;
    margin-bottom: 48px;
}
h3.post-title {
    font-weight: 300;
    font-size: clamp(40px, 4.5vw, 64px);
    line-height: 1.05;
    margin-bottom: 16px;
}
em {
    font-style: italic;
    color: var(--lcg-green);
}

.eyebrow {
    font-family: 'Manrope', sans-serif;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--lcg-green);
    margin-bottom: 24px;
    display: inline-block;
}

.meta {
    font-family: 'Manrope', sans-serif;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--lcg-ink-60);
}

.num-big {
    font-family: 'Fraunces', serif;
    font-weight: 200;
    font-size: clamp(180px, 28vw, 360px);
    line-height: 0.9;
    letter-spacing: -0.04em;
    color: var(--lcg-green);
}

/* ====== Cover ====== */
.cover-content {
    display: grid;
    grid-template-rows: 1fr auto;
    min-height: calc(100vh - 160px);
    gap: 48px;
}
.cover-foot {
    display: grid;
    grid-template-columns: 440px 1fr auto;
    gap: 48px;
    align-items: end;
    border-top: 1px solid rgba(242,238,232,0.18);
    padding-top: 32px;
}
.cover-stat .label { display: block; margin-bottom: 6px; }
.cover-stat .value { font-family: 'Fraunces', serif; font-weight: 200; font-size: 64px; line-height: 1; color: var(--lcg-mint); }

/* ====== Index table ====== */
table.index {
    width: 100%;
    border-collapse: collapse;
    margin-top: 32px;
    font-family: 'Manrope', sans-serif;
}
table.index th {
    text-align: left;
    padding: 14px 16px 14px 0;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--lcg-ink-60);
    border-bottom: 1px solid var(--lcg-line);
}
table.index td {
    padding: 18px 16px 18px 0;
    border-bottom: 1px solid var(--lcg-line);
    vertical-align: top;
    font-size: 16px;
}
table.index td.date { font-family: 'Fraunces', serif; font-weight: 300; font-size: 18px; white-space: nowrap; width: 130px; color: var(--lcg-dark); }
table.index td.words { text-align: right; font-variant-numeric: tabular-nums; color: var(--lcg-ink-60); white-space: nowrap; width: 120px; }
table.index td.title a { color: var(--lcg-ink); text-decoration: none; border-bottom: 1px dashed var(--lcg-line); }
table.index td.title a:hover { border-bottom-color: var(--lcg-green); color: var(--lcg-dark); }
table.index td.title .subtitle { display: block; font-size: 14px; color: var(--lcg-ink-60); margin-top: 4px; line-height: 1.4; }

/* ====== Post entry ====== */
.post {
    max-width: 920px;
}
.post .post-subtitle {
    font-family: 'Fraunces', serif;
    font-weight: 300;
    font-style: italic;
    font-size: 26px;
    line-height: 1.3;
    color: var(--lcg-ink-60);
    margin: 0 0 32px 0;
}
.post .post-meta {
    display: flex;
    gap: 32px;
    margin-bottom: 48px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--lcg-line);
}
.post .post-meta .pill {
    display: inline-block;
    padding: 4px 14px;
    border: 1px solid var(--lcg-line);
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--lcg-dark);
}
.post .post-meta .pill.green { background: var(--lcg-green); color: var(--lcg-cream); border-color: var(--lcg-green); }
.post .body {
    font-family: 'Manrope', sans-serif;
    font-size: 17px;
    line-height: 1.7;
    color: var(--lcg-ink);
}
.post .body p { margin: 0 0 20px 0; }
.post .body h1, .post .body h2, .post .body h3, .post .body h4 {
    font-family: 'Fraunces', serif;
    font-weight: 400;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin: 40px 0 16px 0;
    color: var(--lcg-dark);
}
.post .body h1 { font-size: 36px; }
.post .body h2 { font-size: 30px; }
.post .body h3 { font-size: 24px; }
.post .body h4 { font-size: 20px; }
.post .body a { color: var(--lcg-dark); border-bottom: 1px solid var(--lcg-line); text-decoration: none; }
.post .body a:hover { color: var(--lcg-green); border-bottom-color: var(--lcg-green); }
.post .body blockquote {
    margin: 24px 0;
    padding: 16px 28px;
    border-left: 3px solid var(--lcg-green);
    background: rgba(3,181,133,0.04);
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 19px;
    line-height: 1.5;
    color: var(--lcg-dark);
}
.post .body img { max-width: 100%; height: auto; border-radius: 2px; margin: 24px 0; }
.post .body ul, .post .body ol { padding-left: 28px; margin: 0 0 24px 0; }
.post .body li { margin-bottom: 8px; }
.post .body hr { border: none; border-top: 1px solid var(--lcg-line); margin: 32px 0; }
.post .body code { font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-size: 0.9em; background: rgba(8,94,84,0.06); padding: 2px 6px; border-radius: 2px; }

/* ====== Print ====== */
@media print {
    .section { min-height: auto; padding: 60px 60px; }
    .chrome-top { top: 20px; }
    .chrome-bottom { bottom: 20px; }
    body { font-size: 11pt; }
    h1.display { font-size: 72pt; }
    h2.section-title { font-size: 36pt; }
    h3.post-title { font-size: 24pt; }
    .post .body { font-size: 10.5pt; }
}
"""


def chrome(section_label: str, breadcrumb: str, n: int, total: int) -> tuple[str, str]:
    top = f"""
<div class="chrome-top">
    <span>{html.escape(section_label)}<span class="emblem"></span></span>
    <span>LCG · WHITEPAPER INTELLIGENCE</span>
</div>"""
    bot = f"""
<div class="chrome-bottom">
    <span>{html.escape(breadcrumb)}</span>
    <span>{n:02d} / {total:02d}</span>
</div>"""
    return top, bot


def render_cover(posts: list[dict], total_sections: int) -> str:
    d_from, d_to = date_range(posts)
    word_total = sum(p.get("word_count", 0) or 0 for p in posts)
    ok = sum(1 for p in posts if p.get("auth_ok"))
    top, bot = chrome("BRIEF CONSOLIDADO", f"WHITEPAPER · TAG: HOY · {d_from} → {d_to}", 1, total_sections)
    return f"""
<section class="section dark" id="cover">
    {top}
    <div class="cover-content">
        <div>
            <span class="eyebrow" style="color: var(--lcg-mint);">Whitepaper.mx · Inteligencia editorial</span>
            <h1 class="display">Whitepaper,<br><em>Hoy</em>.</h1>
            <p class="meta" style="margin-top: 32px;">Compilado del tag «hoy» · {d_from} → {d_to}</p>
        </div>
        <div class="cover-foot">
            <div class="cover-stat"><span class="meta label">Entradas</span><span class="value">{len(posts):03d}</span></div>
            <div class="cover-stat"><span class="meta label">Auth OK</span><span class="value">{ok:03d}</span></div>
            <div class="cover-stat"><span class="meta label">Palabras totales</span><span class="value">{word_total:,}</span></div>
        </div>
    </div>
    {bot}
</section>"""


def render_index(posts: list[dict], total_sections: int) -> str:
    top, bot = chrome("ÍNDICE", "TABLA DE CONTENIDOS", 2, total_sections)
    rows = []
    for p in posts:
        anchor = anchor_for(p)
        title = html.escape(p.get("title", "").strip() or p.get("slug", ""))
        subtitle = html.escape((p.get("subtitle") or "").strip())
        words = p.get("word_count", 0) or 0
        rows.append(f"""
            <tr>
                <td class="date">{html.escape(p.get('date', ''))}</td>
                <td class="title">
                    <a href="#{anchor}">{title}</a>
                    {f'<span class="subtitle">{subtitle}</span>' if subtitle else ''}
                </td>
                <td class="words">{words:,} pal.</td>
            </tr>""")
    return f"""
<section class="section" id="index">
    {top}
    <span class="eyebrow">Índice</span>
    <h2 class="section-title">{len(posts)} entradas <em>en este brief</em>.</h2>
    <table class="index">
        <thead><tr><th>Fecha</th><th>Título</th><th style="text-align:right;">Extensión</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
    </table>
    {bot}
</section>"""


def anchor_for(p: dict) -> str:
    raw = f"{p.get('date','')}-{p.get('slug','')}"
    return re.sub(r"[^a-z0-9-]", "-", raw.lower()).strip("-")


def render_post(p: dict, n: int, total_sections: int) -> str:
    top, bot = chrome(f"ENTRADA · {p.get('date','')}", html.escape(p.get('title','')[:80]), n, total_sections)
    title = html.escape(p.get("title", "").strip() or p.get("slug", ""))
    subtitle = html.escape((p.get("subtitle") or "").strip())
    body_md = p.get("body_md") or ""
    body_html = md_lib.markdown(body_md, extensions=["extra", "sane_lists"])
    pills = [
        f'<span class="pill green">{p.get("date","")}</span>',
        f'<span class="pill">{p.get("word_count", 0):,} palabras</span>',
    ]
    if p.get("audience"):
        pills.append(f'<span class="pill">{html.escape(p["audience"])}</span>')
    if not p.get("auth_ok"):
        pills.append('<span class="pill" style="border-color:#a33;color:#a33;">contenido parcial</span>')

    return f"""
<section class="section" id="{anchor_for(p)}">
    {top}
    <article class="post">
        <span class="eyebrow">{html.escape(p.get('date',''))} · Whitepaper.mx</span>
        <h3 class="post-title">{title}</h3>
        {f'<p class="post-subtitle">{subtitle}</p>' if subtitle else ''}
        <div class="post-meta">{' '.join(pills)} <a href="{html.escape(p.get('url',''))}" class="pill" style="text-decoration:none;">Abrir original ↗</a></div>
        <div class="body">{body_html}</div>
    </article>
    {bot}
</section>"""


def render_html(posts: list[dict]) -> str:
    total_sections = len(posts) + 2  # cover + index + N posts
    sections = [render_cover(posts, total_sections), render_index(posts, total_sections)]
    for i, p in enumerate(posts, start=3):
        sections.append(render_post(p, i, total_sections))
    d_from, d_to = date_range(posts)
    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<title>Whitepaper Hoy · Brief Consolidado {d_from} → {d_to}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{CSS}</style>
</head>
<body>
{''.join(sections)}
</body>
</html>"""


# ========================================================================
# TXT RENDER
# ========================================================================

def hr(char="=", width=80) -> str:
    return char * width

def wrap_para(text: str, width: int = 80) -> str:
    import textwrap
    paras = re.split(r"\n\s*\n", text.strip())
    out = []
    for p in paras:
        p = re.sub(r"\s+", " ", p).strip()
        if not p:
            continue
        out.append(textwrap.fill(p, width=width))
    return "\n\n".join(out)


def render_txt(posts: list[dict]) -> str:
    d_from, d_to = date_range(posts)
    word_total = sum(p.get("word_count", 0) or 0 for p in posts)
    ok = sum(1 for p in posts if p.get("auth_ok"))

    out = []
    # ===== Cover =====
    out.append(hr("="))
    out.append("LCG · WHITEPAPER INTELLIGENCE")
    out.append("BRIEF CONSOLIDADO · TAG «HOY»")
    out.append(hr("="))
    out.append("")
    out.append("        WHITEPAPER, HOY.")
    out.append(f"        Compilado del tag «hoy» · {d_from} → {d_to}")
    out.append("")
    out.append(f"        Entradas:         {len(posts):>6}")
    out.append(f"        Auth OK:          {ok:>6}")
    out.append(f"        Palabras totales: {word_total:>6,}")
    out.append("")
    out.append(hr("="))
    out.append("")

    # ===== Index =====
    out.append("ÍNDICE")
    out.append(hr("-"))
    out.append(f"{'FECHA':<12} {'TEMAS DEL DÍA':<60} {'PALABRAS':>8}")
    out.append(hr("-"))
    for p in posts:
        # El title es siempre "Whitepaper, Hoy" — el subtitle trae los temas reales
        topics = (p.get("subtitle") or p.get("title") or p.get("slug") or "").strip()
        # Recorta a 60 chars
        if len(topics) > 60:
            topics = topics[:57].rstrip() + "..."
        out.append(f"{p.get('date',''):<12} {topics:<60} {p.get('word_count',0):>8,}")
    out.append(hr("-"))
    out.append("")
    out.append("")

    # ===== Posts =====
    for i, p in enumerate(posts, start=1):
        out.append(hr("="))
        out.append(f"ENTRADA {i:03d} / {len(posts):03d}  ·  {p.get('date','')}")
        out.append(hr("="))
        out.append("")
        title = p.get("title", "").strip() or p.get("slug", "")
        out.append(title.upper())
        out.append(hr("-", len(title)))
        if p.get("subtitle"):
            out.append("")
            out.append(f"« {p['subtitle'].strip()} »")
        out.append("")
        meta = [
            f"Fecha: {p.get('date','')}",
            f"URL: {p.get('url','')}",
            f"Palabras: {p.get('word_count', 0):,}",
        ]
        if not p.get("auth_ok"):
            meta.append("⚠ Contenido parcial (auth/paywall)")
        out.append(" · ".join(meta))
        out.append("")
        out.append(hr("-"))
        out.append("")
        body = p.get("body_md") or "[contenido no disponible]"
        # Strip markdown syntax cosmetically for plaintext
        body_clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)  # links → text
        body_clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", body_clean)  # bold
        body_clean = re.sub(r"\*([^*]+)\*", r"\1", body_clean)      # italic
        body_clean = re.sub(r"^#+\s+", "", body_clean, flags=re.MULTILINE)  # headings
        out.append(wrap_para(body_clean))
        out.append("")
        out.append("")

    return "\n".join(out)


# ========================================================================
# MAIN
# ========================================================================

def main():
    print("="*72)
    print("RENDER BRIEF — LCG design system")
    print("="*72)

    if not POSTS_DIR.exists():
        print(f"ERROR: no existe {POSTS_DIR}. Corre primero extract_whitepaper.py")
        return

    posts = load_posts()
    if not posts:
        print(f"ERROR: no encontré posts en {POSTS_DIR}")
        return

    print(f"  Cargados {len(posts)} posts")
    d_from, d_to = date_range(posts)
    print(f"  Rango: {d_from} → {d_to}")

    # HTML
    html_doc = render_html(posts)
    BRIEF_HTML.write_text(html_doc, encoding="utf-8")
    print(f"  ✓ HTML: {BRIEF_HTML.resolve()} ({len(html_doc):,} chars)")

    # TXT
    txt_doc = render_txt(posts)
    BRIEF_TXT.write_text(txt_doc, encoding="utf-8")
    print(f"  ✓ TXT:  {BRIEF_TXT.resolve()} ({len(txt_doc):,} chars)")

    print("="*72)
    print("LISTO")
    print("="*72)


if __name__ == "__main__":
    main()
