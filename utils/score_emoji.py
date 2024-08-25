# Function to get emoji based on score
def get_score_emoji(score):
    if score >= 8: return "🌟"
    elif score >= 6: return "✨"
    elif score >= 4: return "⚠️"
    else: return "❗"