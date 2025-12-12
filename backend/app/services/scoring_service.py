def calculate_fit_score(user, event):
    score = 0

    if any(skill in event["skills"] for skill in user["skills"]):
        score += 40

    if user["interests"] in event["category"]:
        score += 30

    if user["experience"] >= event["difficulty"]:
        score += 30

    return min(score, 100)
