# Maneuvers NA 2026 — Tracker Táctico Clan [HIDRA]

Portal de seguimiento táctico y consulta de rivales para el evento de Maniobras (Noviembre 2026) en el servidor de World of Tanks North America (NA).

## Características
1. **Ficha de Clan Táctica (Clan Info):**
   - Buscador rápido con autocompletado en tiempo real.
   - Puesto (Place), Puntos de Fama, Elo Fortaleza Tier X, Multiplicador/Premio.
   - Jugadores en el clan, jugadores en leaderboard, jugadores en tanque (corte diario superado) y WN8 medio.
   - Ventana **Cara a Cara vs [HIDRA]**: Balance histórico, victorias/derrotas, mapas jugados y comandantes.
2. **Puntos Personales (Personal Points):**
   - Roster de jugadores activos en el Callejón de la Fama.
   - Estado de tanque (`🟢 EN TANQUE` / `🔴 FUERA`), diferencia de puntos al corte (`+X pts`) y estadísticas individuales.
3. **Leaderboard General de NA:**
   - Tabla completa clasificatoria con salto directo a la ficha de cualquier rival.
4. **Sincronización Automática:**
   - Programada en GitHub Actions para ejecutarse a las 01:00, 02:00, 03:00, 04:00 y 05:00 CET.

## Cómo Publicar en GitHub Pages (`hidra-wot.github.io`)
1. Crea un repositorio en GitHub llamado `hidra-wot.github.io` (o cualquier nombre bajo tu cuenta).
2. Sube los archivos de esta carpeta (`index.html`, `.github/`, `scripts/`).
3. Ve a **Settings > Pages > Branch: `main` / Folder: `/ (root)` > Save**.
4. ¡Listo! La web estará activa y visible para todo el clan.
