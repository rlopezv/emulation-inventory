# Prompt - Validate cross references

Valida consistencia entre documentos:

1. `docs/devices.md` → todos los dispositivos aparecen en `docs/distributions.md`.
2. `docs/software.md` → todo software usado en `docs/distributions.md` existe o está marcado como `[TODO]`.
3. `docs/systems.md` → los identificadores canónicos no se usan como nombres de carpetas salvo que se indique explícitamente.
4. No inventes datos: usa `[TODO]` o notas breves.
5. Devuelve una lista de inconsistencias y una propuesta de corrección por cada una.
