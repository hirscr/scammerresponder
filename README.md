
# 🕷 Telegram Scammer Bot

This Python bot detects messages from scammers in [Telegram Web](https://web.telegram.org), then replies using a locally hosted LLM (via [Ollama](https://ollama.com)). It’s designed to waste scammers’ time by acting naive, confused, and subtly frustrating.

---

## 📦 Install & Setup

### 1️⃣ Install Python (3.8+) & pip
- **macOS**: Python 3 comes preinstalled. If not, download from [python.org](https://www.python.org/downloads/).  
- **Windows**: Download Python from [python.org](https://www.python.org/downloads/) and check *“Add Python to PATH”* during installation.  

---

### 2️⃣ Clone this repo & set up a virtual environment
```bash
git clone https://github.com/YOUR-USERNAME/telegram-scammer-bot.git
cd telegram-scammer-bot
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3️⃣ Install Ollama
- Download & install from [ollama.com](https://ollama.com).  
- Follow their quickstart guide: [Ollama Docs](https://ollama.com/start) or read [this Medium tutorial](https://medium.com/p/ollama-install).  
- Pull the LLaMA 3 model:  
```bash
ollama pull llama3.2
```

---

### 4️⃣ Install ChromeDriver
- **macOS (with Homebrew):**  
  ```bash
  brew install chromedriver
  ```
- **Windows:** Download ChromeDriver matching your Chrome version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads).  
- Add ChromeDriver to your system PATH.

---

## ▶ How to Run
1. Log in to [web.telegram.org](https://web.telegram.org) in your regular Chrome browser (if not already logged in).  
2. From the project folder, start the bot:  
```bash
python3 scammer_bot.py
```  
The bot will:  
- Launch Chrome in debugging mode automatically.  
- Open Telegram Web.  
- Wait for you to navigate to the scammer chat and press Enter.  
- Start monitoring scammer messages and auto-responding.

---

## 🚨 Notes
- The Chrome window will stay open even if you stop the bot, so you can restart the bot without losing your place:  
```bash
python3 scammer_bot.py
```
- The bot tracks the Telegram chat window. Make sure you stay on the same chat while it runs.

---

## 📚 Medium Article (Coming Soon)
A step-by-step guide with screenshots will be published soon on Medium.

