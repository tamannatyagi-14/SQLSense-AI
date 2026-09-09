import re

def analyze_query(query):
    query_upper = query.upper()
    suggestions = []

    def add(issue, suggestion, severity):
        suggestions.append({"issue": issue, "suggestion": suggestion, "severity": severity})

    # 1. SELECT *
    if re.search(r"SELECT\s+\*", query_upper):
        add(
            "Using SELECT *",
            "Avoid SELECT * — specify only the columns you need. This reduces data transfer and makes your query faster and clearer.",
            "warning"
        )

    # 2. Missing WHERE on a SELECT
    if re.search(r"\bSELECT\b", query_upper) and not re.search(r"\bWHERE\b", query_upper):
        add(
            "No WHERE clause found",
            "Without a WHERE clause, this query scans the entire table. Add a WHERE condition if you only need specific rows.",
            "info"
        )

    # 3. ORDER BY without LIMIT
    if re.search(r"\bORDER BY\b", query_upper) and not re.search(r"\bLIMIT\b", query_upper):
        add(
            "ORDER BY without LIMIT",
            "Sorting large result sets is expensive. If you don't need all rows, add a LIMIT to improve performance.",
            "info"
        )

    # 4. JOIN without ON or USING
    if re.search(r"\bJOIN\b", query_upper) and not re.search(r"\bON\b", query_upper) and not re.search(r"\bUSING\b", query_upper):
        add(
            "JOIN without ON condition",
            "A JOIN without an ON condition creates a cartesian product (every row matched with every row), which can produce huge, incorrect results.",
            "warning"
        )

    # 5. UPDATE without WHERE — very dangerous
    if re.search(r"^\s*UPDATE\b", query_upper) and not re.search(r"\bWHERE\b", query_upper):
        add(
            "UPDATE without WHERE",
            "This will update EVERY row in the table. If that's not intended, add a WHERE clause to target specific rows.",
            "warning"
        )

    # 6. DELETE without WHERE — very dangerous
    if re.search(r"^\s*DELETE\b", query_upper) and not re.search(r"\bWHERE\b", query_upper):
        add(
            "DELETE without WHERE",
            "This will delete EVERY row in the table. If that's not intended, add a WHERE clause to target specific rows.",
            "warning"
        )

    # 7. HAVING without GROUP BY
    if re.search(r"\bHAVING\b", query_upper) and not re.search(r"\bGROUP BY\b", query_upper):
        add(
            "HAVING without GROUP BY",
            "HAVING is meant to filter grouped results. Without GROUP BY, you probably want WHERE instead.",
            "info"
        )

    # 8. Aggregate function used inside WHERE (should be HAVING)
    where_idx = query_upper.find("WHERE")
    if where_idx != -1:
        end_idx = len(query_upper)
        for kw in ["GROUP BY", "ORDER BY", "HAVING", "LIMIT"]:
            idx = query_upper.find(kw, where_idx)
            if idx != -1 and idx < end_idx:
                end_idx = idx
        where_clause = query_upper[where_idx:end_idx]
        if re.search(r"\b(COUNT|SUM|AVG|MIN|MAX)\s*\(", where_clause):
            add(
                "Aggregate function inside WHERE",
                "Aggregate functions like COUNT, SUM, AVG can't be used in WHERE. Use HAVING instead, since WHERE runs before grouping happens.",
                "warning"
            )

        # 9. Function wrapped around a column in WHERE (blocks index usage)
        if re.search(r"\b(UPPER|LOWER|TRIM|SUBSTR)\s*\(", where_clause):
            add(
                "Function applied to a column in WHERE",
                "Wrapping a column in a function (e.g. UPPER(name) = ...) prevents SQLite from using an index on that column, making the query slower.",
                "info"
            )

    # 10. LIKE with a leading wildcard
    if re.search(r"LIKE\s+'%", query_upper):
        add(
            "LIKE pattern starts with %",
            "A leading % (e.g. LIKE '%smith') can't use an index and forces a full table scan. A trailing wildcard (e.g. LIKE 'smith%') is faster.",
            "info"
        )

    # 11. NOT IN with a subquery (NULL trap)
    if re.search(r"NOT\s+IN\s*\(\s*SELECT", query_upper):
        add(
            "NOT IN with a subquery",
            "If the subquery can return NULL, NOT IN may unexpectedly return zero rows. NOT EXISTS is usually safer.",
            "warning"
        )

    # 12. DISTINCT combined with JOIN (possible sign of duplicate rows)
    if re.search(r"\bDISTINCT\b", query_upper) and re.search(r"\bJOIN\b", query_upper):
        add(
            "DISTINCT used with JOIN",
            "Needing DISTINCT after a JOIN often means the join is producing duplicate rows. Double-check your join condition.",
            "info"
        )

    # 13. Repeated OR on the same column (could use IN)
    if re.search(r"(\w+)\s*=\s*\S+\s+OR\s+\1\s*=", query_upper):
        add(
            "Multiple OR conditions on the same column",
            "Instead of col = 'A' OR col = 'B' OR col = 'C', use col IN ('A', 'B', 'C') — it's cleaner and often faster.",
            "info"
        )

    return suggestions