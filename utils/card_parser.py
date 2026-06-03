import re

_SEPS = ['|', ':', ',', '\t', '-', ' ']

def _norm_yy(yy: str) -> str | None:
    if not yy.isdigit():
        return None
    if len(yy) == 2:
        return yy
    if len(yy) == 4:
        return yy[2:]
    return None

def _norm_mm(mm: str) -> str | None:
    if not mm.isdigit():
        return None
    m = int(mm)
    if not 1 <= m <= 12:
        return None
    return str(m).zfill(2)

def _valid_cc(cc: str) -> bool:
    digits = re.sub(r'\s', '', cc)
    return digits.isdigit() and 13 <= len(digits) <= 19

def _valid_cvv(cvv: str) -> bool:
    return cvv.isdigit() and 3 <= len(cvv) <= 4

def _try_parts(parts: list[str]) -> str | None:
    parts = [p.strip() for p in parts if p.strip()]

    if len(parts) == 4:
        cc_raw, mm_raw, yy_raw, cvv = parts[0], parts[1], parts[2], parts[3]
        if '/' in mm_raw and yy_raw and _valid_cvv(cvv):
            sp = mm_raw.split('/', 1)
            mm_raw, yy_raw = sp[0], sp[1]
        cc = re.sub(r'\s', '', cc_raw)
        if not _valid_cc(cc): return None
        mm = _norm_mm(mm_raw)
        yy = _norm_yy(yy_raw)
        if not mm or not yy: return None
        if not _valid_cvv(cvv): return None
        return f"{cc}|{mm}|{yy}|{cvv}"

    if len(parts) == 3:
        cc_raw, exp_raw, cvv = parts[0], parts[1], parts[2]
        cc = re.sub(r'\s', '', cc_raw)
        if not _valid_cc(cc): return None
        if not _valid_cvv(cvv): return None
        if '/' in exp_raw:
            sp = exp_raw.split('/', 1)
            mm = _norm_mm(sp[0])
            yy = _norm_yy(sp[1])
            if mm and yy:
                return f"{cc}|{mm}|{yy}|{cvv}"
        return None

    return None

def parse_card(text: str) -> str | None:
    if not text:
        return None
    line = text.strip()
    if not line or line.startswith('#'):
        return None

    for sep in _SEPS:
        if sep not in line:
            continue
        parts = line.split(sep)
        result = _try_parts(parts)
        if result:
            return result

    m = re.match(
        r'^(\d[\d\s]{11,17}\d)'
        r'[\s|:,\-]+'
        r'(\d{1,2})[/\-](\d{2,4})'
        r'[\s|:,\-]+'
        r'(\d{3,4})$',
        line
    )
    if m:
        cc = re.sub(r'\s', '', m.group(1))
        mm = _norm_mm(m.group(2))
        yy = _norm_yy(m.group(3))
        cvv = m.group(4)
        if _valid_cc(cc) and mm and yy and _valid_cvv(cvv):
            return f"{cc}|{mm}|{yy}|{cvv}"

    return None

def parse_first_card(text: str) -> str | None:
    if not text:
        return None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        result = parse_card(line)
        if result:
            return result
        for token in line.split():
            result = parse_card(token)
            if result:
                return result
    return None

def parse_all_cards(text: str) -> list[str]:
    if not text:
        return []
    seen: dict[str, bool] = {}
    for line in text.replace('\r', '\n').splitlines():
        line = line.strip()
        if not line:
            continue
        result = parse_card(line)
        if result and result not in seen:
            seen[result] = True
    return list(seen.keys())
