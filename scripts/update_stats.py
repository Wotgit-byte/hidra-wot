import urllib.request, urllib.parse, json, http.cookiejar, os, re

print("Iniciando actualización nocturna oficial de Campaña NA...")

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

try:
    opener.open(urllib.request.Request('https://hemero.ru/en/na2026nov/results.php', headers=headers), timeout=10)
    all_clans = []
    
    for start in [0, 100]:
        params = {
            'draw': str(start + 1),
            'start': str(start),
            'length': '100',
            'search[value]': '',
            'search[regex]': 'false'
        }
        for i in range(13):
            params[f'columns[{i}][data]'] = str(i)
            params[f'columns[{i}][name]'] = ''
            params[f'columns[{i}][searchable]'] = 'true'
            params[f'columns[{i}][orderable]'] = 'true'
            params[f'columns[{i}][search][value]'] = ''
            params[f'columns[{i}][search][regex]'] = 'false'

        post_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://hemero.ru/en/na2026nov/results.php',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        data = urllib.parse.urlencode(params).encode('utf-8')
        req = urllib.request.Request('https://hemero.ru/en/na2026nov/data/res_ssp.php', data=data, headers=post_headers)
        resp = opener.open(req, timeout=15)
        res = json.loads(resp.read().decode('utf-8', errors='ignore'))
        all_clans.extend(res.get('data', []))

    print(f"Sincronizados exitosamente {len(all_clans)} clanes oficiales de NA.")
    # In case of successful pull, save cache
    with open('clans_live_cache.json', 'w', encoding='utf-8') as f:
        json.dump(all_clans, f, indent=2)
except Exception as e:
    print("Aviso de sincronización:", e)

print("Sistema operativo y listo.")
