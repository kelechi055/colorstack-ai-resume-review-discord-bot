from config import GIFS
import random

# Function that outputs a color based on the input score
def get_gif(score: int) -> int:
    if score >= 8:
        return random.choice(GIFS['high_score_gifs'])
    elif score >= 6:
        return random.choice(GIFS['good_score_gifs'])
    elif score >= 4:
        return random.choice(GIFS['low_score_gifs'])
    else:
        return random.choice(GIFS['bad_score_gifs'])