from config import HIGH_SCORE_COLOR, GOOD_SCORE_COLOR, LOW_SCORE_COLOR, BAD_SCORE_COLOR

# Function that outputs a color based on the input score
def get_score_color(score: int) -> int:
    if score >= 8:
        return HIGH_SCORE_COLOR
    elif score >= 6:
        return GOOD_SCORE_COLOR
    elif score >= 4:
        return LOW_SCORE_COLOR
    else:
        return BAD_SCORE_COLOR