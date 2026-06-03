OK        = "✅"
FAIL      = "❌"
CHARGED   = "🔥"
DS3       = "🔐"
WARN      = "⚠️"
LOADING   = "⏳"

DIAMOND   = "💎"
CROWN     = "👑"
SHIELD    = "🛡️"
KEY       = "🔑"
LOCK      = "🔒"
FIRE      = "🔥"
STAR      = "⭐️"
LIGHTNING = "⚡"
ROCKET    = "🚀"
CHART     = "📊"
MONEY     = "💰"
CARD      = "💳"
GLOBE     = "🌐"
INFO      = "ℹ️"
REFRESH   = "🔄"
TRASH     = "🗑️"
USER      = "👤"
BOT_IC    = "🤖"
GIFT      = "🎁"
TARGET    = "🎯"

LINE  = "━━━━━━━━━━━━━━━━━"
DOT   = "•"
ARR   = "↬"
SUB   = "⤷"
BULL  = "⊀"
BULL2 = "⌬"

STATUS_TEXT: dict[str, str] = {
    "APPROVED":           f"✅ 𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙",
    "CHARGED":            f"💸 𝘾𝙝𝙖𝙧𝙜𝙚𝙙",
    "DECLINED":           f"❌ 𝘿𝙚𝙘𝙡𝙞𝙣𝙚𝙙",
    "3DS":                f"🔐 𝟯𝘿𝙎 𝙍𝙚𝙦𝙪𝙞𝙧𝙚𝙙",
    "LIVE":               f"{OK} 𝙇𝙄𝙑𝙀",
    "DEAD":               f"{FAIL} 𝘿𝙀𝘼𝘿",
    "ERROR":              f"{WARN} 𝙀𝙧𝙧𝙤𝙧",
    "UNKNOWN":            f"{WARN} 𝙐𝙣𝙠𝙣𝙤𝙬𝙣",
    "NOT_ENROLLED":       f"{OK} 𝙉𝙤𝙩 𝙀𝙣𝙧𝙤𝙡𝙡𝙚𝙙",
    "3DS_SUCCESS":        f"{OK} 𝟯𝘿𝙎 𝙎𝙪𝙘𝙘𝙚𝙨𝙨",
    "ENROLLED_CHALLENGE": f"{FAIL} 𝙀𝙣𝙧𝙤𝙡𝙡𝙚𝙙 (𝘾𝙝𝙖𝙡𝙡𝙚𝙣𝙜𝙚)",
    "INSUFFICIENT_FUNDS": f"{OK} 𝙇𝙄𝙑𝙀 (𝙇𝙤𝙬 𝙁𝙪𝙣𝙙𝙨)",
    "INCORRECT_CVC":      f"{OK} 𝙇𝙄𝙑𝙀 𝘾𝘾𝙉",
    "ORDER_PLACED":       f"{CHARGED} 𝘾𝙃𝘼𝙍𝙂𝙀𝘿",
    "SITE_DEAD":          f"{WARN} 𝙎𝙞𝙩𝙚 𝘿𝙚𝙖𝙙",
    "NOT_FOUND":          f"🔍 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙",
}

def get_status(status: str) -> str:
    text = STATUS_TEXT.get(
        status.upper() if status else "ERROR",
        f"{WARN} {status or 'Error'}"
    )
    return premium_emoji(text)

def processing_msg(card: str, gate_label: str) -> str:
    text = (
        f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>\n"
        f"<b>⚡💠 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠...</b>\n"
        f"<blockquote>💳 𝗖𝗮𝗿𝗱: <code>{card}</code></blockquote>\n"
        f"<b>━━━━━━━━━━━━━━━━━</b>"
    )
    return premium_emoji(text)

_PREMIUM_IDS: dict[str, str] = {
    "⭐️": "5253922906378881072",
    "🎈": "5082413149873767213",
    "🔗": "5980995951160987855",
    "🙁": "5116275208906343429",
    "🛸": "5913264639025615311",
    "😓": "5852881749645728848",
    "👻": "6026243289890427139",
    "🐸": "5980995951160987855",
    "🥶": "5361563222132405424",
    "4️⃣": "5138822752123225428",
    "🐳": "5134201302888219205",
    "0️⃣": "5140999334174655345",
    "2️⃣": "5140871649091912628",
    "⏭️": "5125546965261618614",
    "⌛": "5161245668274079675",
    "🤤": "5971944878815317190",
    "⚡": "6026367225466720832",
    "⚠️": "5122871166276470097",
    "💠": "5971837723676249096",
    "✅": "5764701999429849874",
    "❌": "5273914604752216432",
    "😁": "5197304993920616826",
    "🫠": "4918408122868958076",
    "🥶": "6030656587830399914",
    "🐰": "5971895400792067820",
    "💳": "5472250091332993630",
    "😭": "5208611920529076518",
    "🙂‍↔️": "5363992034728229166",
    "🔐": "6181590577654534191",
    "💸": "5278223861404421915",
    "3️⃣": "5141399818400170896",
    "💰": "6033006935668692007",
    "📝": "6023660820544623088",
    "🎯": "5974235702701853774",
    "⏱️": "5274156304036800055",
    "🌱": "6147489559526513603",
    "📊": "5971837723676249096",
    "🦄": "6183982217308409507",
    "📌": "6237585097084638739",
    "🔄": "6181708264053412213",
    "1️⃣": "5141109049114232089",
    "5️⃣": "5141062672057369534",
    "💋": "6032903688949862892",
    "☯️": "6026257381678124710",
    "🔍": "6030594491193234103",
    "🛑": "6181468514683981841",
    "6️⃣": "5139005588881015916",
    "❓": "6183613451416375575",
    "🎫": "6181625057651987013",
    "🔁": "6181716209742909785"
}

def premium_emoji(text: str) -> str:
    if not text:
        return text
    placeholders = []
    result = text
    for i, (emoji, doc_id) in enumerate(_PREMIUM_IDS.items()):
        ph = f"\x00PE{i:02d}\x00"
        placeholders.append((ph, doc_id, emoji))
        result = result.replace(emoji, ph)
    for ph, doc_id, emoji in placeholders:
        result = result.replace(ph, f'<tg-emoji emoji-id="{doc_id}">{emoji}</tg-emoji>')
    return result
