# Decisores

Carpeta para **perfiles individuales de personas clave** identificadas en los estudios de estado o de empresa.

## Cómo se llena esta carpeta

A petición de Fray, después de identificar a un decisor relevante en `estados/<estado>/06_ecosistema_decisores.md` o en una ficha de empresa.

```
> Crea el perfil de "José Carlos Azcárraga" en decisores/azcarraga_jose_carlos/ siguiendo plantillas/TEMPLATE_DECISOR.md y prompts/11_perfil_decisor/prompt.md
```

## Convención de nombres

- Carpeta por persona: `<apellido_paterno>_<nombre>/`
- En minúsculas, sin acentos, separado con guiones bajos
- Ejemplos:
  - `azcarraga_jose_carlos/`
  - `vales_familia/`  (cuando es una familia, no individuo)
  - `slim_carlos/`
  - `bailleres_alejandro/`

## Estructura

```
decisores/<apellido>_<nombre>/
└── perfil.md     # Perfil individual (one-pager)
```

## Template

Ver `plantillas/TEMPLATE_DECISOR.md` o copia local en `decisores/TEMPLATE_DECISOR.md`.

## Reglas

- **Solo información pública**: LinkedIn, notas de prensa, sitios corporativos, BMV/SEC
- **No publiques correos, celulares ni direcciones particulares**
- **No inventes** parentescos, edades o trayectorias
- **Lenguaje neutral**: no editorices estilos personales con calificativos cargados
