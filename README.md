# ◆ SQLSense AI

**A smarter way to learn SQL — write a query, and this tool tells you what it does, how fast it runs, what mistakes to avoid, and even quizzes you on it.**

Most SQL practice websites just tell you "correct" or "wrong." They don't explain *why*. SQLSense AI is different — it acts like a personal SQL tutor. Write any query, and it will:

- Explain it in simple English
- Show you the actual order the database runs it in
- Point out mistakes and how to fix them
- Give it a performance score out of 100
- Even turn a plain English sentence into a working SQL query

It's built for anyone learning SQL — students, beginners, and anyone preparing for interviews.
---

## 🎯 Why This Exists

Existing SQL practice platforms (LeetCode, HackerRank, SQLZoo) are built around one pattern: pick a problem, submit a query, get a pass/fail. None of them let you write **your own** query and get deep, structural feedback on it — why it's slow, what order it actually runs in, or what a recruiter might ask about it.

SQLSense AI is not another question bank. It's a **query microscope** — bring any query, on any schema, and it tells you what's really going on.

---

## ✨ Features

| Feature | How it works |
|---|---|
| **📊 Query Execution** | Runs any SQL statement (SELECT, UPDATE, DELETE, INSERT) safely against a real SQLite database |
| **✨ AI Explanation** | Gemini explains your query in plain, beginner-friendly English |
| **🔀 Execution Order** | Rule-based engine reveals the *actual* order SQL runs in (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY) — not the order   you wrote it in |
| **⚡ Query Optimizer** | 13 custom rules catch issues like `SELECT *`, missing `WHERE` on `UPDATE`/`DELETE`, aggregate functions misused in `WHERE`, unsafe `NOT IN` subqueries, and more — each with a plain-English explanation |
| **🎯 Performance Score** | A 0–100 score derived from the optimizer's findings, with a visual progress bar |
| **💬 Natural Language → SQL** | Describe what you want in plain English; Gemini generates a working query against your actual schema |
| **🎯 Interview Question Generator** | Generates practice interview questions based on the exact SQL concepts used in your query |
| **📋 Schema Explorer** | Browse every table, column, and sample data before writing a single query |
| **🕐 Query History** | Automatically saves your recent queries — click to reload instantly |
| **📖 Learn SQL** | A reference page covering 18 core-to-advanced SQL concepts (JOINs, CTEs, window functions, triggers, indexes, and more), each with a runnable example against this project's own schema |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (custom dark theme, gradient UI)
- **Backend Logic:** Python (rule-based optimizer, execution order engine, scoring)
- **Database:** SQLite (5 interrelated tables, a trigger, a view, and indexes)
- **AI:** Google Gemini API
- **Libraries:** `pandas`, `sqlite3`, `google-genai`, `python-dotenv`

---

## 🗄️ Database Schema

The project ships with a realistic sample database so every feature is testable out of the box:

- `departments` — department records
- `employees` — includes a self-referencing `manager_id` (for self-joins & recursive CTEs)
- `projects` — linked to departments
- `employee_projects` — a many-to-many junction table
- `salary_audit` — populated automatically by a trigger whenever a salary is updated

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<tamannatyagi-14>/SQLSense-AI.git
cd SQLSense-AI
```

### 2. Set up a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
Create a `.env` file in the root folder:
Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 5. Run the app
```bash
streamlit run app.py
```

The sample database is already included, so the app works immediately — no setup queries needed.

---

## 📁 Project Structure
SQLSense-AI/
├── app.py # Main Streamlit app
├── backend/
│ ├── execution_order.py # Rule-based execution order logic
│ ├── optimizer.py # 13-rule query optimizer
│ ├── score.py # Performance scoring
│ ├── ai_engine.py # Gemini integration (explain, NL→SQL, interview Qs)
│ ├── schema_explorer.py # Reads live schema from the database
│ ├── history.py # Query history persistence
│ └── learn_content.py # Static content for the Learn page
├── database/
│ ├── setup_db.py # Builds the sample database from scratch
│ └── sample.db # Pre-built SQLite database
└── requirements.txt

---

## 🧠 What Makes This Different

Every "smart" feature in this project falls into one of two clearly separated categories:

- **Rule-based (fully custom logic, no AI):** Execution Order, Query Optimizer, Performance Score — deterministic, explainable, and testable
- **AI-powered (Gemini):** Explanation, Natural Language → SQL, Interview Questions — where genuine language understanding is needed

This separation means the project isn't "just a ChatGPT wrapper" — the core analytical engine is hand-written and fully inspectable.

---

## 🔭 Future Scope

- PostgreSQL / MySQL support (for DCL commands, which SQLite doesn't support)
- Daily SQL challenges
- Exportable PDF/TXT reports
- User authentication for personal query history

---

## 👤 Author

**Tamanna Tyagi**
B.Tech CSE student

---

*Built as a portfolio project to go beyond "practice platforms" — a tool that explains SQL the way a mentor would.*