def get_execution_order(query):
    query_upper = query.upper()
    
    execution_sequence = ["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY", "LIMIT"]
    
    present_clauses = []
    for clause in execution_sequence:
        if clause in query_upper:
            present_clauses.append(clause)
    
    return present_clauses