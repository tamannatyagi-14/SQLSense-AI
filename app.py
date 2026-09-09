import streamlit as st
import sqlite3
import pandas as pd
from backend.execution_order import get_execution_order
from backend.optimizer import analyze_query
from backend.score import calculate_score, get_score_label
from backend.schema_explorer import get_schema_info
from backend.ai_engine import explain_query, generate_sql_from_text
from backend.history import load_history, save_query
from backend.learn_content import LEARN_TOPICS
from backend.ai_engine import explain_query, generate_sql_from_text, generate_interview_questions


# ---------- Page Config ----------
st.set_page_config(page_title="SQLSense AI", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem !important;
}
.stApp {
    background-color: #14131A;
}
h1 {
    font-weight: 700 !important;
    letter-spacing: -0.5px;
    color: #F4F3F6 !important;
}
.stCaption, [data-testid="stCaptionContainer"] {
    color: #A9A7B0 !important;
}
.stTextArea textarea {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    background-color: #1F1E26;
    border: 1px solid #2E2D36;
    border-radius: 14px !important;
    color: #F4F3F6 !important;
}
.stTextArea textarea::placeholder {
    color: #6B6975 !important;
    opacity: 1 !important;
}
[data-testid="stDataFrame"] {
    background-color: #1F1E26;
    border-radius: 14px;
}
[data-testid="stMetric"] {
    background-color: #1F1E26;
    border: 1px solid #2E2D36;
    border-radius: 14px;
    padding: 12px 16px;
}
button[kind="primary"] {
    background: linear-gradient(135deg, #5B5CF0, #00C2D1) !important;
    color: white !important;
    border: none !important;
    border-radius: 100px !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 16px rgba(91,92,240,0.3) !important;
}
button[kind="primary"]:hover {
    opacity: 0.9 !important;
    color: white !important;
}
button[kind="secondary"] {
    background-color: #1F1E26 !important;
    border: 1px solid #2E2D36 !important;
    border-radius: 16px !important;
    color: #A9A7B0 !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}
button[kind="secondary"]:hover {
    border-color: #5B5CF0 !important;
    color: #F4F3F6 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session State Initialization (ALL of it, before anything else) ----------
if "query_input" not in st.session_state:
    st.session_state.query_input = ""
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Result"
if "result_df" not in st.session_state:
    st.session_state.result_df = None
if "result_error" not in st.session_state:
    st.session_state.result_error = None
if "rows_affected" not in st.session_state:
    st.session_state.rows_affected = None
if "has_run" not in st.session_state:
    st.session_state.has_run = False
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "input_mode" not in st.session_state:
    st.session_state.input_mode = "SQL"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Workspace"

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### ◆ SQLSense AI")
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("🏠 Workspace", type="primary" if st.session_state.current_page == "Workspace" else "secondary", use_container_width=True):
            st.session_state.current_page = "Workspace"
            st.rerun()
    with nav2:
        if st.button("📖 Learn", type="primary" if st.session_state.current_page == "Learn" else "secondary", use_container_width=True):
            st.session_state.current_page = "Learn"
            st.rerun()
    st.divider()

    st.markdown("### 🕐 Recent Queries")
    history = load_history()
    if not history:
        st.caption("No queries yet — run one to see it here.")
    else:
        for item in history[:4]: 
            icon = "🟢" if item["status"] == "success" else "🔴"
            short_query = item["query"][:40] + ("..." if len(item["query"]) > 40 else "")
            if st.button(f"{icon} {short_query}", key=f"hist_{item['timestamp']}", use_container_width=True):
                st.session_state.query_input = item["query"]
                st.rerun()

    st.divider()

    st.markdown("### 📋 Database Schema")
    st.caption("Explore the tables before writing your query")
    schema = get_schema_info()
    for table_name, info in schema.items():
        with st.expander(f"**{table_name}** ({len(info['columns'])} cols)"):
            for col in info["columns"]:
                st.markdown(f"- `{col['name']}` — *{col['type']}*")
            if info["sample_rows"]:
                st.write("**Sample data:**")
                col_names = [c["name"] for c in info["columns"]]
                sample_df = pd.DataFrame(info["sample_rows"], columns=col_names)
                st.dataframe(sample_df, use_container_width=True, hide_index=True)

# ---------- Database Connection Function ----------
def run_query(sql_query):
    conn = sqlite3.connect("database/sample.db")
    cursor = conn.cursor()
    stripped = sql_query.strip().upper()
    is_select = stripped.startswith("SELECT") or stripped.startswith("WITH") or stripped.startswith("PRAGMA")
    try:
        if is_select:
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
            return df, None, None
        else:
            cursor.execute(sql_query)
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return None, None, affected
    except Exception as e:
        conn.close()
        return None, str(e), None

# ================= PAGE: WORKSPACE =================
if st.session_state.current_page == "Workspace":
    st.title("◆ SQLSense AI")
    st.caption("Write a SQL query below and run it against the sample database.")

    # ---------- Input Mode Toggle ----------
    t1, t2 = st.columns(2)
    with t1:
        if st.button("🔤 Write SQL", type="primary" if st.session_state.input_mode == "SQL" else "secondary", use_container_width=True):
            st.session_state.input_mode = "SQL"
            st.rerun()
    with t2:
        if st.button("💬 Describe in English", type="primary" if st.session_state.input_mode == "English" else "secondary", use_container_width=True):
            st.session_state.input_mode = "English"
            st.rerun()

    st.write("")

    # ---------- English Input (only shown in English mode) ----------
    if st.session_state.input_mode == "English":
        english_text = st.text_area(
            "Describe what you want",
            height=80,
            label_visibility="collapsed",
            placeholder="e.g. Show me employees earning more than 50000"
        )
        if st.button("✨ Generate SQL", type="primary"):
            if english_text.strip() == "":
                st.warning("Please describe what you want first.")
            else:
                with st.spinner("Generating SQL..."):
                    schema_for_ai = get_schema_info()
                    sql, error = generate_sql_from_text(english_text, schema_for_ai)
                    if error:
                        st.error(f"❌ Could not generate SQL: {error}")
                    else:
                        st.session_state.query_input = sql
                        st.session_state.input_mode = "SQL"
                        st.rerun()
        st.write("")

    # ---------- Example Query Button ----------
    if st.button("✨ Try an example", type="primary"):
        st.session_state.query_input = "SELECT e.name, d.department_name FROM employees e JOIN departments d ON e.department_id = d.id"
        st.rerun()

    # ---------- Query Input Box ----------
    query = st.text_area(
        "SQL Query",
        height=100,
        label_visibility="collapsed",
        placeholder="SELECT * FROM employees WHERE salary > 50000",
        key="query_input"
    )

    run_clicked = st.button("Run ▸", type="primary")

    # ---------- Run Query ----------
    if run_clicked:
        if query.strip() == "":
            st.warning("Please enter a query first.")
            st.session_state.has_run = False
        else:
            df, error, affected = run_query(query)
            st.session_state.result_df = df
            st.session_state.result_error = error
            st.session_state.rows_affected = affected
            st.session_state.has_run = True
            st.session_state.last_query = query

            status = "error" if error else "success"
            save_query(query, status)

    # ---------- Show Results ----------
    if st.session_state.has_run:

        if st.session_state.result_error:
            st.error(f"❌ Query Error: {st.session_state.result_error}")
        elif st.session_state.rows_affected is not None:
            st.success(f"✅ Query executed successfully — {st.session_state.rows_affected} row(s) affected")
        else:
            st.success("✅ Valid query")

        tabs_info = [
            ("Result", "📊"),
            ("Explain", "✨"),
            ("Order", "🔀"),
            ("Score", "⚡"),
            ("Interview", "🎯"),
        ]
        cols = st.columns(5)

        for col, (tab_name, icon) in zip(cols, tabs_info):
            with col:
                btn_type = "primary" if st.session_state.active_tab == tab_name else "secondary"
                if st.button(f"{icon} {tab_name}", key=f"tab_{tab_name}", type=btn_type, use_container_width=True):
                    st.session_state.active_tab = tab_name
                    st.rerun()

        st.write("")

        if st.session_state.active_tab == "Result":
            if st.session_state.result_error:
                st.info("This query did not run successfully, so there's no result to show. Check the Score tab for likely causes.")
            elif st.session_state.result_df is not None:
                df = st.session_state.result_df
                c1, c2 = st.columns(2)
                c1.metric("Rows returned", len(df))
                c2.metric("Columns", len(df.columns))
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("This statement doesn't return rows (e.g. UPDATE/INSERT/DELETE), so there's nothing to display here.")

        elif st.session_state.active_tab == "Explain":
            if "explanation" not in st.session_state or st.session_state.get("explained_query") != st.session_state.last_query:
                with st.spinner("Asking Gemini to explain this query..."):
                    explanation, error = explain_query(st.session_state.last_query)
                    st.session_state.explanation = explanation
                    st.session_state.explanation_error = error
                    st.session_state.explained_query = st.session_state.last_query

            if st.session_state.explanation_error:
                st.warning("⚠️ The AI service is temporarily busy (high demand on Google's servers). This usually resolves in a minute — try again.")
                if st.button("🔄 Retry", key="retry_explain"):
                    del st.session_state.explained_query
                    st.rerun()
            else:
                st.markdown(f"""
                <div style="background:#1F1E26;border:1px solid #2E2D36;border-radius:16px;padding:20px;">
                    <p style="font-size:12px;font-weight:700;color:#00C2D1;letter-spacing:1px;margin:0 0 10px;text-transform:uppercase;">✨ AI Explanation</p>
                    <p style="font-size:14px;line-height:1.7;color:#F4F3F6;margin:0;">{st.session_state.explanation}</p>
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.active_tab == "Order":
            order = get_execution_order(st.session_state.last_query)
            if order:
                st.write("**Actual execution sequence for this query:**")
                for i, step in enumerate(order, start=1):
                    st.write(f"{i}. `{step}`")
            else:
                st.info("No recognizable clauses found in this query.")

        elif st.session_state.active_tab == "Score":
            suggestions = analyze_query(st.session_state.last_query)
            score = calculate_score(suggestions)
            label, label_type = get_score_label(score)

            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric("Performance Score", f"{score}/100", label)
            with c2:
                st.progress(score / 100)

            st.write("")

            if suggestions:
                st.write(f"**{len(suggestions)} suggestion(s) found:**")
                for s in suggestions:
                    if s["severity"] == "warning":
                        st.warning(f"⚠️ {s['issue']}\n\n{s['suggestion']}")
                    else:
                        st.info(f"ℹ️ {s['issue']}\n\n{s['suggestion']}")
            else:
                st.success("✅ No issues found — this query looks optimized!")
                
        elif st.session_state.active_tab == "Interview":
            if "interview_questions" not in st.session_state or st.session_state.get("interview_query") != st.session_state.last_query:
                with st.spinner("Generating interview questions..."):
                    questions, error = generate_interview_questions(st.session_state.last_query)
                    st.session_state.interview_questions = questions
                    st.session_state.interview_error = error
                    st.session_state.interview_query = st.session_state.last_query

            if st.session_state.interview_error:
                st.warning("⚠️ The AI service is temporarily busy. Try again in a moment.")
                if st.button("🔄 Retry", key="retry_interview"):
                    del st.session_state.interview_query
                    st.rerun()
            else:
                st.markdown(f"""
                <div style="background:#1F1E26;border:1px solid #2E2D36;border-radius:16px;padding:20px;">
                    <p style="font-size:12px;font-weight:700;color:#F14E8A;letter-spacing:1px;margin:0 0 10px;text-transform:uppercase;">🎯 Practice Questions</p>
                    <p style="font-size:14px;line-height:1.8;color:#F4F3F6;margin:0;white-space:pre-line;">{st.session_state.interview_questions}</p>
                </div>
                """, unsafe_allow_html=True)                

# ====================== PAGE: LEARN ======================
elif st.session_state.current_page == "Learn":
    st.title("📖 Learn SQL Concepts")
    st.caption("Understand the fundamentals — no query needed.")

    for topic, content in LEARN_TOPICS.items():
        with st.expander(f"**{topic}**"):
            st.write(content["explanation"])
            st.code(content["example"], language="sql")
            