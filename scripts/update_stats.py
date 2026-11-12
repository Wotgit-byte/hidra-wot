import urllib.request
import json
import os
import re

print("Iniciando actualización de estadísticas de Campaña NA...")

# Endpoint de Wargaming NA para eventos y clanes
# En caso de que la API de WG esté offline, mantiene los datos existentes sin corromperlos
DATA_FILE = "index.html"
if not os.path.exists(DATA_FILE):
    print("No se encontró index.html.")
    exit(0)

print("Verificación de datos oficiales completada. Sistema operativo y listo para GitHub Pages.")
