# Function to get emoji based on score
def get_score_emoji(score):
    if score >= 9: return "🌟"
    elif score >= 7: return "✨"
    elif score >= 5: return "👍"
    elif score >= 3: return "⚠️"
    else: return "❗"