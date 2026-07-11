# Arcade Special

## Sistemas

| Carpeta       | Sistema          | Core RetroArch                     | Standalone       | Romset base        | Formato                         | BIOS           | Nota                             |
| ------------- | ---------------- | ---------------------------------- | ---------------- | ------------------ | ------------------------------- | -------------- | -------------------------------- |
| `neogeo/`     | Neo Geo MVS      | `fbneo`, `fbalpha`, `mame`         | MAME             | FBNeo / FBA / MAME | `.zip`                          | `neogeo.zip`   | Separarlo es muy práctico        |
| `cps1/`       | Capcom CPS-1     | `fbneo`, `fbalpha`, `mame`         | MAME             | FBNeo / FBA / MAME | `.zip`                          | No normalmente | Muy estable                      |
| `cps2/`       | Capcom CPS-2     | `fbneo`, `fbalpha`, `mame`         | MAME             | FBNeo / FBA / MAME | `.zip`                          | No normalmente | Muy estable                      |
| `cps3/`       | Capcom CPS-3     | `fbneo`, `mame`                    | MAME             | FBNeo / MAME       | `.zip` / `.zip` + CHD según set | A veces        | Más sensible a versión           |
| `cave/`       | Cave / CV1000    | `fbneo`, `mame`                    | MAME             | FBNeo / MAME       | `.zip`                          | No normalmente | Sensible a rendimiento/versiones |
| `daphne/`     | LaserDisc Daphne | variable / `hypseus` según sistema | Hypseus / Daphne | Daphne             | carpetas + vídeos               | Sí             | Estructura propia                |
| `singe/`      | Singe / Singe 2  | variable                           | Hypseus Singe    | Singe              | carpetas + scripts + vídeos     | Sí             | Estructura propia                |
| `naomi/`      | Sega NAOMI       | `flycast`                          | Flycast / DEMUL  | MAME / Flycast     | `.zip`, `.zip` + CHD            | Sí             | Mejor carpeta propia             |
| `naomi2/`     | Sega NAOMI 2     | `flycast`                          | Flycast / DEMUL  | MAME / Flycast     | `.zip`, `.zip` + CHD            | Sí             | Más exigente                     |
| `atomiswave/` | Sammy Atomiswave | `flycast`                          | Flycast / DEMUL  | MAME / Flycast     | `.zip`                          | Sí             | Muy recomendable separarlo       |

## Viabilidad

| Sistema       | RPi 3B+         | RPi 5 4GB     | Teclast T50       | Xiaomi Redmi Pad 2 |
| ------------- | --------------- | ------------- | ----------------- | ------------------ |
| `neogeo/`     | Excelente       | Excelente     | Excelente         | Excelente          |
| `cps1/`       | Excelente       | Excelente     | Excelente         | Excelente          |
| `cps2/`       | Excelente       | Excelente     | Excelente         | Excelente          |
| `cps3/`       | Parcial         | Excelente     | Excelente         | Excelente          |
| `cave/`       | Parcial         | Muy bueno     | Muy bueno         | Muy bueno          |
| `daphne/`     | Experimental    | Bueno         | Poco recomendable | Parcial            |
| `singe/`      | No              | Parcial/Bueno | Poco recomendable | Parcial            |
| `naomi/`      | No recomendable | Muy bueno     | Bueno             | Bueno/Muy bueno    |
| `naomi2/`     | No              | Parcial       | Parcial           | Parcial/Bueno      |
| `atomiswave/` | Muy limitado    | Muy bueno     | Bueno             | Bueno/Muy bueno    |
