# ⏱️ Time Analyzer AI — Local LLM Productivity Insights

Turn your daily time log into GPT-powered productivity feedback — all powered locally with LLaMA 3 via [Ollama](https://ollama.com), and built for developers who love terminal tools.

---

## 💡 What It Does

🧠 This script reads your Toggl time-tracking log (or any plain text log), sends it to a local LLaMA 3 model, and returns:

- A structured **summary** of how you spent your day  
- Highlights of **deep work vs distractions**  
- Suggestions for improvement (via LLM analysis)  

All done locally on your machine — **no OpenAI key or cloud calls.**

---

## 👩🏽‍💻 Who It’s For

- Freelancers, devs & remote workers using [Toggl Track](https://track.toggl.com/timer)  
- Productivity nerds who love AI but respect privacy  
- People who live in the terminal and want better reflection tools

---

## 🔧 Setup

### 1. Install Ollama

```bash
brew install ollama   # macOS
```

[➡️ Full install instructions](https://ollama.com/download)

---

### 2. Pull the LLaMA 3 Model

```bash
ollama pull llama3.2
```

This will download LLaMA 3.2 for local use.

---

### 3. Sign Up & Use [Toggl Track](https://track.toggl.com/timer)

1. Sign up for a free account  
2. Track your work sessions using Toggl’s web or desktop timer  
3. At the end of your day, export or copy your time entries into a pdf `.pdf` or `.csv`

---

### 4. Clone & Run This Tool

```bash
git clone https://github.com/ElishebaW/Local-LLM-Projects.git
cd Local-LLM-Projects/time_analyzer_ai
chmod +x analyze_time.sh
./analyze_time.sh
```

---

For help run `../analyze_time.sh --help`

## 🧪 Example Output


---

## 🆓 vs Pro

| Feature | Free | Pro (coming soon) |
|--------|------|-------------------|
| LLM summary | ✅ | ✅ |
| Custom prompt templates | ❌ | ✅ |
| Weekly check-in generator | ❌ | ✅ |
| Export to PDF | ❌ | ✅ |

📦 [Join the waitlist for Pro features](https://docs.google.com/forms/d/e/1FAIpQLSe2DlrwH8hiq_H0vDeWWP2oZd9dUoAmRY0PYNdwyWexUy923Q/viewform?usp=sharing)

---

## 🙌 Contribute

Have an idea? Want to integrate the Toggl API or add another LLM support?  
Shoot me an email at elisheba.t.anderson@gmail.com.