import json
import os
import re
import time
import random
import string
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

_BASE_DIR       = ""
_ROOT_ADMIN_IDS = []
_GROUP_CHAT_ID  = None

def init(base_dir, root_admin_ids):
    global _BASE_DIR, _ROOT_ADMIN_IDS
    _BASE_DIR       = base_dir
    _ROOT_ADMIN_IDS = list(root_admin_ids)

def _path(filename):
    return os.path.join(_BASE_DIR, filename)

def load_admin_ids():
    fp = _path("admin_ids.json")
    if os.path.exists(fp):
        try:
            with open(fp, 'r') as f:
                data = json.load(f)
            if isinstance(data, list):
                return [int(x) for x in data if str(x).isdigit()]
            return [int(x) for x in (data.get("ids") or []) if str(x).isdigit()]
        except Exception:
            return []
    return []

def save_admin_ids(ids_list):
    with open(_path("admin_ids.json"), 'w') as f:
        json.dump({"ids": ids_list}, f, indent=2)

def get_admin_ids():
    return list(set(_ROOT_ADMIN_IDS + load_admin_ids()))

def is_admin(user_id):
    return user_id in get_admin_ids()

def add_admin_id(user_id):
    uid = int(user_id)
    if uid in _ROOT_ADMIN_IDS: return False
    ids = load_admin_ids()
    if uid in ids: return False
    ids.append(uid)
    save_admin_ids(ids)
    return True

def remove_admin_id(user_id):
    uid = int(user_id)
    if uid in _ROOT_ADMIN_IDS: return False, "Không thể xóa ROOT admin."
    ids = load_admin_ids()
    if uid not in ids: return False, "User không phải admin."
    ids.remove(uid)
    save_admin_ids(ids)
    return True, None

def _load_banned():
    fp = _path("banned.json")
    if os.path.exists(fp):
        try:
            with open(fp, 'r') as f:
                data = json.load(f)
            if isinstance(data, list):
                return set(int(x) for x in data if str(x).isdigit())
        except Exception:
            pass
    return set()

def _save_banned(banned_set):
    with open(_path("banned.json"), 'w') as f:
        json.dump(list(banned_set), f, indent=2)

_banned_cache = None

def _get_banned():
    global _banned_cache
    if _banned_cache is None:
        _banned_cache = _load_banned()
    return _banned_cache

def is_banned(user_id):
    return int(user_id) in _get_banned()

def ban_user(user_id):
    uid = int(user_id)
    banned = _get_banned()
    if uid in banned:
        return False
    banned.add(uid)
    _save_banned(banned)
    return True

def unban_user(user_id):
    uid = int(user_id)
    banned = _get_banned()
    if uid not in banned:
        return False
    banned.discard(uid)
    _save_banned(banned)
    return True

def load_users():
    fp = _path("users_v2.json")
    if os.path.exists(fp):
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_users(data):
    with open(_path("users_v2.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user(user_id):
    return load_users().get(str(user_id)) 

def register_user(user_id, username, first_name):
    data = load_users()
    uid  = str(user_id)
    if uid in data: return False
    tz_vn     = ZoneInfo("Asia/Ho_Chi_Minh")
    join_time = datetime.now(tz_vn).strftime("%d/%m/%y %H:%M:%S")
    data[uid] = {
        "user_id":    user_id,
        "username":   username   or "None",
        "first_name": first_name or "User",
        "credit":     100,
        "joined_at":  join_time,
    }
    save_users(data)
    return True

def add_credit(user_id, delta):
    data = load_users()
    uid  = str(user_id)
    if uid not in data: return 0
    current = max(0, data[uid].get("credit", 0))
    new_cr  = max(0, current + delta)
    data[uid]["credit"] = new_cr
    save_users(data)
    return new_cr

def deduct_credit_for_status(user_id, status):
    if is_admin(user_id): return
    status = (status or "").upper()
    if   status == "APPROVED": add_credit(user_id, -2)
    elif status == "DECLINED": add_credit(user_id, -1)
    elif status == "CHARGED":  add_credit(user_id, -3)

def load_shopify_data():
    fp = _path("shopify_data.json")
    if os.path.exists(fp):
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_shopify_data(data):
    with open(_path("shopify_data.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _get_user_shopify(user_id):
    data = load_shopify_data()
    uid  = str(user_id)
    if uid not in data:
        data[uid] = {"sites": [], "proxies": []}
        save_shopify_data(data)
    return data[uid]

def get_user_sites(user_id):
    return _get_user_shopify(user_id).get("sites", [])

def get_user_proxies(user_id):
    return _get_user_shopify(user_id).get("proxies", [])

def add_user_site(user_id, url):
    url = url.strip().rstrip('/')
    if not url.startswith('http'): url = 'https://' + url
    data = load_shopify_data()
    uid  = str(user_id)
    if uid not in data: data[uid] = {"sites": [], "proxies": []}
    if url not in data[uid]["sites"]:
        data[uid]["sites"].append(url)
        save_shopify_data(data)
        return True
    return False

def remove_user_site(user_id, idx_or_url):
    data = load_shopify_data()
    uid  = str(user_id)
    if uid not in data: return False
    sites = data[uid].get("sites", [])
    if isinstance(idx_or_url, int) or (isinstance(idx_or_url, str) and idx_or_url.isdigit()):
        idx = int(idx_or_url)
        if 1 <= idx <= len(sites):
            data[uid]["sites"].pop(idx - 1)
            save_shopify_data(data)
            return True
    else:
        if idx_or_url.strip() in sites:
            data[uid]["sites"].remove(idx_or_url.strip())
            save_shopify_data(data)
            return True
    return False

def parse_proxy_line(line):
    line = (line or "").strip()
    if not line or line.startswith('#'): return None
    if '@' in line:
        try:
            auth_host = line.split('://', 1)[1] if '://' in line else line
            auth, host_port = auth_host.rsplit('@', 1)
            user, passwd = auth.split(':', 1) if ':' in auth else (auth, '')
            hp = host_port.split(':')
            if len(hp) >= 2:
                return f"{hp[0]}:{hp[1]}:{user}:{passwd}" if passwd else f"{hp[0]}:{hp[1]}:{user}:"
        except Exception: pass
    parts = line.split(':')
    if len(parts) >= 4: return f"{parts[0]}:{parts[1]}:{parts[2]}:{':'.join(parts[3:])}"
    if len(parts) == 3: return f"{parts[0]}:{parts[1]}:{parts[2]}:"
    if len(parts) == 2: return f"{parts[0]}:{parts[1]}"
    return None

def add_user_proxies(user_id, proxy_lines):
    data = load_shopify_data()
    uid  = str(user_id)
    if uid not in data: data[uid] = {"sites": [], "proxies": []}
    added = []
    for ln in proxy_lines.replace('\n', ' ').split():
        p = parse_proxy_line(ln)
        if p and p not in data[uid]["proxies"]:
            data[uid]["proxies"].append(p)
            added.append(p)
    if added: save_shopify_data(data)
    return len(added), added

def remove_user_proxy(user_id, idx_or_proxy):
    data = load_shopify_data()
    uid  = str(user_id)
    if uid not in data: return False
    proxies = data[uid].get("proxies", [])
    if isinstance(idx_or_proxy, int) or (isinstance(idx_or_proxy, str) and idx_or_proxy.isdigit()):
        idx = int(idx_or_proxy)
        if 1 <= idx <= len(proxies):
            data[uid]["proxies"].pop(idx - 1)
            save_shopify_data(data)
            return True
    else:
        for i, p in enumerate(proxies):
            if idx_or_proxy in p or p in idx_or_proxy:
                data[uid]["proxies"].pop(i)
                save_shopify_data(data)
                return True
    return False

PROXY_CHECK_API = "https://api.ipify.org?format=json"

def _proxy_to_requests_dict(proxy_str):
    if not proxy_str or not proxy_str.strip(): return None
    p = proxy_str.strip()
    if p.startswith("http://") or p.startswith("https://"):
        u = p if p.startswith("http://") else "http://" + p.split("://", 1)[1]
        return {"http": u, "https": u}
    parts = p.split(':')
    if len(parts) >= 4:
        host, port, user, passwd = parts[0], parts[1], parts[2], ':'.join(parts[3:])
        auth = f"{user}:{passwd}" if (user or passwd) else None
        url  = f"http://{auth}@{host}:{port}" if auth else f"http://{host}:{port}"
    elif len(parts) == 2:
        url = f"http://{parts[0]}:{parts[1]}"
    else:
        return None
    return {"http": url, "https": url}

def _mask_proxy_display(proxy_str):
    if not proxy_str or len(proxy_str) < 10:
        return proxy_str[:4] + "***" if proxy_str else "—"
    s = proxy_str.strip()
    return s[:4] + "***" + s[-4:] if len(s) > 12 else s[:3] + "***"

def check_proxy_via_ip_api(proxy_str, timeout=15):
    try:
        px = _proxy_to_requests_dict(proxy_str)
        if not px: return None, False
        r  = requests.get(PROXY_CHECK_API, proxies=px, timeout=timeout)
        if r.status_code == 200:
            ip = r.json().get("ip", "")
            if ip: return ip, True
        return None, False
    except Exception:
        return None, False

def parse_duration(s):
    s = (s or "").strip().lower()
    if not s: return None
    m = re.match(r'^(\d+)(d|h|m|w)$', s)
    if not m: return None
    num, unit = int(m.group(1)), m.group(2)
    if unit == 'w': return num * 7 * 24 * 3600
    if unit == 'd': return num * 24 * 3600
    if unit == 'h': return num * 3600
    if unit == 'm': return num * 60
    return None
