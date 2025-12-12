def match_team(users, event):
    # Complementary skill matching logic (simple version)
    sorted_users = sorted(users, key=lambda u: u["experience"], reverse=True)
    return sorted_users[:4]
