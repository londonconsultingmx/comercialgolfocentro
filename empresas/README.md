# Empresas

Carpeta para **fichas profundas de investigación de empresas**, en el formato establecido (estilo PI Group / Grupo TAFER).

## Cómo se llena esta carpeta

Esta carpeta **se llena bajo demanda**. Después de completar los estudios de estado y revisar quiénes son las empresas relevantes, Fray selecciona qué empresas merecen una ficha profunda y pide a Claude Code:

```
> Crea la ficha de la empresa "Liverpool" en empresas/001_liverpool/ siguiendo plantillas/TEMPLATE_EMPRESA.md y prompts/10_perfil_empresa/prompt.md
```

## Convención de nombres

- Carpeta por empresa: `<numero>_<nombre_normalizado>/`
- Ejemplos:
  - `001_liverpool/`
  - `002_volkswagen_mexico/`
  - `003_grupo_vales/`
  - `004_softys_de_mexico/`
- Nombres en minúsculas, sin acentos, separados con guiones bajos.

## Estructura de cada ficha

```
empresas/<numero>_<nombre>/
├── investigacion.md       # Ficha completa (9 secciones, formato PI Group)
├── resumen_ejecutivo.md   # One-pager (~600 palabras)
└── prompt.md              # Prompt específico de la empresa (opcional)
```

## Template

Ver `plantillas/TEMPLATE_EMPRESA.md` o copia local en `empresas/TEMPLATE_EMPRESA.md`.

## Referencias de calidad

- Ficha de **PI Group SA de CV** (proyecto raíz Claude del usuario) — es la referencia base
- Ficha de **Grupo TAFER & Villa Group** (proyecto previo `lcg-market-intelligence`)
