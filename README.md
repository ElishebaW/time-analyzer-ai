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

```
# 2025-04-10
**Time Usage Analysis**
======================

### Overview

Today's time usage:
```markdown
| DURATION | AMOUNT | PERCENTAGE |
| --- | --- | --- |
| Lunch | 0:58:42 | 12.86% |
| Building Agentic RAG with Llamaindex | 0:56:27 | 12.37% |
| Break | 0:32:29 | 7.12% |
| Walk | 0:24:00 | 5.26% |
| Other time entries | 0:13:41 | 1.81% |
```

Yesterday's time usage:
```markdown
| DURATION | AMOUNT | PERCENTAGE |
| --- | --- | --- |
| Pomodoro - AI | 2:07:16 | 27.88% |
| Fill out a job | 0:59:00 | 12.93% |
| Lunch | 0:58:42 | 12.86% |
| Building Agentic RAG with Llamaindex | 0:56:27 | 12.37% |
| Break | 0:32:29 | 7.12% |
| Walk | 0:24:00 | 5.26% |
| Working on Monizing my task tracker | 0:22:37 | 4.95% |
| Other time entries | 0:13:41 | 1.81% |
```

### Improvement Score

Based on the data, it appears that you maintained a consistent level of productivity throughout both days. Your overall time usage percentages are very similar between the two days.

However, I notice that you had a slightly shorter break period today (7.12% vs 8.24% yesterday). This could be an indication that you're becoming more efficient in taking breaks and refocusing on your work.

### Suggestions for Improvement

1. **Explore different Pomodoro intervals**: You've been using the standard 25:5 Pomodoro interval, which is a popular choice among productivity enthusiasts. Consider experimenting with other intervals (e.g., 20:10 or 30:15) to see if you find one that suits your work style better.
2. **Use breaks more strategically**: While breaks are essential for recharging and refocusing, they can also be used to tackle smaller tasks or make progress on a specific project. Consider using your breaks to do something productive, like responding to emails or making phone calls.
3. **Prioritize task tracking**: You've been working on monizing your task tracker, which is great! Make sure to dedicate sufficient time to this activity and explore different tools or methods until you find one that works for you.

Overall, it looks like you're maintaining a high level of productivity and making progress on your goals. Keep up the good work!
```

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