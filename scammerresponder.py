import subprocess
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# --- STEP 1: Launch Chrome normally (Selenium will handle it) ---
def start_selenium():
    print("🧪 Launching Chrome with Selenium...")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.telegram.org")  # Auto-load Telegram
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
def get_new_messages(driver, last_seen_texts):
    try:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class,"message-content")]')
        new_texts = []
        for msg in reversed(messages):
            msg_text = msg.text.strip()
            classes = msg.get_attribute("class").lower()

            # Skip empty, non-text, or edited messages
            if not msg_text:
                continue
            if "edited" in classes or "service-message" in classes:
                continue

            # Stop if we've already seen this message
            if msg_text in last_seen_texts:
                break

            # Only include scammer messages
            if "peer-color-" in classes and "peer-color-count-" not in classes:
                new_texts.insert(0, msg_text)
        return new_texts
    except Exception as e:
        print(f"Error getting new messages: {e}")
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
                    "You are roleplaying as an extremely gullible, overly chatty, and slightly confused person who is texting with a scammer on Telegram. "
                    "Your goal is to waste their time, frustrate them, and keep them engaged for as long as possible without making them suspect you are not real. "
                    "Keep replies short (1-3 sentences max) like a real person texting on Telegram.\n\n"
                    f"Scammer: {prompt}\nYou:"
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
        while True:
            new_texts = get_new_messages(driver, last_seen_texts)
            if new_texts:
                combined_text = "\n".join(new_texts).strip()
                print(f"📩 New scammer messages:\n{combined_text}")
                print("⏳ Waiting 30 seconds before replying...")
                time.sleep(30)
                ollama_reply = get_ollama_response(combined_text)
                send_message(driver, ollama_reply)
                last_seen_texts.extend(new_texts)
            else:
                print("No new scammer messages. Checking again in 3 seconds...")
            time.sleep(3)
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user.")
        driver.quit()
