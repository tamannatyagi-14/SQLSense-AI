import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def explain_query(sql_query):
    prompt = f"""You are a friendly SQL teacher helping a beginner understand a query.

Explain this SQL query in simple, plain English. Keep it short (3-4 sentences max).
Avoid technical jargon where possible. Focus on WHAT the query does and WHY, not just repeating the syntax.

SQL Query:
{sql_query}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text, None
    except Exception as e:
        return None, str(e)


def generate_sql_from_text(english_text, schema_info):
    schema_description = ""
    for table_name, info in schema_info.items():
        columns = ", ".join([col["name"] for col in info["columns"]])
        schema_description += f"- {table_name}({columns})\n"

    prompt = f"""You are a SQL generator. Convert the user's plain English request into a single valid SQLite query.

Database schema:
{schema_description}

Rules:
- Return ONLY the SQL query, nothing else. No explanation, no markdown, no code fences.
- Use only the tables and columns listed above.
- If the request is ambiguous, make a reasonable assumption.

User request: {english_text}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        sql = response.text.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        return sql, None
    except Exception as e:
        return None, str(e)

def generate_interview_questions(sql_query):
    prompt = f"""Based on the SQL concepts used in this query, generate 3 interview-style questions
that a recruiter might ask a candidate about these concepts.

Mix the question types — include at least one conceptual/theory question and one 
"what would this output" or coding-style question.

Format your response as plain numbered text like this:
1. [question]
2. [question]
3. [question]

Do not include answers, just the questions.

SQL Query:
{sql_query}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text, None
    except Exception as e:
        return None, str(e)