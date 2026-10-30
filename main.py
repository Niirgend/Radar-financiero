import time
import subprocess
import requests

def obtener_precios_en_vivo():
    # Crypto via CoinGecko API
    try:
        url_crypto = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
        res_c = requests.get(url_crypto, timeout=5).json()
        btc = res_c.get('bitcoin', {}).get('usd', 'N/A')
        eth = res_c.get('ethereum', {}).get('usd', 'N/A')
    except Exception:
        btc, eth = "Err", "Err"

    # ASML via Yahoo Finance API
    try:
        url_asml = "https://query1.finance.yahoo.com/v8/finance/chart/ASML"
        headers = {"User-Agent": "Mozilla/5.0"}
        res_a = requests.get(url_asml, headers=headers, timeout=5).json()
        asml = round(res_a['chart']['result'][0]['meta']['regularMarketPrice'], 2)
    except Exception:
        asml = "Err"

    return btc, eth, asml

def actualizar_notificacion(btc, eth, asml):
    titulo = "📡 Radar Financiero — En Vivo"
    
    # Formateo de precios con comas para los miles
    btc_str = f"${btc:,}" if isinstance(btc, (int, float)) else str(btc)
    eth_str = f"${eth:,}" if isinstance(eth, (int, float)) else str(eth)
    asml_str = f"${asml}" if isinstance(asml, (int, float)) else str(asml)
    
    contenido = f"BTC: {btc_str} | ETH: {eth_str} | ASML: {asml_str}"
    
    cmd = [
        "termux-notification",
        "--id", "radar_live",
        "--title", titulo,
        "--content", contenido,
        "--ongoing",
        "--priority", "high"
    ]
    subprocess.run(cmd)

print("🚀 Iniciando servicio de notificaciones en vivo para el Radar...")
while True:
    btc, eth, asml = obtener_precios_en_vivo()
    actualizar_notificacion(btc, eth, asml)
    time.sleep(15)  # Actualiza cada 15 segundos automáticamente
