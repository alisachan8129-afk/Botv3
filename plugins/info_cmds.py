import html
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from utils import icons as ic

def setup(ctx) -> tuple:
    is_admin      = ctx['is_admin']
    get_user      = ctx['get_user']
    register_user = ctx['register_user']
    ban_user      = ctx['ban_user']
    unban_user    = ctx['unban_user']
    GROUP_LINK    = ctx['GROUP_LINK']

    def _ensure(user):
        register_user(user.id, user.username or '', user.first_name or 'User')
        return get_user(user.id) or {}

    async def cmd_start(message: Message):
        u    = message.from_user
        data = _ensure(u)
        uid  = u.id
        name = html.escape(u.first_name or 'User')
        username = html.escape(u.username or 'None')

        text = (
            f"⭐️  <b>𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼, {name}!</b>\n\n"
            f"🎈   <b>𝐍𝐚𝐦𝐞</b>   {ic.ARR}  <a href='tg://user?id={uid}'>{username}</a>\n"
            f"🔗   <b>𝐈𝐃</b>     {ic.ARR}  <code>{uid}</code>\n"
            f"\n🛸 <b>𝗨𝘀𝗲 𝘁𝗵𝗲 𝗺𝗲𝗻𝘂 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝗴𝗲𝘁 𝘀𝘁𝗮𝗿𝘁𝗲𝗱:</b>"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=' 𝗚𝗮𝘁𝗲𝘀', callback_data='help_main', style='success', icon_custom_emoji_id='6026321200597176575'),
            InlineKeyboardButton(text=' 𝗚𝗿𝗼𝘂𝗽', url=GROUP_LINK, style='primary', icon_custom_emoji_id='6026106482297147601'),
        ]])
        await message.reply(ic.premium_emoji(text), reply_markup=kb)

    async def cb_help(call: CallbackQuery):
        section = call.data
        back_kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=' 𝗕𝗮𝗰𝗸', callback_data='help_main', style='danger', icon_custom_emoji_id='4904819211416633963')
        ]])

        if section == 'help_main':
            text = (
                f"<b>👻 𝙂𝙖𝙩𝙚𝙬𝙖𝙮𝙨 𝙈𝙚𝙣𝙪</b>\n\n"
                f"🐸 <b>𝗔𝘂𝘁𝗵 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ 6️⃣\n"
                f"🐸 <b>𝗖𝗵𝗮𝗿𝗴𝗲 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀</b> ➜ 6️⃣\n"
                f"🐸 <b>𝗠𝗮𝘀𝘀 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀</b> ➜ 2️⃣\n"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=' 𝗔𝘂𝘁𝗵 𝗚𝗮𝘁𝗲𝘀',   callback_data='help_auth',   style='success', icon_custom_emoji_id='5361563222132405424'),
                    InlineKeyboardButton(text=' 𝗖𝗵𝗮𝗿𝗴𝗲 𝗚𝗮𝘁𝗲𝘀', callback_data='help_charge', style='success', icon_custom_emoji_id='5981305412144599367'),
                ],
                [InlineKeyboardButton(text=' 𝗠𝗮𝘀𝘀 𝗚𝗮𝘁𝗲𝘀', callback_data='mass', style='primary', icon_custom_emoji_id='6026342293181568142')],
                [InlineKeyboardButton(text=' 𝗦𝗵𝗼𝗽𝗶𝗳𝘆', callback_data='shopify', style='primary', icon_custom_emoji_id='6321225560789877992')],
                [InlineKeyboardButton(text=' 𝗕𝗮𝗰𝗸', callback_data='back_start', style='danger', icon_custom_emoji_id='4904819211416633963')],
                
            ])
        elif section == 'help_auth':
            text = (
                f"<b>🐳 𝗔𝘂𝘁𝗵 𝗚𝗮𝘁𝗲𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱</b>\n\n"
                f"<blockquote><b>𝟭. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Stripe Auth</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/chk</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟮. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Stripe Auth 2</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/au</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟯. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Ayden Auth</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/ad</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟰. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Braintree Auth</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/b3</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟱. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>VBV Lookup Database</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/vbv</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟲. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>VBV Lookup Api</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/vbs</code> CC|MM|YY|CVV"
                f"\n\n 🙁"
            )
            kb = back_kb
        elif section == 'mass':
            text = (
                f"<b>🐳 𝗠𝗮𝘀𝘀 𝗚𝗮𝘁𝗲𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱</b>\n\n"
                f"<blockquote><b>𝟭. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Mass Stripe Auth</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/mchk</code> Reply file.txt (Max 1000 lines)\n\n"
                f"<blockquote><b>𝟮. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Mass Stripe 1$</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/mch</code> Reply file.txt (Max 1000 lines)"
                f"\n\n 🙁"
            )
            kb = back_kb
        elif section == 'shopify':
            text = (
                f"<b>🐳 𝗦𝗵𝗼𝗽𝗶𝗳𝘆 𝗖𝗼𝗺𝗺𝗮𝗻𝗱</b>\n\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/cc</code> CC|MM|YY|CVV\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/ran</code> Reply file .txt (Max 1500 lines)\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/addproxy</code> Add proxies (one per line)\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/delproxy</code> Delete proxies\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/proxylist</code> Show proxy list\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/clearproxy</code> Clear all proxies\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/checkproxy</code> Check all proxies"
                f"\n\n 🙁"
            )
            kb = back_kb
        elif section == 'help_charge':
            text = (
                f"<b>🐳 𝗖𝗵𝗮𝗿𝗴𝗲 𝗚𝗮𝘁𝗲𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱</b>\n\n"
                f"<blockquote><b>𝟭. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>PayPal 1$</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/pp</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟮. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>PayPal 1$ 2</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/pp2</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟯. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Square 1$</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/sq</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟰. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Stripe CCN 3$</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/stccn</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟱. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Stripe 1.1$</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/st</code> CC|MM|YY|CVV\n\n"
                f"<blockquote><b>𝟲. 𝗚𝗮𝘁𝗲𝘄𝗮𝘆</b> ➜ <b>Stripe 1$</b> 🐸</blockquote>\n"
                f"⏭️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ➜ <code>/ch</code> CC|MM|YY|CVV"
                f"\n\n 🙁"
            )
            kb = back_kb
        elif section == 'help_tools':
            text = (
                f"{ic.CHART} <b>𝗧𝗼𝗼𝗹𝘀</b>\n{ic.LINE}\n"
                f"{ic.ARR} /start    ➜ Account info\n"
                f"{ic.ARR} /help     ➜ Command menu\n"
                f"{ic.ARR} /getemoji ➜ Get Premium emoji ID\n"
                f"{ic.LINE}"
            )
            kb = back_kb
        elif section == 'back_start':
            name = html.escape(call.from_user.first_name or 'User')
            uid  = call.from_user.id
            username = html.escape(call.from_user.username or 'None')
            text = (
                f"⭐️  <b>𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼, {name}!</b>\n\n"
                f"🎈   <b>𝐍𝐚𝐦𝐞</b>   {ic.ARR}  <a href='tg://user?id={uid}'>{username}</a>\n"
                f"🔗   <b>𝐈𝐃</b>     {ic.ARR}  <code>{uid}</code>\n"
                f"\n🛸 <b>𝗨𝘀𝗲 𝘁𝗵𝗲 𝗺𝗲𝗻𝘂 𝗯𝗲𝗹𝗼𝘄 𝘁𝗼 𝗴𝗲𝘁 𝘀𝘁𝗮𝗿𝘁𝗲𝗱:</b>"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=' 𝗚𝗮𝘁𝗲𝘀', callback_data='help_main', style='success', icon_custom_emoji_id='6026321200597176575'),
                InlineKeyboardButton(text=' 𝗚𝗿𝗼𝘂𝗽', url=GROUP_LINK, style='primary', icon_custom_emoji_id='6026106482297147601'),
            ]])
            try:
                await call.message.edit_text(ic.premium_emoji(text), reply_markup=kb)
            except Exception:
                pass
            await call.answer()
            return
        else:
            await call.answer()
            return

        try:
            await call.message.edit_text(ic.premium_emoji(text), reply_markup=kb)
        except Exception:
            pass
        try:
            await call.answer()
        except Exception:
            pass

    async def cmd_ban(message: Message):
        if not is_admin(message.from_user.id): return
        parts = (message.text or '').split()
        if len(parts) < 2 or not parts[1].isdigit():
            await message.reply("⚠️ <b>Usage:</b> <code>/ban user_id</code>")
            return
        uid = int(parts[1])
        if is_admin(uid):
            await message.reply("❌ <b>Cannot ban an admin.</b>")
            return
        if ban_user(uid):
            await message.reply(f"🚫 <b>Banned user</b> <code>{uid}</code>")
        else:
            await message.reply(f"⚠️ <b>User</b> <code>{uid}</code> <b>already banned.</b>")

    async def cmd_unban(message: Message):
        if not is_admin(message.from_user.id): return
        parts = (message.text or '').split()
        if len(parts) < 2 or not parts[1].isdigit():
            await message.reply("⚠️ <b>Usage:</b> <code>/unban user_id</code>")
            return
        uid = int(parts[1])
        if unban_user(uid):
            await message.reply(f"✅ <b>Unbanned user</b> <code>{uid}</code>")
        else:
            await message.reply(f"⚠️ <b>User</b> <code>{uid}</code> <b>is not banned.</b>")

    commands  = {'start': cmd_start, 'help': cmd_start, 'ban': cmd_ban, 'unban': cmd_unban}
    callbacks = [('help_', cb_help), ('back_start', cb_help), ('shopify', cb_help), ('mass', cb_help)]
    return commands, callbacks
