import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import requests

# --- STEP 1: Start Chrome if not already running ---
def start_chrome_debug():
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    user_data_dir = "/tmp/chrome-debug"

    print("🔗 Checking for existing Chrome debugging session...")
    from socket import socket
    s = socket()
    try:
        s.connect(("localhost", 9222))
        s.close()
        print("✅ Chrome debugging session already running.")
    except ConnectionRefusedError:
        print("🔗 Starting Chrome in debugging mode...")
        subprocess.Popen([
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={user_data_dir}",
            "https://web.telegram.org"  # Auto-load Telegram
        ])
        print("⏳ Waiting for Chrome to start...")
        time.sleep(5)  # Give Chrome time to launch

# --- STEP 2: Connect Selenium to Chrome ---
def start_selenium():
    print("🧪 Connecting Selenium to Chrome...")
    options = webdriver.ChromeOptions()
    options.debugger_address = "localhost:9222"
    driver = webdriver.Chrome(options=options)
    return driver

# --- STEP 3: Send a message to Telegram ---
def send_message(driver, message):
    try:
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        message_box.click()
        time.sleep(random.uniform(0.5, 1.5))
        message_box.send_keys(message + Keys.ENTER)
        print(f"✅ Sent: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

# --- STEP 4: Detect scammer messages ---
def get_new_messages(driver, last_seen_texts):
    """
    Returns all new incoming scammer messages since last_seen_texts.
    """
    try:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class,"message-content")]')
        new_texts = []

        for msg in reversed(messages):
            msg_text = msg.text.strip()
            classes = msg.get_attribute("class").lower()

            # Skip empty or non-text messages
            if not msg_text:
                continue

            # Stop when we hit a message we already saw
            if msg_text in last_seen_texts:
                break

            # Include only incoming scammer messages
            if "peer-color-" in classes and "peer-color-count-" not in classes:
                new_texts.insert(0, msg_text)  # Insert at beginning for correct order

        return new_texts
    except Exception as e:
        print(f"Error getting new messages: {e}")
        return []

# --- STEP 5: Generate a response with Ollama ---
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
                    "Your replies should: "
                    "- Be friendly and polite, but subtly annoying. "
                    "- Ask repetitive questions or request clarifications even when they already explained. "
                    "- Bring up irrelevant stories or personal anecdotes. "
                    "- Change your mind in the middle of sentences, or contradict yourself. "
                    "- Use bad jokes, random thoughts, or oversharing to make the conversation chaotic. "
                    "Never accuse them of being a scammer, and never express anger. "
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
    start_chrome_debug()
    driver = start_selenium()

    print("🚀 If this is your first run, navigate to the scammer chat in Telegram Web.")
    print("👉 Once the scammer chat is open, press Enter to start.")
    input("✅ Press Enter here to begin monitoring...")

    print("🤖 Bot is running. Waiting for scammer to post something new...")
    last_seen_message = None

    try:
        last_seen_texts = []
        while True:
            # Check if Selenium session is still valid
            if driver.session_id is None:
                print("⚠️ Lost connection to Chrome. Reattaching...")
                driver = start_selenium()

            # Get all new scammer messages since last reply
            new_texts = get_new_messages(driver, last_seen_texts)

            if new_texts:
                combined_text = "\n".join(new_texts).strip()
                print(f"📩 New scammer messages:\n{combined_text}")

                print("✅ Detected new scammer message(s).")
                print("⏳ Waiting 30 seconds before replying...")
                time.sleep(30)

                # Get reply from Ollama LLaMA 3
                ollama_reply = get_ollama_response(combined_text)
                send_message(driver, ollama_reply)

                # Mark these messages as seen
                last_seen_texts.extend(new_texts)
            else:
                print("No new scammer messages. Checking again in 3 seconds...")
            time.sleep(3)
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user.")
