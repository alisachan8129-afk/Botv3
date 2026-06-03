import html
from utils import icons as ic
from utils.bin_api import parse_bin_info

def _bin(card: str) -> str:
    b, iss, ctr = parse_bin_info(card)
    return ic.premium_emoji(
        f"😁 <b>𝐁𝐈𝐍 𝐈𝐧𝐟𝐨</b>\n"
        f"<pre>"
        f"𝘽𝙧𝙖𝙣𝙙: {html.escape(b   or 'N/A')}\n"
        f"𝘽𝙖𝙣𝙠: {html.escape(iss or 'N/A')}\n"
        f"𝘾𝙤𝙪𝙣𝙩𝙧𝙮: {html.escape(ctr or 'N/A')}"
        f"</pre>\n"
    )

def _foot(uid: int, name: str, role: str) -> str:
    return ic.premium_emoji(
        f"🥶 <b>𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆</b> 🐰 <a href='tg://user?id={uid}'>{name}</a>\n"
    )

def processing(card: str, gate_label: str) -> str:
    return ic.processing_msg(card, gate_label)

def chk(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gatewat = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gatewat}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def ad(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗔𝘆𝗱𝗲𝗻 𝗔𝘂𝘁𝗵"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def pp(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗣𝗮𝘆𝗣𝗮𝗹 𝟭$"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def pp2(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗣𝗮𝘆𝗣𝗮𝗹 𝟭$ 𝟮"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def sq(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗦𝗾𝘂𝗮𝗿𝗲 𝟭$"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def au(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵 𝟮"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def b3(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗕𝗿𝗮𝗶𝗻𝘁𝗿𝗲𝗲 𝗔𝘂𝘁𝗵"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def vbv(card: str, status: str, resp: str, is_3ds: bool, uid: int, name: str, role: str) -> str:
    gateway  = "𝗩𝗕𝗩 𝗟𝗼𝗼𝗸𝘂𝗽 𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲"
    st       = ic.get_status(status)
    if is_3ds is None:
        tds_line = ""
    elif is_3ds:
        tds_line = "💋 <b>𝟯𝗗𝗦 🫠 </b> 𝗧𝗿𝘂𝗲 (𝗩𝗕𝗩)\n"
    else:
        tds_line = "☯️ <b>𝟯𝗗𝗦 🫠 </b> 𝗙𝗮𝗹𝘀𝗲 (𝗡𝗼𝗻-𝗩𝗕𝗩)\n"
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{tds_line}"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def stccn(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗖𝗡 𝟯$"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def mchk_processing(total: int) -> str:
    return ic.premium_emoji(
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>⚡💠 𝐌𝐚𝐬𝐬 𝐒𝐭𝐫𝐢𝐩𝐞 𝗔𝘂𝘁𝗵 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠...</b>\n"
        f"<blockquote>🤤 𝗧𝗼𝘁𝗮𝗹: {total}</blockquote>\n"
        f"<blockquote>✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱: 0\n"
        f"❌ 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱: 0</blockquote>\n"
        f"<blockquote>📊 𝗖𝗵𝗲𝗰𝗸𝗲𝗱: 0/{total}</blockquote>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>"
    )

def mchk_progress(total: int, approved: int, declined: int, checked: int, m: int, sec: int) -> str:
    return ic.premium_emoji(
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>⚡💠 𝐌𝐚𝐬𝐬 𝐒𝐭𝐫𝐢𝐩𝐞 𝗔𝘂𝘁𝗵 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠...</b>\n"
        f"<blockquote>🤤 𝗧𝗼𝘁𝗮𝗹: {total}</blockquote>\n"
        f"<blockquote>✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱: {approved}\n"
        f"❌ 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱: {declined}</blockquote>\n"
        f"<blockquote>📊 𝗖𝗵𝗲𝗰𝗸𝗲𝗱: {checked}/{total}</blockquote>\n"
        f"<blockquote>⏱️ 𝗧𝗶𝗺𝗲: {m}𝗺 {sec}𝘀</blockquote>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>"
    )

def mchk_hit(card: str, resp: str, uid: int, name: str) -> str:
    return ic.premium_emoji(
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>🌱 𝐇𝐢𝐭 𝐅𝐨𝐮𝐧𝐝!</b>\n"
        f"<blockquote>✅ 𝗦𝘁𝗮𝘁𝘂𝘀: 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝</blockquote>\n"
        f"<blockquote>💳 𝗖𝗮𝗿𝗱: <code>{html.escape(card)}</code></blockquote>\n"
        f"<blockquote>😭 𝗚𝗮𝘁𝗲𝘄𝗮𝘆: 𝐒𝐭𝐫𝐢𝐩𝐞 𝗔𝘂𝘁𝗵</blockquote>\n"
        f"<blockquote>📝 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: <b>{html.escape(resp)}</b></blockquote>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"{_bin(card)}"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"{_foot(uid, name, '👤 User')}"
    )

def st(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗦𝘁𝗿𝗶𝗽𝗲 𝟭.𝟭$"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def ch(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗦𝘁𝗿𝗶𝗽𝗲 𝟭$"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def mch_processing(total: int) -> str:
    return ic.premium_emoji(
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>⚡💠 𝐌𝐚𝐬𝐬 𝐒𝐭𝐫𝐢𝐩𝐞 𝟏$ 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠...</b>\n"
        f"<blockquote>🤤 𝗧𝗼𝘁𝗮𝗹: {total}</blockquote>\n"
        f"<blockquote>💸 𝗖𝗵𝗮𝗿𝗴𝗲𝗱: 0\n"
        f"🔐 𝟯𝗗𝗦: 0\n"
        f"❌ 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱: 0</blockquote>\n"
        f"<blockquote>📊 𝗖𝗵𝗲𝗰𝗸𝗲𝗱: 0/{total}</blockquote>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>"
    )

def mch_progress(total: int, charged: int, tds: int, declined: int, checked: int, m: int, sec: int) -> str:
    return ic.premium_emoji(
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>⚡💠 𝐌𝐚𝐬𝐬 𝐒𝐭𝐫𝐢𝐩𝐞 𝟏$ 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠...</b>\n"
        f"<blockquote>🤤 𝗧𝗼𝘁𝗮𝗹: {total}</blockquote>\n"
        f"<blockquote>💸 𝗖𝗵𝗮𝗿𝗴𝗲𝗱: {charged}\n"
        f"🔐 𝟯𝗗𝗦: {tds}\n"
        f"❌ 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱: {declined}</blockquote>\n"
        f"<blockquote>📊 𝗖𝗵𝗲𝗰𝗸𝗲𝗱: {checked}/{total}</blockquote>\n"
        f"<blockquote>⏱️ 𝗧𝗶𝗺𝗲: {m}𝗺 {sec}𝘀</blockquote>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>"
    )

def mch_hit(card: str, resp: str, uid: int, name: str) -> str:
    return ic.premium_emoji(
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>🌱 𝐇𝐢𝐭 𝐅𝐨𝐮𝐧𝐝!</b>\n"
        f"<blockquote>💸 𝗦𝘁𝗮𝘁𝘂𝘀: 𝐂𝐡𝐚𝐫𝐠𝐞𝐝</blockquote>\n"
        f"<blockquote>💳 𝗖𝗮𝗿𝗱: <code>{html.escape(card)}</code></blockquote>\n"
        f"<blockquote>😭 𝗚𝗮𝘁𝗲𝘄𝗮𝘆: 𝗦𝘁𝗿𝗶𝗽𝗲 𝟭$</blockquote>\n"
        f"<blockquote>📝 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: <b>{html.escape(resp)}</b></blockquote>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"{_bin(card)}"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"{_foot(uid, name, '👤 User')}"
    )

def zt(card: str, status: str, resp: str, uid: int, name: str, role: str) -> str:
    gateway = "𝗦𝘁𝗿𝗶𝗽𝗲 𝟱$"
    st = ic.get_status(status)
    return ic.premium_emoji(
        f"<b>{st}</b>\n\n"
        f"💳 <b>𝗖𝗮𝗿𝗱</b> 🫠 <code>{html.escape(card)}</code>\n"
        f"😭 <b>𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> 🫠 {gateway}\n"
        f"🙂‍↔️ <b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b> 🫠 <b>{html.escape(resp)}</b>\n"
        f"{ic.LINE}\n"
        f"{_bin(card)}"
        f"{ic.LINE}\n"
        f"{_foot(uid, name, role)}"
    )

def vbs(card: str, result: str, raw_status: str, enrolled, liability_shifted, liability_shift_possible, uid: int, name: str, role: str) -> str:
    _RESULT_ICONS = {
        "3DS_SUCCESS":        ("✅", "𝟯𝗗𝗦 𝗦𝘂𝗰𝗰𝗲𝘀𝘀"),
        "ENROLLED_CHALLENGE": ("🔐", "𝗘𝗻𝗿𝗼𝗹𝗹𝗲𝗱 𝗖𝗵𝗮𝗹𝗹𝗲𝗻𝗴𝗲"),
        "NOT_ENROLLED":       ("☯️", "𝗡𝗼𝘁 𝗘𝗻𝗿𝗼𝗹𝗹𝗲𝗱"),
        "3DS_FAILED":         ("❌", "𝟯𝗗𝗦 𝗙𝗮𝗶𝗹𝗲𝗱"),
        "UNKNOWN":            ("❓", "𝗨𝗻𝗸𝗻𝗼𝘄𝗻"),
        "ERROR":              ("⚠️", "𝗘𝗿𝗿𝗼𝗿"),
    }
    icon, label = _RESULT_ICONS.get(result, ("❓", html.escape(result)))
    enr_line  = f"<blockquote>🎫 𝗘𝗻𝗿𝗼𝗹𝗹𝗲𝗱: <b>{html.escape(str(enrolled))}</b></blockquote>\n" if enrolled is not None else ""
    ls_line   = f"<blockquote>🔄 𝗟𝗶𝗮𝗯𝗶𝗹𝗶𝘁𝘆 𝗦𝗵𝗶𝗳𝘁𝗲𝗱: <b>{'☯️ Yes' if liability_shifted else '💋 No'}</b></blockquote>\n" if liability_shifted is not None else ""
    lsp_line  = f"<blockquote>🔁 𝗦𝗵𝗶𝗳𝘁 𝗣𝗼𝘀𝘀𝗶𝗯𝗹𝗲: <b>{'☯️ Yes' if liability_shift_possible else '💋 No'}</b></blockquote>\n" if liability_shift_possible is not None else ""
    return ic.premium_emoji(
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>⚡💠 𝗩𝗕𝗩 𝐋𝐨𝐨𝐤𝐮𝐩 𝗔𝗽𝗶</b>\n"
        f"<blockquote>{icon} 𝗥𝗲𝘀𝘂𝗹𝘁: <b>{label}</b></blockquote>\n"
        f"<blockquote>💳 𝗖𝗮𝗿𝗱: <code>{html.escape(card)}</code></blockquote>\n"
        f"<blockquote>📝 𝗦𝘁𝗮𝘁𝘂𝘀: <b>{html.escape(raw_status)}</b></blockquote>\n"
        f"{enr_line}"
        f"{ls_line}"
        f"{lsp_line}"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"{_bin(card)}"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"{_foot(uid, name, role)}"
    )

