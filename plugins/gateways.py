import asyncio
import html
import io
import re
import time

import utils.formats as fmt
from utils import icons as ic
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton

_mchk_sessions: dict = {}
_mch_sessions: dict = {}

def _mchk_stop_kb(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=" Stop",
            callback_data=f"mchk_stop_{uid}",
            style='danger',
            icon_custom_emoji_id='5116444615301399317',
        )]
    ])

def _mch_stop_kb(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=" Stop",
            callback_data=f"mch_stop_{uid}",
            style='danger',
            icon_custom_emoji_id='5116444615301399317',
        )]
    ])

async def _send(s_msg: Message, text: str):
    try:
        await s_msg.edit_text(text, disable_web_page_preview=True)
    except Exception:
        await s_msg.answer(text, disable_web_page_preview=True)

def setup(ctx) -> tuple:
    is_admin         = ctx['is_admin']
    parse_first_card = ctx['parse_first_card']
    parse_all_cards  = ctx['parse_all_cards']
    gates            = ctx['gates']
    bot              = ctx['bot']

    async def _pre(message: Message, cmd: str):
        uid   = message.from_user.id
        fname = html.escape(message.from_user.first_name or 'User')
        raw  = re.sub(r'^/' + re.escape(cmd) + r'(@\w+)?\s*',
                      '', (message.text or '').strip(), flags=re.IGNORECASE).strip()
        card = parse_first_card(raw)
        if not card and message.reply_to_message:
            card = parse_first_card(
                (message.reply_to_message.text
                 or message.reply_to_message.caption or '').strip())
        if not card:
            await message.reply(
                ic.premium_emoji(f"⚠️ <b>𝗨𝘀𝗮𝗴𝗲:</b> <code>/{cmd} cc|mm|yy|cvv</code>"))
            return None
        role = "👑 Admin" if is_admin(uid) else "👤 User"
        return card, fname, role, uid

    async def cmd_chk(message: Message):
        pre = await _pre(message, 'chk')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵'))
        res = await asyncio.to_thread(gates.stripe_auth, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.chk(card, status, resp, uid, name, role))

    async def cmd_ad(message: Message):
        pre = await _pre(message, 'ad')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗔𝘆𝗱𝗲𝗻 𝗔𝘂𝘁𝗵'))
        res = await asyncio.to_thread(gates.adyen_auth, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.ad(card, status, resp, uid, name, role))

    async def cmd_pp(message: Message):
        pre = await _pre(message, 'pp')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗣𝗮𝘆𝗣𝗮𝗹 𝟭$'))
        res = await asyncio.to_thread(gates.paypal_charge, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.pp(card, status, resp, uid, name, role))

    async def cmd_pp2(message: Message):
        pre = await _pre(message, 'pp2')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗣𝗮𝘆𝗣𝗮𝗹 𝟭$ 𝟮'))
        res = await asyncio.to_thread(gates.paypal_charge2, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.pp2(card, status, resp, uid, name, role))

    async def cmd_sq(message: Message):
        pre = await _pre(message, 'sq')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗦𝗾𝘂𝗮𝗿𝗲 𝟭$'))
        res = await asyncio.to_thread(gates.square_charge, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.sq(card, status, resp, uid, name, role))

    async def cmd_au(message: Message):
        pre = await _pre(message, 'au')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵 𝟮'))
        res = await asyncio.to_thread(gates.stripe_auth2, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.au(card, status, resp, uid, name, role))

    async def _notify_hit(uid, fname, card, resp):
        try:
            await bot.send_message(uid, fmt.mchk_hit(card, resp, uid, fname))
        except Exception:
            pass

    async def cb_mchk(call: CallbackQuery):
        data = call.data
        uid  = call.from_user.id
        if data.startswith('mchk_stop_'):
            target_uid = int(data[len('mchk_stop_'):])
            if uid != target_uid:
                await call.answer("❌ Not your session.", show_alert=True)
                return
            if uid in _mchk_sessions:
                _mchk_sessions[uid][0] = True
                await call.answer("🛑 Stopping...")
                try:
                    await call.message.edit_text(
                        ic.premium_emoji("🛑 <b>Stop signal sent. Finishing up...</b>"))
                except Exception:
                    pass
            else:
                await call.answer("Session not found.")

    async def cmd_mchk(message: Message):
        uid   = message.from_user.id
        fname = html.escape(message.from_user.first_name or 'User')

        if uid in _mchk_sessions:
            await message.reply(
                ic.premium_emoji("⚠️ <b>You already have a running session.</b>\n"
                                  "Press 🛑 Stop to cancel it first."))
            return

        doc = None
        if message.reply_to_message and message.reply_to_message.document:
            doc = message.reply_to_message.document
        elif message.document:
            doc = message.document
        if not doc:
            await message.reply(ic.premium_emoji(
                f"⚠️ <b>Reply to a .txt file with cards.</b>\n"
                f"📌 Max 1000 cards per run."))
            return
        if not (doc.file_name or '').lower().endswith('.txt'):
            await message.reply("⚠️ <b>Only .txt files accepted.</b>")
            return

        if doc.file_size > 2 * 1024 * 1024:
            await message.reply(ic.premium_emoji("⚠️ <b>File too large. Max 2MB.</b>"))
            return

        s = await message.reply(
            ic.premium_emoji("🔄 <b>Loading file...</b>"))
        
        try:
            file_bytes = await bot.download(doc)
            content    = file_bytes.read().decode('utf-8', errors='ignore')
            cards      = parse_all_cards(content)
        except Exception as e:
            await s.edit_text(ic.premium_emoji(f"❌ <b>Error loading file:</b> <code>{html.escape(str(e))}</code>"))
            return

        if not cards:
            await s.edit_text("❌ <b>No valid cards found.</b>")
            return
        cards = list(dict.fromkeys(cards))[:1000]
        total = len(cards)

        stopped = [False]
        _mchk_sessions[uid] = stopped
        stop_kb  = _mchk_stop_kb(uid)

        await s.edit_text(fmt.mchk_processing(total), reply_markup=stop_kb)

        approved   = []
        declined   = []
        checked    = [0]
        start_ts   = time.time()
        last_upd   = [time.time()]
        sem        = asyncio.Semaphore(5)

        async def _check_one(card):
            if stopped[0]:
                return
            async with sem:
                if stopped[0]:
                    return
                res    = await asyncio.to_thread(gates.freechk_stripe, card)
                if stopped[0]:
                    return
                status = res.get('status', '').upper()
                msg    = res.get('message', '')
                checked[0] += 1
                if status == 'APPROVED':
                    approved.append((card, msg))
                    asyncio.create_task(_notify_hit(uid, fname, card, msg))
                else:
                    declined.append((card, msg))
                now = time.time()
                if now - last_upd[0] >= 2.0:
                    last_upd[0] = now
                    el = int(now - start_ts)
                    m, sec = divmod(el, 60)
                    try:
                        await s.edit_text(fmt.mchk_progress(
                            total, len(approved), len(declined), checked[0], m, sec),
                            reply_markup=stop_kb)
                    except Exception:
                        pass

        await asyncio.gather(*[_check_one(c) for c in cards])
        _mchk_sessions.pop(uid, None)

        el = int(time.time() - start_ts)
        m, sec = divmod(el, 60)

        lines = []
        if approved:
            lines.append("=== APPROVED ===")
            for card, msg in approved:
                lines.append(f"{card} | {msg}" if msg else card)
        if declined:
            lines.append("=== DECLINED ===")
            for card, msg in declined:
                lines.append(f"{card} | {msg}" if msg else card)

        stopped_label = " (stopped)" if stopped[0] else ""
        buf     = io.BytesIO("\n".join(lines).encode('utf-8'))
        doc_out = BufferedInputFile(buf.getvalue(), filename=f"mchk_{uid}.txt")
        caption = (
            f"Mass Stripe Check{stopped_label}\n"
            f"Total: {total} | Approved: {len(approved)} | Declined: {len(declined)}\n"
            f"Time: {m}m {sec}s"
        )
        try:
            await s.delete()
        except Exception:
            pass
        try:
            await bot.send_document(uid, doc_out, caption=caption)
        except Exception:
            pass

    async def cmd_st(message: Message):
        pre = await _pre(message, 'st')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗦𝘁𝗿𝗶𝗽𝗲 𝟭.𝟭$'))
        res = await asyncio.to_thread(gates.stripe_1, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.st(card, status, resp, uid, name, role))

    async def cmd_ch(message: Message):
        pre = await _pre(message, 'ch')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗦𝘁𝗿𝗶𝗽𝗲 𝟭$'))
        res = await asyncio.to_thread(gates.stripe_1d, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.ch(card, status, resp, uid, name, role))

    async def _notify_mch_hit(uid, fname, card, resp):
        try:
            await bot.send_message(uid, fmt.mch_hit(card, resp, uid, fname))
        except Exception:
            pass

    async def cb_mch(call: CallbackQuery):
        data = call.data
        uid  = call.from_user.id
        if data.startswith('mch_stop_'):
            target_uid = int(data[len('mch_stop_'):])
            if uid != target_uid:
                await call.answer("❌ Not your session.", show_alert=True)
                return
            if uid in _mch_sessions:
                _mch_sessions[uid][0] = True
                await call.answer("🛑 Stopping...")
                try:
                    await call.message.edit_text(
                        ic.premium_emoji("🛑 <b>Stop signal sent. Finishing up...</b>"))
                except Exception:
                    pass
            else:
                await call.answer("Session not found.")

    async def cmd_mch(message: Message):
        uid   = message.from_user.id
        fname = html.escape(message.from_user.first_name or 'User')

        if uid in _mch_sessions:
            await message.reply(
                ic.premium_emoji("⚠️ <b>You already have a running session.</b>\n"
                                  "Press 🛑 Stop to cancel it first."))
            return

        doc = None
        if message.reply_to_message and message.reply_to_message.document:
            doc = message.reply_to_message.document
        elif message.document:
            doc = message.document
        if not doc:
            await message.reply(ic.premium_emoji(
                f"⚠️ <b>Reply to a .txt file with cards.</b>\n"
                f"📌 Max 1000 cards per run."))
            return
        if not (doc.file_name or '').lower().endswith('.txt'):
            await message.reply("⚠️ <b>Only .txt files accepted.</b>")
            return

        if doc.file_size > 2 * 1024 * 1024:
            await message.reply(ic.premium_emoji("⚠️ <b>File too large. Max 2MB.</b>"))
            return

        s = await message.reply(
            ic.premium_emoji("🔄 <b>Loading file...</b>"))
        
        try:
            file_bytes = await bot.download(doc)
            content    = file_bytes.read().decode('utf-8', errors='ignore')
            cards      = parse_all_cards(content)
        except Exception as e:
            await s.edit_text(ic.premium_emoji(f"❌ <b>Error loading file:</b> <code>{html.escape(str(e))}</code>"))
            return

        if not cards:
            await s.edit_text("❌ <b>No valid cards found.</b>")
            return
        cards = list(dict.fromkeys(cards))[:1000]
        total = len(cards)

        stopped  = [False]
        _mch_sessions[uid] = stopped
        stop_kb  = _mch_stop_kb(uid)

        await s.edit_text(fmt.mch_processing(total), reply_markup=stop_kb)

        charged_l  = []
        tds_l      = []
        declined_l = []
        checked    = [0]
        start_ts   = time.time()
        last_upd   = [time.time()]
        sem        = asyncio.Semaphore(5)

        async def _check_one(card):
            if stopped[0]:
                return
            async with sem:
                if stopped[0]:
                    return
                res    = await asyncio.to_thread(gates.stripe_1d, card)
                if stopped[0]:
                    return
                status = res.get('status', '').upper()
                msg    = res.get('message', '')
                checked[0] += 1
                if status == 'CHARGED':
                    charged_l.append((card, msg))
                    asyncio.create_task(_notify_mch_hit(uid, fname, card, msg))
                elif status == '3DS':
                    tds_l.append((card, msg))
                else:
                    declined_l.append((card, msg))
                now = time.time()
                if now - last_upd[0] >= 2.0:
                    last_upd[0] = now
                    el = int(now - start_ts)
                    m, sec = divmod(el, 60)
                    try:
                        await s.edit_text(fmt.mch_progress(
                            total, len(charged_l), len(tds_l), len(declined_l),
                            checked[0], m, sec),
                            reply_markup=stop_kb)
                    except Exception:
                        pass

        await asyncio.gather(*[_check_one(c) for c in cards])
        _mch_sessions.pop(uid, None)

        el = int(time.time() - start_ts)
        m, sec = divmod(el, 60)

        lines = []
        if charged_l:
            lines.append("=== CHARGED ===")
            for card, msg in charged_l:
                lines.append(f"{card} | {msg}" if msg else card)
        if tds_l:
            lines.append("=== 3DS ===")
            for card, msg in tds_l:
                lines.append(f"{card} | {msg}" if msg else card)
        if declined_l:
            lines.append("=== DECLINED ===")
            for card, msg in declined_l:
                lines.append(f"{card} | {msg}" if msg else card)

        stopped_label = " (stopped)" if stopped[0] else ""
        buf     = io.BytesIO("\n".join(lines).encode('utf-8'))
        doc_out = BufferedInputFile(buf.getvalue(), filename=f"mch_{uid}.txt")
        caption = (
            f"Mass Stripe 1${stopped_label}\n"
            f"Total: {total} | Charged: {len(charged_l)} | 3DS: {len(tds_l)} | Declined: {len(declined_l)}\n"
            f"Time: {m}m {sec}s"
        )
        try:
            await s.delete()
        except Exception:
            pass
        try:
            await bot.send_document(uid, doc_out, caption=caption)
        except Exception:
            pass

    async def cmd_vbv(message: Message):
        pre = await _pre(message, 'vbv')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗩𝗕𝗩 𝗟𝗼𝗼𝗸𝘂𝗽 𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲'))
        res = await asyncio.to_thread(gates.vbv_lookup, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        is_3ds = res.get('3ds', True)
        await _send(s, fmt.vbv(card, status, resp, is_3ds, uid, name, role))

    async def cmd_stccn(message: Message):
        pre = await _pre(message, 'stccn')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗖𝗡 𝟯$'))
        res = await asyncio.to_thread(gates.stripeccn, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.stccn(card, status, resp, uid, name, role))

    async def cmd_b3(message: Message):
        pre = await _pre(message, 'b3')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗕𝗿𝗮𝗶𝗻𝘁𝗿𝗲𝗲 𝗔𝘂𝘁𝗵'))
        res = await asyncio.to_thread(gates.braintree_auth, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.b3(card, status, resp, uid, name, role))

    async def cmd_zt(message: Message):
        pre = await _pre(message, 'zt')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗦𝘁𝗿𝗶𝗽𝗲 𝟱$'))
        res = await asyncio.to_thread(gates.stripe_5, card)
        status = (res.get('status') or 'ERROR').upper()
        resp   = res.get('message') or ''
        await _send(s, fmt.zt(card, status, resp, uid, name, role))

    async def cmd_vbs(message: Message):
        pre = await _pre(message, 'vbs')
        if not pre: return
        card, name, role, uid = pre
        s   = await message.reply(fmt.processing(card, '𝗩𝗕𝗩 𝗟𝗼𝗼𝗸𝘂𝗽 𝗔𝗽𝗶'))
        res = await asyncio.to_thread(gates.vbs_lookup, card)
        result   = res.get('result') or 'ERROR'
        raw_status = res.get('status') or res.get('message') or ''
        enrolled  = res.get('enrolled')
        ls        = res.get('liability_shifted')
        lsp       = res.get('liability_shift_possible')
        await _send(s, fmt.vbs(card, result, raw_status, enrolled, ls, lsp, uid, name, role))

    async def cmd_getemoji(message: Message):
        if message.reply_to_message:
            for ent in (message.reply_to_message.entities or
                        message.reply_to_message.caption_entities or []):
                if ent.type == 'custom_emoji':
                    await message.reply(
                        f"{ic.STAR} Emoji ID: <code>{ent.custom_emoji_id}</code>")
                    return
        await message.reply(
            f"{ic.INFO} Reply lệnh vào tin nhắn có icon Premium động.\n"
            f"Hoặc xem file <code>utils/icons.py</code> để tùy chỉnh ID.")

    commands  = {'chk': cmd_chk, 'au': cmd_au, 'ad': cmd_ad, 'pp': cmd_pp, 'pp2': cmd_pp2, 'sq': cmd_sq, 'b3': cmd_b3, 'stccn': cmd_stccn, 'vbv': cmd_vbv, 'vbs': cmd_vbs, 'zt': cmd_zt, 'st': cmd_st, 'ch': cmd_ch, 'mchk': cmd_mchk, 'mch': cmd_mch, 'getemoji': cmd_getemoji}
    callbacks = [('mchk_stop_', cb_mchk), ('mch_stop_', cb_mch)]
    return commands, callbacks
