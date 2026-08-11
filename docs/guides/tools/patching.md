# Parcheo

Aplicación de parches de traducción, hacks o bugfixes en formato IPS/BPS/xdelta sobre una ROM limpia (No-Intro/Redump) ya auditada (fase 3). El parche modifica una copia de la ROM original — la ROM base debe conservarse intacta, tanto por si hay que reaplicar el parche como porque el resultado parcheado no auditará contra el DAT original (ver Notas).

Corresponde a la fase 6 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

## Lunar IPS (LIPS)

**Fuente:** GUI clásica y ligera para Windows, formato IPS únicamente. Solo interfaz gráfica, sin CLI.

**Flujo confirmado para aplicar un parche:**

1. Abrir Lunar IPS.
2. **Apply IPS Patch**.
3. Seleccionar el fichero `.ips` → Open.
4. Seleccionar la ROM base a parchear → Open.
5. Mensaje de confirmación: *"The file was successfully patched"*.

**Notas prácticas:** hacer copia de la ROM base antes de parchear (el parche se aplica sobre el fichero seleccionado, no genera una copia nueva); si la ROM no aparece al navegar, cambiar el filtro del selector a "All Files". Renombrar el resultado para distinguirlo de la ROM limpia original.

## Flips (Floating IPS)

**Fuente:** github.com/Alcaro/Flips. Sucesor moderno de Lunar IPS — soporta IPS y BPS (genera los parches BPS más compactos conocidos, según su propia documentación). GUI (Windows y GTK+) y CLI, ambas en el mismo binario.

**GUI:** ejecutar el programa sin más — los selectores de fichero indican en el título qué se espera en cada paso. Soporta aplicar varios parches a la vez, recordar ROMs usadas recientemente y ejecutar un programa tras parchear.

**CLI confirmada:**

```bash
# Aplicar un parche
flips --apply patch.bps rom.smc hack.smc

# Crear un parche comparando ROM original y modificada
flips --create rom.smc hack.smc patch.bps
```

`--apply` necesita parche + ROM base + nombre de salida; `--create` necesita ROM original + ROM modificada + nombre del parche resultante. Ver `flips --help` para el resto de opciones.

## DeltaPatcher (xdelta)

**Fuente:** github.com/marco-calautti/DeltaPatcher. GUI multiplataforma (Windows/Linux, disponible también en Flathub) para crear y aplicar parches xdelta — pensada para ROMs pesadas (N64, PlayStation en adelante) donde IPS/BPS no son viables por límite de tamaño.

**Particularidad confirmada:** a diferencia de otras GUI que son solo un frontend del binario `xdelta3`, DeltaPatcher es autocontenido — no depende de tener `xdelta3` instalado aparte (todas las librerías necesarias van estáticamente enlazadas en el ejecutable).

**Uso:** arrastrar y soltar el fichero original y el parche `.xdelta` en la ventana de decodificación. Opciones disponibles: nivel de compresión, tamaño de ventana de origen, descripción del parche y verificación por checksum.

[TODO: no se ha encontrado un tutorial paso a paso oficial más detallado que el flujo de arrastrar-y-soltar — suficiente para uso básico, pero sin confirmar el detalle de las opciones avanzadas (nivel de compresión, ventana de origen)]

## Notas

**Verificar el resultado, no solo confiar en el parche:** tras aplicar cualquier parche, el hash de la ROM resultante ya no coincide con el DAT de origen (No-Intro/Redump) — es un fichero nuevo y distinto. Si existe un DAT de traducciones/hacks para el parche aplicado, verificar contra ese en vez de asumir que "aplicó sin error" equivale a "resultado correcto".

**Automatización futura de este paso:** ver la sección "Translated" del roadmap en [custom-pipeline.md](../romsets/custom-pipeline.md) — la idea evaluada es no almacenar la ROM ya parcheada, sino guardar la ROM limpia más una carpeta de parches y automatizar el parcheo en el pipeline (con `xdelta3` por CLI en el caso de xdelta, ya que DeltaPatcher aquí documentado es una GUI sin modo por lotes confirmado).
