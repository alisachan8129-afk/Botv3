import asyncio
import importlib
import sys
import os
import html
import logging
import socket

_lock_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    _lock_socket.bind(('127.0.0.1', 47291))
except OSError:
    print("❌ Another bot instance is already running! Exiting.")
    sys.exit(1)

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage

from utils import icons       as _icons
from utils import card_parser as _card_parser
from utils import bin_api     as _bin_api
import api.gates as _gates
import api.data  as _data

logging.basicConfig(level=logging.WARNING)

BOT_TOKEN      = "8787030321:AAHiOJsh0s3escHhuKPr5-K2W78ORh9uJ5c" 
ROOT_ADMIN_IDS = [5188362948]
GROUP_LINK     = "https://t.me/MatrixAutoXchat"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_MAINTENANCE_MODE = False

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp  = Dispatcher(storage=MemoryStorage())

_data.init(BASE_DIR, ROOT_ADMIN_IDS)

PLUGIN_MODULES = [
    "plugins.info_cmds",
    "plugins.gateways",
    "plugins.shopify",
]

_cmd_registry: dict = {}
_cb_registry:  list = []
_reload_lock = asyncio.Lock()

def _build_ctx() -> dict:
    return {
        "bot":            bot,
        "GROUP_LINK":     GROUP_LINK,
        "ROOT_ADMIN_IDS": ROOT_ADMIN_IDS,
        "icons":          _icons,
        "is_admin":      _data.is_admin,
        "get_admin_ids": _data.get_admin_ids,
        "is_banned":     _data.is_banned,
        "ban_user":      _data.ban_user,
        "unban_user":    _data.unban_user,
        "get_user":                 _data.get_user,
        "register_user":            _data.register_user,
        "deduct_credit_for_status": _data.deduct_credit_for_status,
        "parse_first_card": _card_parser.parse_first_card,
        "parse_all_cards":  _card_parser.parse_all_cards,
        "parse_bin_info": _bin_api.parse_bin_info,
        "gates":          _gates,
        "_safe_error":    _gates._safe_error,
        "_call_gate_api": _gates._call_gate_api,
        "BASE_DIR":            BASE_DIR,
        "get_user_proxies":    _data.get_user_proxies,
        "add_user_proxies":    _data.add_user_proxies,
        "remove_user_proxy":   _data.remove_user_proxy,
        "load_shopify_data":   _data.load_shopify_data,
        "save_shopify_data":   _data.save_shopify_data,
        "check_proxy_via_ip":  _data.check_proxy_via_ip_api,
        "get_maintenance_mode": lambda: IS_MAINTENANCE_MODE,
    }

@dp.message(Command('mtn'))
async def cmd_mtn(message: Message):
    global IS_MAINTENANCE_MODE
    if not _data.is_admin(message.from_user.id): return
    args = (message.text or "").strip().lower().split()
    if len(args) < 2:
        state = "ON" if IS_MAINTENANCE_MODE else "OFF"
        await message.reply(f"🔧 <b>Maintenance: {state}</b>\n<code>/mtn on|off</code>")
        return
    if   args[1] == "on":  IS_MAINTENANCE_MODE = True;  await message.reply("🛠️ <b>Maintenance ENABLED.</b>")
    elif args[1] == "off": IS_MAINTENANCE_MODE = False; await message.reply("✅ <b>Maintenance DISABLED.</b>")

@dp.message(Command('reload'))
async def cmd_reload(message: Message):
    if not _data.is_admin(message.from_user.id): return
    if _reload_lock.locked():
        await message.reply("⏳ <b>Reload đang chạy, chờ xíu...</b>")
        return
    async with _reload_lock:
        s = await message.reply("🔄 <b>Reloading plugins...</b>")
        errors = await reload_all_plugins()
        if errors:
            lines = "\n".join(f"• <code>{html.escape(e)}</code>" for e in errors)
            await s.edit_text(f"⚠️ <b>Reload errors:</b>\n{lines}")
        else:
            loaded = ", ".join(f"<code>{m.split('.')[-1]}</code>" for m in PLUGIN_MODULES)
            await s.edit_text(f"✅ <b>Reloaded!</b>\n{loaded}")

@dp.message(Command('broadcast'))
async def cmd_broadcast(message: Message):
    if not _data.is_admin(message.from_user.id): return
    parts = (message.text or '').split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("📢 <b>Usage:</b> <code>/broadcast nội dung</code>")
        return
    text = parts[1]
    users = _data.load_users()
    s = await message.reply(f"📤 <b>Broadcasting to {len(users)} users...</b>")
    ok = fail = 0
    for uid in users:
        try:
            await bot.send_message(int(uid), text, parse_mode=ParseMode.HTML)
            ok += 1
        except Exception:
            fail += 1
    await s.edit_text(f"✅ <b>Broadcast done!</b>\n✅ Sent: <b>{ok}</b>\n❌ Failed: <b>{fail}</b>")

@dp.message(F.text.startswith('/'))
async def plugin_dispatch(message: Message):
    if not message.from_user: return
    if _data.is_banned(message.from_user.id):
        await message.reply("🚫 <b>You are banned from using this bot.</b>")
        return
    if IS_MAINTENANCE_MODE and not _data.is_admin(message.from_user.id):
        await message.reply("🛠️ <b>Bot đang bảo trì. Vui lòng chờ.</b>")
        return
    cmd = (message.text or '').split()[0][1:].split('@')[0].lower()
    h = _cmd_registry.get(cmd)
    if h:
        await h(message)

@dp.callback_query()
async def plugin_cb_dispatch(call: CallbackQuery):
    if not call.data:
        await call.answer()
        return
    for matcher, h in _cb_registry:
        matched = matcher(call.data) if callable(matcher) else call.data.startswith(str(matcher))
        if matched:
            await h(call)
            return
    await call.answer()

async def load_all_plugins():
    ctx = _build_ctx()
    errors = []
    for mod_name in PLUGIN_MODULES:
        try:
            mod = (importlib.reload(sys.modules[mod_name]) if mod_name in sys.modules
                   else importlib.import_module(mod_name))
            cmds, cbs = mod.setup(ctx)
            _cmd_registry.update(cmds)
            _cb_registry.extend(cbs)
            print(f"  ✅ {mod_name}")
        except Exception as e:
            errors.append(f"{mod_name}: {e}")
            print(f"  ❌ {mod_name}: {e}")
    return errors

async def reload_all_plugins():
    for dep in ["api.gates", "api.data", "utils.formats", "utils.icons",
                "utils.card_parser", "utils.bin_api"]:
        if dep in sys.modules:
            try:   importlib.reload(sys.modules[dep])
            except Exception as e: print(f"  ⚠️ reload {dep}: {e}")

    _data.init(BASE_DIR, ROOT_ADMIN_IDS)
    _cmd_registry.clear()
    _cb_registry.clear()
    ctx = _build_ctx()
    errors = []
    for mod_name in PLUGIN_MODULES:
        try:
            mod = (importlib.reload(sys.modules[mod_name]) if mod_name in sys.modules
                   else importlib.import_module(mod_name))
            cmds, cbs = mod.setup(ctx)
            _cmd_registry.update(cmds)
            _cb_registry.extend(cbs)
            print(f"  ✅ {mod_name}")
        except Exception as e:
            errors.append(f"{mod_name}: {e}")
            print(f"  ❌ {mod_name}: {e}")
    return errors

async def main():
    print("🤖 Bot V3 starting (aiogram 3.26)...")
    errs = await load_all_plugins()
    for e in errs: print(f"  ⚠️ {e}")
    print(f"✅ Started | Admins: {_data.get_admin_ids()}")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
