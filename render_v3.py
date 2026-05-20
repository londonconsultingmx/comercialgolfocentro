#!/usr/bin/env python3
"""
========================================================================
RENDER v3 — Páginas por estado con análisis narrativo embebido
========================================================================
Combina:
  - output/intel/state-{slug}.json  (datos crudos: extractos, familias PPT, stats)
  - output/intel/analysis-{slug}.json (análisis estructurado de Claude)
Y produce:
  - docs/estado-{slug}.html — página por estado con pulso, temas, actores,
                              oportunidades, alertas, extractos
  - docs/zona.html y docs/index.html (overview)
========================================================================
"""

import json
import re
import html
import shutil
from pathlib import Path
from collections import Counter

import sys
sys.path.insert(0, str(Path(__file__).parent))
from state_intel import (
    ZONA_ESTADOS, CRM_DATA, PPT_FAMILIAS, slugify,
    chrome_header, chrome_footer, CSS,
)

OUT = Path("./output")
INTEL_DIR = OUT / "intel"
DOCS = Path("./docs")


# ========================================================================
# Extended CSS (apilado a state_intel.CSS)
# ========================================================================
EXTRA_CSS = r"""
/* ====== Pulso block ====== */
.pulso { padding: 32px 40px; margin: 32px 0 48px 0; border-left: 4px solid var(--lcg-green); background: rgba(3,181,133,0.04); }
.pulso p { font-family: 'Fraunces', serif; font-weight: 300; font-style: italic; font-size: 22px; line-height: 1.5; color: var(--lcg-ink); margin: 0 0 18px 0; }
.pulso p:last-child { margin-bottom: 0; }

/* ====== Lectura comercial / exec banner ====== */
.qbanner { padding: 24px 32px; margin: 24px 0 32px 0; border-radius: 2px; font-size: 16px; line-height: 1.65; color: var(--lcg-ink); background: rgba(3,181,133,0.06); border: 1px solid var(--lcg-green); }
.qbanner strong { display: block; font-family: 'Manrope', sans-serif; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; font-size: 11px; color: var(--lcg-green); margin-bottom: 12px; }

/* ====== Theme cards ====== */
.themes { display: grid; grid-template-columns: 1fr; gap: 0; margin: 24px 0 48px 0; }
.theme { padding: 32px 0; border-top: 1px solid var(--lcg-line); }
.theme:first-child { border-top: none; padding-top: 16px; }
.theme h3 { margin-bottom: 12px; }
.theme .t-meta { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.theme .t-meta .pill { display: inline-block; font-size: 10px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; padding: 4px 10px; border: 1px solid var(--lcg-line); border-radius: 999px; color: var(--lcg-dark); }
.theme .t-meta .pill.sector { background: rgba(3,181,133,0.08); border-color: var(--lcg-green); color: var(--lcg-dark); }
.theme .t-meta .pill.date { color: var(--lcg-ink-60); }
.theme p { font-size: 16px; line-height: 1.65; color: var(--lcg-ink); margin: 0 0 16px 0; max-width: 920px; }
.theme .implica { padding: 14px 20px; background: rgba(8,94,84,0.04); border-left: 3px solid var(--lcg-dark); margin-top: 12px; max-width: 920px; }
.theme .implica strong { display: block; font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--lcg-dark); margin-bottom: 4px; }
.theme .implica p { font-size: 14px; margin: 0; color: var(--lcg-ink); }

/* ====== Actor cards ====== */
.actores { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin: 24px 0 48px 0; }
.actor { padding: 20px 24px; border: 1px solid var(--lcg-line); border-radius: 2px; background: rgba(242,238,232,0.6); position: relative; }
.actor.crm { border-color: var(--lcg-green); background: rgba(3,181,133,0.04); }
.actor.crm::after { content: '✓ CRM'; position: absolute; top: 14px; right: 18px; font-size: 9px; font-weight: 700; letter-spacing: 0.18em; color: var(--lcg-green); padding: 2px 8px; border: 1px solid var(--lcg-green); border-radius: 999px; }
.actor::after { position: absolute; top: 14px; right: 18px; content: 'NUEVO'; font-size: 9px; font-weight: 700; letter-spacing: 0.18em; color: var(--lcg-ink-60); padding: 2px 8px; border: 1px solid var(--lcg-line); border-radius: 999px; }
.actor h4 { margin: 0 60px 12px 0; font-size: 19px; }
.actor .a-row { font-size: 13px; line-height: 1.55; margin: 8px 0; }
.actor .a-label { font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--lcg-ink-60); display: block; margin-bottom: 2px; }

/* ====== Oportunidades ====== */
.oport { display: grid; grid-template-columns: 1fr; gap: 0; margin: 24px 0 48px 0; }
.opp { padding: 28px 0; border-top: 1px solid var(--lcg-line); display: grid; grid-template-columns: 1fr 200px; gap: 32px; align-items: start; }
.opp:first-child { border-top: none; padding-top: 16px; }
.opp .o-main h3 { margin-bottom: 14px; }
.opp .o-tipo { display: inline-block; font-size: 10px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; padding: 4px 10px; background: var(--lcg-dark); color: var(--lcg-cream); border-radius: 999px; margin-bottom: 12px; }
.opp .o-grid { display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 10px; font-size: 14px; line-height: 1.6; }
.opp .o-grid .o-row { padding: 6px 0; border-bottom: 1px dotted var(--lcg-line); }
.opp .o-grid .o-row:last-child { border-bottom: none; }
.opp .o-grid .o-label { font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--lcg-ink-60); display: block; margin-bottom: 2px; }
.opp .o-urg { padding: 16px 18px; border: 1px solid var(--lcg-line); border-radius: 2px; text-align: center; }
.opp .o-urg.alta { border-color: #C9A800; background: rgba(255,200,0,0.06); }
.opp .o-urg.media { border-color: var(--lcg-line); }
.opp .o-urg.baja { border-color: var(--lcg-line); background: rgba(242,238,232,0.4); }
.opp .o-urg .l { display: block; font-size: 10px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--lcg-ink-60); }
.opp .o-urg .v { font-family: 'Fraunces', serif; font-weight: 300; font-size: 32px; line-height: 1; color: var(--lcg-dark); margin-top: 6px; display: block; }
.opp .o-urg.alta .v { color: #C9A800; }

/* ====== Alertas + gaps ====== */
.list-alerts { list-style: none; padding: 0; margin: 16px 0 32px 0; }
.list-alerts li { padding: 16px 20px 16px 56px; border: 1px solid var(--lcg-line); margin-bottom: 8px; position: relative; border-radius: 2px; font-size: 14px; line-height: 1.6; }
.list-alerts li::before { content: '⚠'; position: absolute; left: 18px; top: 14px; font-size: 20px; color: #C9A800; }
.list-alerts li strong { display: block; font-weight: 700; color: var(--lcg-dark); margin-bottom: 4px; }

.list-gaps { list-style: none; padding: 0; margin: 16px 0 32px 0; columns: 2; column-gap: 32px; }
.list-gaps li { font-size: 14px; padding: 8px 0 8px 24px; position: relative; break-inside: avoid; line-height: 1.5; color: var(--lcg-ink); }
.list-gaps li::before { content: '○'; position: absolute; left: 6px; top: 7px; color: var(--lcg-green); font-weight: 700; }
@media (max-width: 768px) { .list-gaps { columns: 1; } }

/* TOC for state page */
.state-toc { display: flex; flex-wrap: wrap; gap: 6px; margin: 24px 0 48px 0; }
.state-toc a { font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; padding: 6px 14px; border: 1px solid var(--lcg-line); border-radius: 999px; color: var(--lcg-dark); text-decoration: none; }
.state-toc a:hover { background: var(--lcg-green); color: var(--lcg-cream); border-color: var(--lcg-green); }
"""


# ========================================================================
# RENDER
# ========================================================================

def render_pulso(pulso_text: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\s*\n", pulso_text) if p.strip()]
    if not paras:
        paras = [pulso_text]
    pp = "".join(f"<p>{html.escape(p)}</p>" for p in paras)
    return f'<div class="pulso">{pp}</div>'


def render_exec_banner(slug: str) -> str:
    """Lee el resumen ejecutivo de oportunidades comerciales (lenguaje de negocio,
    generado por agente leyendo el análisis profundo) y lo renderiza como banner verde."""
    exec_path = INTEL_DIR / f"exec-{slug}.txt"
    if not exec_path.exists():
        return ""
    text = exec_path.read_text(encoding="utf-8").strip()
    if not text:
        return ""
    return f'<div class="qbanner rica"><strong>Lectura comercial</strong>{html.escape(text)}</div>'


def render_themes(themes: list[dict]) -> str:
    if not themes:
        return '<p class="meta">Sin temas dominantes detectables con los extractos disponibles.</p>'
    out = []
    for t in themes:
        sectors = "".join(f'<span class="pill sector">{html.escape(s)}</span>' for s in t.get("sectores", []))
        dates = "".join(f'<span class="pill date">{html.escape(d)}</span>' for d in t.get("evidence_dates", [])[:6])
        implica = t.get("implicacion_lcg", "")
        implica_html = ""
        if implica:
            implica_html = f'<div class="implica"><strong>Implicación LCG</strong><p>{html.escape(implica)}</p></div>'
        out.append(f"""<article class="theme">
    <h3>{html.escape(t.get("titulo", ""))}</h3>
    <div class="t-meta">{sectors}{dates}</div>
    <p>{html.escape(t.get("explicacion", ""))}</p>
    {implica_html}
</article>""")
    return f'<div class="themes">{"".join(out)}</div>'


def render_actores(actores: list[dict]) -> str:
    if not actores:
        return '<p class="meta">Sin actores específicos identificados en los extractos.</p>'
    out = []
    # Sort: CRM first
    sorted_actors = sorted(actores, key=lambda a: (not a.get("en_crm", False), a.get("nombre", "")))
    for a in sorted_actors:
        crm_class = "crm" if a.get("en_crm") else ""
        out.append(f"""<div class="actor {crm_class}">
    <h4>{html.escape(a.get("nombre", ""))}</h4>
    <div class="a-row"><span class="a-label">Movimiento</span>{html.escape(a.get("movimiento", ""))}</div>
    <div class="a-row"><span class="a-label">Qué revela</span>{html.escape(a.get("que_revela", ""))}</div>
    <div class="a-row"><span class="a-label">Approach sugerido</span>{html.escape(a.get("approach_sugerido", ""))}</div>
</div>""")
    return f'<div class="actores">{"".join(out)}</div>'


def render_oportunidades(oport: list[dict]) -> str:
    if not oport:
        return '<p class="meta">No se identificaron oportunidades específicas con la evidencia disponible.</p>'
    # Sort by urgencia: alta → media → baja
    order = {"alta": 0, "media": 1, "baja": 2}
    sorted_o = sorted(oport, key=lambda o: order.get(o.get("urgencia", "media").lower(), 1))
    out = []
    for o in sorted_o:
        urg = o.get("urgencia", "media").lower()
        out.append(f"""<article class="opp">
    <div class="o-main">
        <span class="o-tipo">{html.escape(o.get("tipo", "").upper())}</span>
        <h3>{html.escape(o.get("titulo", ""))}</h3>
        <div class="o-grid">
            <div class="o-row"><span class="o-label">Evidencia (Whitepaper)</span>{html.escape(o.get("que_dice_el_extracto", ""))}</div>
            <div class="o-row"><span class="o-label">Cómo acercarse</span>{html.escape(o.get("como_acercarse", ""))}</div>
            <div class="o-row"><span class="o-label">Pretexto comercial</span>{html.escape(o.get("pretexto", ""))}</div>
        </div>
    </div>
    <div class="o-urg {urg}">
        <span class="l">Urgencia</span>
        <span class="v">{html.escape(urg.upper())}</span>
    </div>
</article>""")
    return f'<div class="oport">{"".join(out)}</div>'


def render_alertas(alertas: list[dict]) -> str:
    if not alertas:
        return '<p class="meta">Sin alertas significativas detectadas.</p>'
    items = "".join(
        f'<li><strong>{html.escape(a.get("titulo", ""))}</strong>{html.escape(a.get("descripcion", ""))}</li>'
        for a in alertas
    )
    return f'<ul class="list-alerts">{items}</ul>'


def render_gaps(gaps: list[str]) -> str:
    if not gaps:
        return '<p class="meta">El intel de Whitepaper cubre bien este estado.</p>'
    items = "".join(f'<li>{html.escape(g)}</li>' for g in gaps)
    return f'<ul class="list-gaps">{items}</ul>'


def render_excerpts(excerpts: list[dict], max_n: int = 15) -> str:
    """Lista compacta de extractos como evidencia, cap a max_n."""
    if not excerpts:
        return '<p class="meta">Sin extractos disponibles.</p>'
    items = []
    for ex in excerpts[:max_n]:
        text = html.escape(ex.get("text", ""))
        if len(text) > 500:
            text = text[:480] + "…"
        items.append(f"""<article class="excerpt">
    <div class="ex-date">{html.escape(ex.get("date", ""))}
        <small>{html.escape(ex.get("subtitle", "")[:55])}</small>
    </div>
    <div class="ex-body">
        <p>{text}</p>
        <a class="ex-link" href="{html.escape(ex.get("url", ""))}" target="_blank">Abrir post</a>
    </div>
</article>""")
    more_note = ""
    if len(excerpts) > max_n:
        more_note = f'<p class="meta" style="margin-top: 24px;">+ {len(excerpts) - max_n} extractos adicionales en el dataset raw (output/intel/state-{{slug}}.json).</p>'
    return f'<div class="excerpts">{"".join(items)}</div>{more_note}'


def render_state_page(state: str, data: dict, analysis: dict) -> str:
    slug = slugify(state)
    crm = data.get("crm_context", CRM_DATA.get(state, {}))

    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>{html.escape(state)} · Inteligencia Comercial · LCG</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="styles.css">
</head><body>
{chrome_header(active='zona')}
<main>
    <span class="eyebrow">Inteligencia comercial · Zona Sur-Centro-Golfo</span>
    <h1 class="hero">{html.escape(state)}.</h1>
    <p class="meta">{html.escape(crm.get("industries", ""))}</p>

    {render_exec_banner(slug)}

    <div class="state-toc">
        <a href="#pulso">Pulso</a>
        <a href="#temas">Temas dominantes</a>
        <a href="#actores">Actores clave</a>
        <a href="#oportunidades">Oportunidades LCG</a>
        <a href="#alertas">Alertas</a>
        <a href="#gaps">Gaps de investigación</a>
        <a href="#evidencia">Extractos</a>
    </div>

    <div class="stats">
        <div class="stat"><span class="num">{crm.get("aaa_aa", 0)}</span><span class="label">AAA+AA CRM</span></div>
        <div class="stat"><span class="num">{crm.get("dm", 0)}</span><span class="label">Decision makers</span></div>
        <div class="stat"><span class="num">{data["stats"]["total_excerpts"]}</span><span class="label">Extractos Whitepaper</span></div>
        <div class="stat"><span class="num">{data["stats"]["ppt_families_hit"]}/{data["stats"]["ppt_families_total"]}</span><span class="label">Familias PPT mencionadas</span></div>
        <div class="stat"><span class="num">{len(analysis.get("themes", []))}</span><span class="label">Temas dominantes</span></div>
        <div class="stat"><span class="num">{len(analysis.get("oportunidades_lcg", []))}</span><span class="label">Oportunidades LCG</span></div>
    </div>

    <h2 class="section" id="pulso">Pulso <em>del estado</em></h2>
    {render_pulso(analysis.get("pulso", ""))}

    <h2 class="section" id="temas">Temas <em>dominantes</em></h2>
    {render_themes(analysis.get("themes", []))}

    <h2 class="section" id="actores">Actores <em>clave</em></h2>
    <p class="meta">Tarjetas con borde verde = están en el CRM AAA/AA del PPT. Tarjetas con etiqueta «NUEVO» = leads detectados que no están en el PPT.</p>
    {render_actores(analysis.get("actores_clave", []))}

    <h2 class="section" id="oportunidades">Oportunidades <em>para LCG</em></h2>
    <p class="meta">Ordenadas por urgencia (alta primero). Cada una con pretexto comercial y vía sugerida de acercamiento.</p>
    {render_oportunidades(analysis.get("oportunidades_lcg", []))}

    <h2 class="section" id="alertas">Alertas <em>a vigilar</em></h2>
    {render_alertas(analysis.get("alertas", []))}

    <h2 class="section" id="gaps">Gaps de <em>investigación</em></h2>
    <p class="meta">Lo que Whitepaper NO cubre y donde LCG debería complementar con investigación primaria, fuentes locales o entrevistas.</p>
    {render_gaps(analysis.get("gaps", []))}

    <h2 class="section" id="evidencia">Extractos <em>textuales</em> (evidencia)</h2>
    <p class="meta">Párrafos exactos de posts de Whitepaper donde aparece el estado o una familia del CRM. Orden cronológico inverso.</p>
    {render_excerpts(data.get("excerpts", []))}

</main>
{chrome_footer()}
</body></html>"""


def render_zona_overview(state_intels: list[dict]) -> str:
    cards = []
    for entry in state_intels:
        state = entry["state"]
        slug = slugify(state)
        a = entry["analysis"]
        d = entry["data"]
        themes_count = len(a.get("themes", []))
        actores_count = len(a.get("actores_clave", []))
        oport_count = len(a.get("oportunidades_lcg", []))
        urg_alta = sum(1 for o in a.get("oportunidades_lcg", []) if o.get("urgencia", "").lower() == "alta")
        pulso_short = (a.get("pulso", "") or "")[:240]
        pulso_short = re.sub(r"\s+", " ", pulso_short).strip()
        if len(a.get("pulso", "")) > 240:
            pulso_short += "…"
        cards.append(f"""<a class="state-card" href="estado-{slug}.html" style="padding: 28px 28px;">
    <h3 class="state-name">{html.escape(state)}</h3>
    <p style="font-size:13px; line-height:1.55; color:var(--lcg-ink); margin: 8px 0 14px 0;">{html.escape(pulso_short)}</p>
    <div class="state-stats">
        <strong>{themes_count}</strong> temas ·
        <strong>{actores_count}</strong> actores ·
        <strong>{oport_count}</strong> oport. ({urg_alta} alta)
    </div>
</a>""")

    total_themes = sum(len(e["analysis"].get("themes", [])) for e in state_intels)
    total_actores = sum(len(e["analysis"].get("actores_clave", [])) for e in state_intels)
    total_oport = sum(len(e["analysis"].get("oportunidades_lcg", [])) for e in state_intels)
    total_urg_alta = sum(1 for e in state_intels for o in e["analysis"].get("oportunidades_lcg", []) if o.get("urgencia", "").lower() == "alta")

    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>Zona Sur-Centro-Golfo · Inteligencia Comercial · LCG</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="styles.css">
</head><body>
{chrome_header(active='zona')}
<main>
    <span class="eyebrow">Iniciativa comercial · 10 estados (zona consolidada)</span>
    <h1 class="hero">Zona <em>Sur-Centro-Golfo</em>.</h1>
    <p class="meta">Inteligencia comercial sintetizada desde 247 posts de Whitepaper.mx (mayo 2025 → mayo 2026). Cada estado tiene su propio análisis narrativo: pulso, temas dominantes, actores en movimiento, oportunidades para LCG, alertas y gaps de investigación.</p>

    <div class="stats">
        <div class="stat"><span class="num">10</span><span class="label">Estados</span></div>
        <div class="stat"><span class="num">{total_themes}</span><span class="label">Temas identificados</span></div>
        <div class="stat"><span class="num">{total_actores}</span><span class="label">Actores clave</span></div>
        <div class="stat"><span class="num">{total_oport}</span><span class="label">Oportunidades LCG</span></div>
        <div class="stat"><span class="num">{total_urg_alta}</span><span class="label">Urgencia ALTA</span></div>
    </div>

    <h2 class="section">Estados</h2>
    <p class="meta">Cada tarjeta resume el pulso del estado. Click para abrir el análisis completo.</p>
    <div class="state-grid">{''.join(cards)}</div>
</main>
{chrome_footer()}
</body></html>"""


def render_index(state_intels: list[dict]) -> str:
    state_cards = []
    for e in state_intels:
        state = e["state"]
        slug = slugify(state)
        urg_alta = sum(1 for o in e["analysis"].get("oportunidades_lcg", []) if o.get("urgencia", "").lower() == "alta")
        state_cards.append(f'<a class="state-card" href="estado-{slug}.html"><h3 class="state-name">{html.escape(state)}</h3><div class="state-stats"><strong>{len(e["analysis"].get("themes", []))}</strong> temas · <strong>{len(e["analysis"].get("oportunidades_lcg", []))}</strong> oport ({urg_alta} alta)</div></a>')

    return f"""<!DOCTYPE html>
<html lang="es-MX"><head><meta charset="UTF-8">
<title>Whitepaper Intelligence · LCG</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="styles.css">
</head><body>
{chrome_header(active='inicio')}
<main>
    <span class="eyebrow">London Consulting Group · Market Intelligence</span>
    <h1 class="hero">Whitepaper, <em>Hoy</em>.</h1>
    <p class="meta">Inteligencia comercial sintética de Whitepaper.mx para la iniciativa Zona Sur-Centro-Golfo · 247 posts · análisis narrativo por estado · Mayo 2025 → Mayo 2026</p>

    <div class="menu-grid">
        <a class="menu-card" href="zona.html">
            <h3>Zona Sur-Centro-Golfo</h3>
            <p>10 estados · análisis comercial completo por estado: pulso, temas dominantes, actores en movimiento, oportunidades para LCG, alertas, gaps de investigación y extractos textuales.</p>
            <span class="arrow">Inteligencia por estado</span>
        </a>
        <a class="menu-card" href="categorias.html">
            <h3>Por categoría</h3>
            <p>247 posts taggeados por 14 sectores y 10 tipos de evento. Para encontrar todos los posts sobre M&A, automotriz, fintech, etc. en toda la zona.</p>
            <span class="arrow">Inteligencia transversal</span>
        </a>
        <a class="menu-card" href="brief.html">
            <h3>Brief consolidado</h3>
            <p>247 posts en orden cronológico para lectura secuencial o exportación a PDF.</p>
            <span class="arrow">Documento completo</span>
        </a>
    </div>

    <h2 class="section">Estados <em>de la zona</em></h2>
    <p class="meta">Acceso directo a la inteligencia comercial de cada estado.</p>
    <div class="state-grid">{''.join(state_cards)}</div>
</main>
{chrome_footer()}
</body></html>"""


# ========================================================================
# MAIN
# ========================================================================

def main():
    print("="*72)
    print("RENDER v3 — Páginas por estado con análisis narrativo")
    print("="*72)

    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)

    state_intels = []
    for state in ZONA_ESTADOS:
        slug = slugify(state)
        data_path = INTEL_DIR / f"state-{slug}.json"
        analysis_path = INTEL_DIR / f"analysis-{slug}.json"
        if not data_path.exists() or not analysis_path.exists():
            print(f"  ✗ {state}: falta {data_path.name} o {analysis_path.name}")
            continue
        data = json.loads(data_path.read_text(encoding="utf-8"))
        analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        state_intels.append({"state": state, "data": data, "analysis": analysis})

        page = render_state_page(state, data, analysis)
        out_path = DOCS / f"estado-{slug}.html"
        out_path.write_text(page, encoding="utf-8")
        n_themes = len(analysis.get("themes", []))
        n_actores = len(analysis.get("actores_clave", []))
        n_oport = len(analysis.get("oportunidades_lcg", []))
        print(f"  ✓ {state:20s} → estado-{slug}.html  ({n_themes}t · {n_actores}a · {n_oport}o)")

    # Zona overview
    (DOCS / "zona.html").write_text(render_zona_overview(state_intels), encoding="utf-8")
    print(f"  ✓ zona.html")

    # Index
    (DOCS / "index.html").write_text(render_index(state_intels), encoding="utf-8")
    print(f"  ✓ index.html")

    # CSS (combinado state_intel + extras)
    (DOCS / "styles.css").write_text(CSS + EXTRA_CSS, encoding="utf-8")
    print(f"  ✓ styles.css")

    # Copy brief / categorias from output/
    for name in ["brief.html", "categorias.html"]:
        src = OUT / name
        if src.exists():
            shutil.copy(src, DOCS / name)
            print(f"  ✓ {name} (copiado desde output/)")

    print("="*72)
    print(f"LISTO · docs/ con {len(list(DOCS.glob('*.html')))} páginas")


if __name__ == "__main__":
    main()
