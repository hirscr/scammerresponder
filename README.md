# 🕵️‍♂️ Telegram Scammer Time-Waster Bot


<pre>```
███████  ██████  █████  ███    ███ ███    ███ ███████ ██████  ██████  ███████ ███████ ██████   ██████  ███    ██ ██████  ███████ ██████  
██      ██      ██   ██ ████  ████ ████  ████ ██      ██   ██ ██   ██ ██      ██      ██   ██ ██    ██ ████   ██ ██   ██ ██      ██   ██ 
███████ ██      ███████ ██ ████ ██ ██ ████ ██ █████   ██████  ██████  █████   ███████ ██████  ██    ██ ██ ██  ██ ██   ██ █████   ██████  
     ██ ██      ██   ██ ██  ██  ██ ██  ██  ██ ██      ██   ██ ██   ██ ██           ██ ██      ██    ██ ██  ██ ██ ██   ██ ██      ██   ██ 
███████  ██████ ██   ██ ██      ██ ██      ██ ███████ ██   ██ ██   ██ ███████ ███████ ██       ██████  ██   ████ ██████  ███████ ██   ██ ```</pre>                                                                                                                                      
                                                                                                                                         
                                                                                                                                         
                                                                                                                                         


> **Mission:** Waste scammers’ time, frustrate them endlessly, and keep them too busy to scam someone else — all while keeping you safe.

Inspired by the [LevelUp article on trapping Telegram scammers in endless AI conversations](https://levelup.gitconnected.com/i-trapped-telegram-scammers-in-an-endless-ai-conversation-5535a7d67a2f), this bot automates the art of trolling fraudsters. Using Selenium, Telegram Web, and [Ollama](https://ollama.ai/) (with a local AI model), it responds like a *gullible but chatty human*, keeping scammers hooked in an infinite loop.

---

## ✨ Features

* **Automated Scammer Engagement**
  The bot monitors scammer messages in a Telegram Web chat and instantly crafts believable, time-wasting replies.

* **AI-Generated Personalities**
  Uses [Ollama](https://ollama.ai/) with `llama3.2` to roleplay as a clueless but endlessly talkative human.

* **Safe Interaction**
  Refuses to click links, join groups, or reveal real personal data. All details shared are fake but plausible.

* **Conversation Logging**
  Every interaction is logged to `logs/session-YYYY-MM-DD_HHMMSS.txt` for laughs, analysis, or evidence.

* **Human-Like Delays**
  Replies are sent with randomized delays to appear more human and avoid suspicion.

---

## 🚀 How It Works

1. **Launches Telegram Web** in Chrome with your persistent profile (so you stay logged in).
2. **Watches for new scammer messages** in an open chat window.
3. **Builds conversation context** from recent logs.
4. **Generates AI responses** with Ollama based on conversation history.
5. **Sends replies** with random, realistic delays.
6. **Repeats until you stop it** — the scammer won’t know what hit them.

---

## 📦 Requirements

* **Python 3.9+**
* **Google Chrome**
* **ChromeDriver** (matching your Chrome version)
* **Ollama** running locally (`ollama serve`)
* **`llama3.2` model** installed in Ollama
* Python packages:

  ```bash
  pip install selenium requests
  ```

---

## ⚙️ Setup

1. **Install Ollama**
   Follow instructions at [ollama.ai/download](https://ollama.ai/download).

2. **Pull the Model**

   ```bash
   ollama pull llama3.2
   ```

3. **Set Your Chrome Profile Path**
   In `start_selenium()`, update:

   ```python
   profile_path = "/path/to/your/chrome/profile"
   ```

   This keeps you logged into Telegram Web without reauthenticating.

4. **Run the Bot**

   ```bash
   python scammer_bot.py
   ```

5. **Open a Scammer Chat in Telegram Web**
   Once ready, press **Enter** to start monitoring.

---

## 📝 Example Log Snippet

```
[2025-08-14 14:32:10] Scammer: Hello dear, I have great investment opportunity for you.
[2025-08-14 14:32:42] Bot Responder: omg that’s wild lol. i just spilled coffee on my socks 😂 what kinda investment?
```

---

## 🛡️ Safety Rules (Enforced by AI)

* No clicking links.
* No joining groups.
* No revealing real personal information.
* Only share **invented but realistic** fake details.
* Keep replies short, unique, and in casual text-message style.

---

## 🧑‍💻 Code Structure

```
scammer_bot.py
├── init_log_file()        # Creates session log files
├── log_message()          # Saves messages to logs
├── get_chat_display_name()
├── get_all_scammer_messages()
├── read_log_context()
├── start_selenium()       # Opens Chrome with Telegram Web
├── send_message()         # Sends messages to chat
├── get_new_messages()     # Detects scammer messages
├── get_ollama_response()  # AI response generation
└── main loop              # Orchestrates bot actions
```

---

## 🤝 Contributing

We welcome PRs that:

* Improve AI persona prompts
* Add scammer detection patterns
* Enhance human-like typing behavior
* Extend support to other messaging platforms

---

## 📜 License

MIT License — free to use, modify, and share.
**Ethical Notice:** Use this tool only against confirmed scammers. Harassment of legitimate users is prohibited.

---

## ❤️ Why We Do This

Every second a scammer spends chatting with this bot is a second they *aren’t* targeting a vulnerable person. By wasting their time, we reduce harm and maybe even make them reconsider their life choices.
