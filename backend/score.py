def calculate_score(suggestions):
    score = 100

    for s in suggestions:
        if s["severity"] == "warning":
            score -= 15
        elif s["severity"] == "info":
            score -= 7

    score = max(score, 0)

    return score

def get_score_label(score):
    if score >= 85:
        return "Excellent", "success"
    elif score >= 60:
        return "Good", "info"
    else:
        return "Needs improvement", "warning"