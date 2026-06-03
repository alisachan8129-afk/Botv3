import re
import time
import requests

_bin_cache: dict = {}
_cache_ts: dict  = {}
_CACHE_TTL = 3600

def lookup_bin(bin_number: str) -> dict | None:
    bin_number = re.sub(r'\D', '', (bin_number or ''))[:6]
    if len(bin_number) < 6:
        return None

    if (bin_number in _bin_cache and
            time.time() - _cache_ts.get(bin_number, 0) < _CACHE_TTL):
        return _bin_cache[bin_number]

    try:
        r = requests.get(
            f'https://bins.antipublic.cc/bins/{bin_number}',
            timeout=8
        )
        if r.status_code == 200:
            raw = r.json()
            if isinstance(raw, dict) and raw.get('brand'):
                _bin_cache[bin_number] = raw
                _cache_ts[bin_number]  = time.time()
                return raw
    except Exception:
        pass

    return None

def parse_bin_info(card_data: str) -> tuple:
    raw_bin = re.sub(r'\D', '', (card_data or '').split('|')[0])[:6]
    if not raw_bin:
        return '', '', ''

    data = lookup_bin(raw_bin)
    if not data:
        return raw_bin, 'Unknown', 'Unknown'

    brand  = (data.get('brand') or '').upper()
    btype  = (data.get('type')  or '').upper()
    level  = (data.get('level') or '').upper()
    issuer = (data.get('bank')  or 'Unknown').upper()

    c_name = (data.get('country_name') or data.get('country') or '').title()
    c_flag = data.get('country_flag') or ''

    parts = [raw_bin]
    if brand: parts.append(brand)
    if btype: parts.append(btype)
    if level: parts.append(level)
    bin_line = ' — '.join(parts)

    country_line = f'{c_name} {c_flag}'.strip() if (c_name or c_flag) else 'Unknown'

    return bin_line, issuer, country_line

def clear_cache():
    _bin_cache.clear()
    _cache_ts.clear()
