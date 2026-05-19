#!/usr/bin/env python3
"""
========================================================================
EXTRACTOR DE POSTS - WHITEPAPER.MX
========================================================================
Descarga los posts del tag "hoy" del último año usando tu sesión de
Substack autenticada (cookie). Guarda cada post como Markdown + JSON.

Requisitos:
    pip install requests beautifulsoup4 markdownify python-dateutil

Uso:
    1. Obtén tu cookie de sesión (ver instrucciones en README)
    2. Pega el valor en SUBSTACK_SESSION_COOKIE abajo
    3. python extract_whitepaper.py

Salida:
    ./output/
        ├── index.json              # Catálogo maestro
        ├── index.csv               # Mismo catálogo en CSV
        └── posts/
            ├── 2025-05-20_titulo-slug.md
            ├── 2025-05-20_titulo-slug.json
            └── ...
========================================================================
"""

import json
import csv
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md_convert

# ========================================================================
# CONFIGURACIÓN — EDITA ESTO
# ========================================================================

# 1) Pega aquí el valor de tu cookie `substack.sid`
#    Cómo obtenerla:
#      - Abre whitepaper.mx en Chrome/Edge, ya logueado
#      - F12 → Application → Cookies → https://www.whitepaper.mx
#      - Copia el VALOR de la cookie llamada `substack.sid`
SUBSTACK_SESSION_COOKIE = "s%3AJTRHkcL8qz0g5XH6qghWXOjje__GdfU6.310zlu8JY868fNqHEshEP1BFqpIXuRYNtw7HgrBFwfY"
# 2) Rango de fechas a descargar (default: último año)
DATE_FROM = datetime.now(timezone.utc) - timedelta(days=365)
DATE_TO   = datetime.now(timezone.utc)

# 3) Tag a filtrar (la sección "Hoy" de Whitepaper)
TAG_SLUG  = "hoy"

# 4) Carpeta de salida
OUTPUT_DIR = Path("./output")

# 5) Throttling — sé amable con Substack (segundos entre requests)
DELAY_SECONDS = 1.0

# ========================================================================
# CONSTANTES DE LA API DE SUBSTACK
# ========================================================================

BASE_URL = "https://www.whitepaper.mx"
ARCHIVE_API = f"{BASE_URL}/api/v1/archive"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# ========================================================================
# UTILIDADES
# ========================================================================

def make_session() -> requests.Session:
    """Crea una sesión HTTP con la cookie de autenticación."""
    if "PEGA_AQUI" in SUBSTACK_SESSION_COOKIE:
        sys.exit(
            "ERROR: Configura SUBSTACK_SESSION_COOKIE con tu cookie real.\n"
            "Ver instrucciones al inicio del archivo."
        )

    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/html,*/*",
        "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
    })
    s.cookies.set("connect.sid", SUBSTACK_SESSION_COOKIE, domain="www.whitepaper.mx")
    return s


def slugify(text: str, max_len: int = 60) -> str:
    """Convierte texto a slug seguro para nombre de archivo."""
    text = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_len]


def fmt_date(iso: str) -> str:
    """ISO 8601 → YYYY-MM-DD."""
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")


# ========================================================================
# FASE 1 — CATÁLOGO: lista todos los posts del tag "hoy" en el rango
# ========================================================================

def fetch_catalog(session: requests.Session) -> list[dict]:
    """
    Pagina la API de archive de Substack para traer todos los posts del tag.
    La API responde con un array; offset=0,12,24,... hasta vaciar.
    """
    print(f"[1/3] Descargando catálogo del tag '{TAG_SLUG}'...")
    posts = []
    offset = 0
    limit = 12
    page = 0

    while True:
        page += 1
        params = {
            "sort": "new",
            "search": "",
            "offset": offset,
            "limit": limit,
        }
        # Si el endpoint soporta filtro por tag, lo agregamos
        url = f"{BASE_URL}/api/v1/archive"

        r = session.get(url, params=params, timeout=30)
        if r.status_code != 200:
            print(f"  ! Error HTTP {r.status_code} en página {page}")
            break

        try:
            batch = r.json()
        except ValueError:
            print(f"  ! Respuesta no-JSON en página {page}")
            break

        if not batch:
            print(f"  [página {page}] vacía → fin del catálogo")
            break

        # Filtrar por tag y por rango de fechas
        kept_in_page = 0
        for p in batch:
            post_date = datetime.fromisoformat(
                p.get("post_date", "").replace("Z", "+00:00")
            )

            # Si ya pasamos del rango inferior, paramos todo
            if post_date < DATE_FROM:
                print(f"  [página {page}] alcanzamos fecha límite ({DATE_FROM.date()})")
                return posts

            if post_date > DATE_TO:
                continue

            # Filtro por tag: el campo `postTags` trae lista de objetos {slug, name}
            tags = [t.get("slug") for t in (p.get("postTags") or [])]
            if TAG_SLUG and TAG_SLUG not in tags:
                continue

            posts.append({
                "id": p.get("id"),
                "slug": p.get("slug"),
                "url": f"{BASE_URL}/p/{p.get('slug')}",
                "title": p.get("title", "").strip(),
                "subtitle": p.get("subtitle", "").strip(),
                "post_date": p.get("post_date"),
                "date": fmt_date(p.get("post_date")),
                "audience": p.get("audience"),
                "tags": tags,
                "reactions": p.get("reactions"),
                "comment_count": p.get("comment_count"),
            })
            kept_in_page += 1

        print(f"  [página {page}] +{kept_in_page} posts (total acumulado: {len(posts)})")

        if len(batch) < limit:
            print(f"  [página {page}] última página")
            break

        offset += limit
        time.sleep(DELAY_SECONDS)

    return posts


# ========================================================================
# FASE 2 — CONTENIDO: descarga cada post y extrae el HTML del cuerpo
# ========================================================================

def fetch_post_body(session: requests.Session, post: dict) -> dict:
    """Descarga un post individual y extrae el cuerpo en HTML + Markdown."""
    last_err = None
    for attempt in range(4):
        try:
            r = session.get(post["url"], timeout=30)
            break
        except (requests.ConnectionError, requests.Timeout) as e:
            last_err = e
            time.sleep(2 ** attempt)
    else:
        return {**post, "error": f"network_error: {last_err}"}
    if r.status_code != 200:
        return {**post, "error": f"HTTP {r.status_code}"}

    soup = BeautifulSoup(r.text, "html.parser")

    # Detectar paywall: Substack inserta un div con clase "paywall" o similar
    paywall = soup.select_one(".paywall, [class*='paywall']")
    is_paywalled = paywall is not None

    # El cuerpo del post vive en div.body.markup o similar
    body = (
        soup.select_one("div.body.markup")
        or soup.select_one("div.available-content")
        or soup.select_one("article")
    )

    if not body:
        return {**post, "error": "no_body_found", "is_paywalled": is_paywalled}

    body_html = str(body)
    body_md = md_convert(body_html, heading_style="ATX").strip()

    # Sanity check: si el contenido es muy corto y vemos paywall, probablemente
    # la sesión no está autenticada para este post
    word_count = len(body_md.split())
    auth_ok = word_count > 200

    return {
        **post,
        "body_html": body_html,
        "body_md": body_md,
        "word_count": word_count,
        "is_paywalled": is_paywalled,
        "auth_ok": auth_ok,
        "error": None if auth_ok else "auth_failed_or_short_content",
    }


# ========================================================================
# FASE 3 — PERSISTENCIA: guarda índice + archivos por post
# ========================================================================

def save_index(posts: list[dict], out_dir: Path) -> None:
    """Guarda index.json y index.csv con metadata de todos los posts."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON completo
    (out_dir / "index.json").write_text(
        json.dumps(posts, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # CSV tabular
    if not posts:
        return

    fields = ["date", "title", "subtitle", "url", "slug", "audience",
              "word_count", "auth_ok", "is_paywalled", "error"]

    with open(out_dir / "index.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for p in posts:
            w.writerow({k: p.get(k, "") for k in fields})

    print(f"  → Índice guardado: {out_dir/'index.json'} y {out_dir/'index.csv'}")


def save_post(post: dict, posts_dir: Path) -> None:
    """Guarda un post en Markdown + JSON."""
    posts_dir.mkdir(parents=True, exist_ok=True)
    base = f"{post['date']}_{slugify(post['title'] or post['slug'])}"

    # Markdown legible
    md_lines = [
        f"# {post['title']}",
        "",
        f"> {post['subtitle']}",
        "",
        f"**Fecha:** {post['date']}  ",
        f"**URL:** {post['url']}  ",
        f"**Word count:** {post.get('word_count', 0)}",
        "",
        "---",
        "",
        post.get("body_md", "*[contenido no disponible]*"),
    ]
    (posts_dir / f"{base}.md").write_text("\n".join(md_lines), encoding="utf-8")

    # JSON con todo (útil para procesamiento posterior por Claude)
    payload = {k: v for k, v in post.items() if k != "body_html"}
    (posts_dir / f"{base}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ========================================================================
# MAIN
# ========================================================================

def main():
    print("="*72)
    print("WHITEPAPER.MX — Extractor de posts (tag: hoy)")
    print(f"Rango: {DATE_FROM.date()} → {DATE_TO.date()}")
    print("="*72)

    session = make_session()

    # FASE 1: catálogo
    catalog = fetch_catalog(session)
    print(f"\n[2/3] {len(catalog)} posts en el catálogo")

    if not catalog:
        print("No hay posts para procesar. ¿Cookie inválida? ¿Rango vacío?")
        return

    save_index(catalog, OUTPUT_DIR)

    # FASE 2: contenido de cada post
    print(f"\n[3/3] Descargando contenido de {len(catalog)} posts...")
    posts_dir = OUTPUT_DIR / "posts"
    enriched = []
    fail_count = 0

    for i, post in enumerate(catalog, 1):
        print(f"  [{i:3d}/{len(catalog)}] {post['date']} · {post['title'][:50]}...", end=" ")

        # Resume: si el .json ya existe con contenido válido, lo cargamos y skip
        base = f"{post['date']}_{slugify(post['title'] or post['slug'])}"
        existing = posts_dir / f"{base}.json"
        if existing.exists():
            try:
                cached = json.loads(existing.read_text(encoding="utf-8"))
                if cached.get("auth_ok") and not cached.get("error"):
                    enriched.append(cached)
                    print(f"⤷ cached ({cached.get('word_count', 0)} palabras)")
                    continue
            except Exception:
                pass

        full = fetch_post_body(session, post)
        save_post(full, posts_dir)
        enriched.append(full)

        if full.get("error"):
            fail_count += 1
            print(f"⚠ {full['error']}")
        else:
            print(f"✓ ({full.get('word_count', 0)} palabras)")

        time.sleep(DELAY_SECONDS)

    # Re-guardar el índice con metadata enriquecida (word_count, errores, etc.)
    save_index(enriched, OUTPUT_DIR)

    print("\n" + "="*72)
    print(f"LISTO: {len(enriched) - fail_count}/{len(enriched)} posts descargados OK")
    print(f"Fallidos: {fail_count}")
    print(f"Archivos en: {OUTPUT_DIR.resolve()}")
    print("="*72)


if __name__ == "__main__":
    main()
