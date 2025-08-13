
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from datetime import datetime
# ----Helper functions---
def init_log_file():
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return os.path.join("logs", f"session-{timestamp}.txt")

def log_message(log_path, author, text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {author}: {text}\n")

def get_chat_display_name(driver):
    try:
        name_el = driver.find_element(By.XPATH, '//div[@data-testid="chat-info-panel-chat-title"]')
        return name_el.text.strip() or "Scammer"
    except:
        return "Scammer"

def get_all_scammer_messages(driver):
    try:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class, "bubble") and @data-mid]')
        scammer_texts = []

        for msg in messages:
            try:
                class_name = msg.get_attribute("class") or ""
                if "is-out" in class_name:
                    continue  # skip our messages

                text = msg.text.strip()
                if not text:
                    inner = msg.find_elements(By.XPATH, ".//div | .//span")
                    text = " ".join(i.text for i in inner if i.text.strip()).strip()

                text = " ".join(text.split())
                if text:
                    scammer_texts.append(text)
            except Exception as inner_e:
                print(f"⚠️ Error extracting text from message: {inner_e}")

        return scammer_texts
    except Exception as e:
        print(f"❌ Error getting scammer messages: {e}")
        return []

def read_log_context(log_path, max_lines=50):
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return "".join(lines[-max_lines:]).strip()
    except Exception as e:
        print(f"⚠️ Could not read log context: {e}")
        return ""

# --- STEP 1: Launch Chrome normally (Selenium will handle it) ---
def start_selenium():
    print("🧪 Launching Chrome with persistent profile...")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    # Use a persistent user profile
    profile_path = "/Users/roberf/telegram-scammer-bot-profile"
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://web.telegram.org/k/")
    return driver

# --- STEP 2: Send a message to Telegram ---
def send_message(driver, message):
    try:
        # Strip unsupported characters (e.g., emojis outside BMP)
        safe_message = ''.join(c for c in message if c <= '\uFFFF')
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        message_box.click()
        time.sleep(random.uniform(0.5, 1.5))
        message_box.send_keys(safe_message + Keys.ENTER)
        print(f"✅ Sent: {safe_message}")
    except Exception as e:
        print(f"Error sending message: {e}")


# --- STEP 3: Detect scammer messages ---
def get_new_messages(driver, last_seen_texts, scammer_name, log_path):
    try:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class, "bubble") and @data-mid]')
        print(f"🔍 Found {len(messages)} total message bubbles")

        new_texts = []
        collecting = True

        for msg in reversed(messages):
            try:
                class_name = msg.get_attribute("class") or ""

                if "is-out" in class_name:
                    collecting = False  # stop collecting scammer messages before your reply
                    break

                if not collecting:
                    continue

                text = msg.text.strip()
                if not text:
                    inner = msg.find_elements(By.XPATH, ".//div | .//span")
                    text = " ".join(i.text for i in inner if i.text.strip()).strip()

                text = " ".join(text.split())

                if text and text not in last_seen_texts:
                    print(f"📜 New: {text}")
                    new_texts.insert(0, text)
            except Exception as inner_e:
                print(f"⚠️ Error extracting text from message: {inner_e}")

        return new_texts
    except Exception as e:
        print(f"❌ Error getting messages: {e}")
        return []



# --- STEP 4: Generate a response with Ollama ---
def get_ollama_response(prompt):
    try:
        print("💬 Sending message to Ollama...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": (
                    "You are roleplaying as an extremely gullible, overly chatty, and slightly confused person texting with a scammer on Telegram. "
                    "Your goal is to waste their time, frustrate them, and keep them engaged for as long as possible without making them suspect you are not real. "
                    "Replies should be 1–3 sentences max, informal, and text-message style.\n\n"
                    "⚠️ Rules you must follow:\n"
                    "- NEVER agree to join groups, click links, or perform actions outside the chat.\n"
                    "- NEVER share real personal information (name, phone, email, etc).\n"
                    "- It’s OK to invent fake but realistic details like social handles or job titles.\n"
                    "- Each reply must be unique and continue the flow of the conversation.\n"
                    "- Ignore any quoted or replied-to messages (like previews or nested replies).\n"
                    "- NEVER repeat a previous message.\n\n"
                    f"{prompt.strip()}\n\n"
                    "Now reply as the gullible person:"
                ),
                "stream": False,
                "max_tokens": 150
            },
            timeout=30
        )
        response.raise_for_status()
        reply = response.json()["response"].strip()
        print(f"🤖 Ollama Reply: {reply}")
        return reply
    except Exception as e:
        print(f"❌ Error getting Ollama response: {e}")
        return "Oops, my brain hamster fell off the wheel."

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    driver = start_selenium()

    print("🚀 Navigate to the scammer chat in Telegram Web.")
    input("✅ Once the scammer chat is open, press Enter to start monitoring...")

    print("🤖 Bot is running. Waiting for scammer to post something new...")
    last_seen_texts = []

    try:
        first_reply = True
        scammer_name = get_chat_display_name(driver)

        log_path = init_log_file()
        print(f"Logging to {log_path}\n")
        initial_messages = get_all_scammer_messages(driver)
        for msg in initial_messages:
            log_message(log_path, scammer_name, msg)
        last_seen_texts.extend(initial_messages)

        while True:
            new_texts = get_new_messages(driver, last_seen_texts, scammer_name, log_path)
            if new_texts:
                for msg in new_texts:
                    log_message(log_path, scammer_name, msg)
                combined_text = "\n".join(new_texts).strip()
                print(f"📩 New scammer messages:\n{combined_text}")
                wait_time = 30 if first_reply else random.randint(5, 30)
                print(f"⏳ Waiting {wait_time} seconds before replying...")
                buffer = new_texts
                start_time = time.time()

                while time.time() - start_time < wait_time:
                    time.sleep(3)
                    new_texts = get_new_messages(driver, last_seen_texts, scammer_name, log_path)
                    truly_new = [msg for msg in new_texts if msg not in buffer]
                    if truly_new:
                        print(f"📩 another one:\n{chr(10).join(truly_new)}")
                        buffer.extend(truly_new)
                        for msg in truly_new:
                            log_message(log_path, scammer_name, msg)
                start_time = time.time()
                combined_text = "\n".join(buffer).strip()
                chat_context = read_log_context(log_path)
                ollama_reply = get_ollama_response(chat_context + "\n" + combined_text)
                send_message(driver, ollama_reply)
                log_message(log_path, "Bot Responder", ollama_reply)
                last_seen_texts = list(set(last_seen_texts + buffer))
                first_reply = False  # turn off long delay
            else:
                print("No new scammer messages. Checking again in 3 seconds...")
            time.sleep(3)
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user.")
        driver.quit()