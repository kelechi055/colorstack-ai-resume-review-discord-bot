import asyncio
import random
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from pdf2image import convert_from_bytes
from io import BytesIO
import base64
from pydantic import BaseModel, Field, ValidationError
import requests
import json
import logging

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
GIF_LIST = [
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWNucTZ3b2w3dmtrZ29kcTR0Ym1ieGg2eWs2eDhvYTl3aTgzdG81MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MbRdUROzrpoPhEIkMq/giphy.gif", # Jobs not done
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2R2cHdhaDhwNnI2cHp4aXNiamlrdjkyd2I2eWRqbjgwZ2o3bWxhNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QlCxsMYJ6HI71k92mG/giphy.gif",  # Clapping Robot
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3duOXUxdGk0Ym5idGwzZnVvbGZ0YTNqbnVoZ2RkdmpubzQyYnFuOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10AmJ6TIlbYxAk/giphy-downsized-large.gif",  # Sleep dance
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGgycGRjaGM4NGRhaWh0Mnd2azlibHllcnRhMzl6MDNjZWplaDc2dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7abldj0b3rxrZUxW/giphy.gif",  # Backflip
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTcyMmR0ZDc4aWFuejBicXZnMXk0Z3Zyd3lkajV2ODZmYTF0cHRwbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yoJC2COHSxjIqadyZW/giphy.gif" # Dog celebrate
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnp6ZmZmcmc5aXhwZzh6Nmt6b3drMmlpdWt3YXNrb2gyZTc3amxvcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MTZioYqK8rcPe/giphy.gif", # Learn Motivational
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjJjbzVtb3A1eTl3aTQxODAzN2JjNWE2emxoeWdzZnF6OGNvZW11ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/41xwtMQgPhUEMASFmx/giphy.gif", # nervous excited
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWVldHMxNGl5bnhhaHJzbnIzOGY1dHd1NWw4NzU1dXA5ZW83YTFuZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l4ZyvMLEbaDRqhlzLq/giphy.gif", # Ate
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2czZXQzbXU5dWI1ZW9tenc1cm95YzdlOG1tdmtmamd4NjV1NGdlNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MJs7EYwHyG8XC/giphy.gif", # Tupac dance
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDdzdm96cnU5bmRlem1xZG5uZHBwZG50d2txYWM0NnI5aWJ5bzZ0OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3m1fbOr4UttDYdZStA/giphy.gif", # Dancing
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2pwNXU3Mzl6eGpuZWNjdzN3dmlrajA3M3I2aWRodHVxeDl1bjNkeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KCEXGVZVL79mM/giphy.gif" # Excited crying
]


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Pydantic Models for Validation
class ResumeBullet(BaseModel):
    content: str = Field(..., description="Content of the resume bullet")
    feedback: str = Field(..., description="Feedback on the resume bullet")
    rewrites: list[str] = Field(default=[], max_items=2, description="Possible rewrites for the resume bullet")
    score: int = Field(..., ge=1, le=10, description="Score for the resume bullet")

class ResumeExperience(BaseModel):
    bullets: list[ResumeBullet] = Field(..., description="List of resume bullets for the experience")
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Role at the company")

class ResumeProject(BaseModel):
    bullets: list[ResumeBullet] = Field(..., description="List of resume bullets for the project")
    title: str = Field(..., description="Title of the project")

class ResumeFeedback(BaseModel):
    experiences: list[ResumeExperience] = Field(..., description="List of experiences in the resume")
    projects: list[ResumeProject] = Field(..., description="List of projects in the resume")

# Convert PDF to Image (Base64)
def convert_pdf_to_image(file: bytes) -> str:
    images = convert_from_bytes(file, first_page=1, last_page=1)
    buffered = BytesIO()
    images[0].save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    logging.info("Converted PDF to Base64 image successfully")
    return img_base64

# Function to Get Chat Completion from Anthropic
def get_chat_completion(max_tokens: int, messages: list, system: str = None, temperature: float = 0.5) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01',
        'x-api-key': ANTHROPIC_API_KEY,
    }
    data = {
        'messages': messages,
        'model': 'claude-3-5-sonnet-20240620',
        'max_tokens': max_tokens,
        'temperature': temperature,
    }
    if system:
        data['system'] = system

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.text
        except (requests.HTTPError, ConnectionError, requests.RequestException, ValueError) as err:
            logging.error("Error during API request attempt %d: %s", attempt + 1, err)
            if attempt < retries - 1:
                logging.info("Retrying...")
                asyncio.sleep(2)
            else:
                logging.error("Failed after %d attempts", retries)
                raise
    
    # response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if not response.ok:
        logging.error(f"Failed to fetch chat completion from Anthropic. Status: {response.status_code}, Response: {response.text}")
        raise Exception(f"Failed to fetch chat completion from Anthropic. Status: {response.status_code}, Response: {response.text}")

    json_response = response.json()
    logging.info("Received chat completion from Anthropic successfully")
    return json_response.get('completion', '').strip()

# Function to Review Resume
def review_resume(resume: bytes) -> dict:
    system_prompt = """
    You are the best resume reviewer in the world, specifically for resumes aimed at getting a software engineering internship/new grad role.
    Here are your guidelines for a great bullet point:
    - It starts with a strong action verb.
    - It is specific.
    - It talks about achievements.
    - It is concise. No fluff.
    - If possible, it quantifies impact. Don't be as critical about this for projects as you are for work experiences.
    Here are your guidelines for giving feedback:
    - Be kind.
    - Be specific.
    - Be actionable.
    - Ask questions (ie: "how many...", "how much...", "what was the impact...").
    - Don't be overly nit-picky.
    - If the bullet point is NOT a 10/10, then the last sentence of your feedback MUST be an actionable improvement item.
    Here are your guidelines for rewriting bullet points:
    - If the original bullet point is a 10/10, do NOT suggest any rewrites.
    - If the original bullet point is not a 10/10, suggest 1-2 rewrite options.
    - Be 1000% certain that the rewrites address all of your feedback.
    """

    user_prompt = """
    Please review this resume. Only return JSON that respects the following schema:
    experiences: [
        {
            bullets: [
                {
                    content: string,
                    feedback: string,
                    rewrites: [string, string],
                    score: number
                }
            ],
            company: string,
            role: string
        }
    ],
    projects: [
        {
            bullets: [
                {
                    content: string,
                    feedback: string,
                    rewrites: [string, string],
                    score: number
                }
            ],
            title: string
        }
    ]
    """

    image_base64 = convert_pdf_to_image(resume)
    
    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': user_prompt},
                {'type': 'image', 'source': {'data': image_base64, 'media_type': 'image/png', 'type': 'base64'}}
            ]
        }
    ]
    
    try:
        completion = get_chat_completion(max_tokens=8192, messages=messages, system=system_prompt, temperature=0.25)
        result = json.loads(completion)
        logging.info(result['content'][0]['text'])
        resume_feedback = ResumeFeedback(**json.loads(result['content'][0]['text']))
        logging.info("Resume reviewed and feedback generated successfully")
        resume_feedback_model = resume_feedback.dict()
        logging.info(resume_feedback_model)
        return resume_feedback.dict()
    except ValidationError as e:
        logging.error(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error processing resume: {str(e)}")
        raise
    
def get_score_color(score: str) -> hex:
    color = None
    if score == 10:
        color = HIGH_SCORE_COLOR
    elif score >= 7:
        color = GOOD_SCORE_COLOR
    elif score == 6:
        color = LOW_SCORE_COLOR
    else:
        color = BAD_SCORE_COLOR
    return color

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')
    logging.info('Bot is ready to process messages and threads')

@bot.event
async def on_message(message):
    logging.info(f"Message event received: {message.id} in channel {message.channel.parent_id}")

    # Avoid processing the bot's own messages
    if message.author == bot.user:
        return

    # Verify that the message is part of the correct forum channel
    if message.channel.parent_id == RESUME_REVIEW_TEST_CHANNEL_ID or message.channel.parent_id == RESUME_REVIEW_CHANNEL_ID:
        logging.info(f"Message received in the correct resume review channel with ID: {message.channel.parent_id}")

        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.lower().endswith('.pdf'):
                    logging.info(f"Processing attachment: {attachment.filename}")
                    logging.info(f"Processing attachment: {attachment.filename}")
                    
                    gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnlrNXdsdWRnbTA2ZTNjbHIxOG1jOGc4ZndpM3o2aWY2YW04d2cwdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/paKhPtCfM7RDQyRyGf/giphy.gif"  # Example GIF URL
                    loading_embed = discord.Embed(
                        title="This could take a minute or two -- our reviewer is hard at work! 😜",
                        color=0x0699ab
                    )
                    loading_embed.set_image(url=gif_url)
                    loading_message = await message.channel.send(embed=loading_embed)

                    main_embed = discord.Embed(
                        title="AI Resume Feedback",
                        description="Currently, the resume review tool will only give feedback on your bullet points for experiences and projects. This does not serve as a complete resume review, so you should still seek feedback from peers. Additionally, this tool relies on AI and may not always provide the best feedback, so take it with a grain of salt.",
                        color=0x0699ab
                    )
                    await message.channel.send(embed=main_embed)
                    pdf_bytes = await attachment.read()
                    try:
                        feedback = review_resume(resume=pdf_bytes)

                        # Experiences Section
                        for experience in feedback.get("experiences", []):
                            experience_embed = discord.Embed(title=f"**Experience at {experience['company']} - {experience['role']}**\n", color=0xe5e7eb)
                            await message.channel.send(embed=experience_embed)
                            for idx, bullet in enumerate(experience['bullets']):
                                rewrites = "\n\n> ".join(bullet['rewrites']) if bullet['rewrites'] else None
                                bullet_embed = discord.Embed(title=f"{bullet['score']}/10", color=get_score_color(bullet['score']))
                                bullet_embed.add_field(name="", value=f"> *{bullet['content']}*\n", inline=False)
                                bullet_embed.add_field(name="Feedback", value=f"> {bullet['feedback']}\n", inline=False)
                                if rewrites:
                                    bullet_embed.add_field(name="Suggestions ", value=f"> {rewrites}", inline=False)
                                await message.channel.send(embed=bullet_embed)

                        # Projects Section
                        for project in feedback.get("projects", []):
                            project_embed = discord.Embed(title=f"**Project: {project['title']}**\n", color=0xe5e7eb)
                            await message.channel.send(embed=project_embed)
                            for idx, bullet in enumerate(project['bullets']):
                                rewrites = "\n\n> ".join(bullet['rewrites']) if bullet['rewrites'] else None
                                bullet_embed = discord.Embed(title=f"{bullet['score']}/10", color=get_score_color(bullet['score']))
                                bullet_embed.add_field(name="", value=f"> *{bullet['content']}*\n", inline=False)
                                bullet_embed.add_field(name="Feedback", value=f"> {bullet['feedback']}\n", inline=False)
                                if rewrites:
                                    bullet_embed.add_field(name="Suggestions ", value=f"> {rewrites}", inline=False)
                                await message.channel.send(embed=bullet_embed)

                        gif_url = random.choice(GIF_LIST)
                        # Completion message
                        final_embed = discord.Embed(
                            title="AI Resume Review Complete! 🎉",
                            color=0x0699ab
                        )
                        final_embed.set_image(url=gif_url)
                        await loading_message.edit(embed=final_embed)
                    except Exception as e:
                        logging.error(f"Failed to process PDF attachment: {e}")
    else:
        logging.debug(f"Message is not in the specified forum channel")

# Run the bot
bot.run(DISCORD_TOKEN)