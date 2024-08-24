import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment Variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
RESUME_REVIEW_TEST_CHANNEL_ID = int(os.getenv('RESUME_REVIEW_TEST_CHANNEL_ID'))  # Set this to your resume review test channel ID
RESUME_REVIEW_CHANNEL_ID = int(os.getenv('RESUME_REVIEW_CHANNEL_ID'))  # Set this to your resume review channel ID
HIGH_SCORE_COLOR = 0x00ff00
GOOD_SCORE_COLOR = 0x4BFFFF
LOW_SCORE_COLOR = 0xFFCF40
BAD_SCORE_COLOR = 0xFF4B4B
# List of celebration GIF URLs
GIFS = {
    "high_score_gifs": [
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDdzdm96cnU5bmRlem1xZG5uZHBwZG50d2txYWM0NnI5aWJ5bzZ0OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3m1fbOr4UttDYdZStA/giphy.gif", # Dancing
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2czZXQzbXU5dWI1ZW9tenc1cm95YzdlOG1tdmtmamd4NjV1NGdlNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MJs7EYwHyG8XC/giphy.gif", # Tupac dance
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2pwNXU3Mzl6eGpuZWNjdzN3dmlrajA3M3I2aWRodHVxeDl1bjNkeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KCEXGVZVL79mM/giphy.gif", # Excited crying
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGgycGRjaGM4NGRhaWh0Mnd2azlibHllcnRhMzl6MDNjZWplaDc2dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abldj0b3rxrZUxW/giphy.gif"  # Backflip
        
    ],
    "good_score_gifs": [
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWVldHMxNGl5bnhhaHJzbnIzOGY1dHd1NWw4NzU1dXA5ZW83YTFuZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l4ZyvMLEbaDRqhlzLq/giphy.gif", # Ate
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWNucTZ3b2w3dmtrZ29kcTR0Ym1ieGg2eWs2eDhvYTl3aTgzdG81MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MbRdUROzrpoPhEIkMq/giphy.gif", # Jobs not done
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3duOXUxdGk0Ym5idGwzZnVvbGZ0YTNqbnVoZ2RkdmpubzQyYnFuOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10AmJ6TIlbYxAk/giphy-downsized-large.gif",  # Sleep dance
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTcyMmR0ZDc4aWFuejBicXZnMXk0Z3Zyd3lkajV2ODZmYTF0cHRwbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yoJC2COHSxjIqadyZW/giphy.gif" # Dog celebrate 
    ],
    "low_score_gifs": [
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjJjbzVtb3A1eTl3aTQxODAzN2JjNWE2emxoeWdzZnF6OGNvZW11ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/41xwtMQgPhUEMASFmx/giphy.gif" # nervous excited
    ],
    "bad_score_gifs": [
        "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnp6ZmZmcmc5aXhwZzh6Nmt6b3drMmlpdWt3YXNrb2gyZTc3amxvcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MTZioYqK8rcPe/giphy.gif" # Learn Motivational
    ]
}