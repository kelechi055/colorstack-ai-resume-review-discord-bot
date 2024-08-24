import logging
import random
import discord
from discord.ext import commands

from config import GIF_LIST, RESUME_REVIEW_CHANNEL_ID, RESUME_REVIEW_TEST_CHANNEL_ID
from utils.resume_utils import review_resume
from utils.score_color import get_score_color


class ResumeBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name}')
        logging.info('Bot is ready to process messages and threads')
        
    async def on_message(self, message):
        logging.info(f"Message event received: {message.id} in channel {message.channel.parent_id}")

        # Avoid processing the bot's own messages
        if message.author == self.user:
            return

        # Verify that the message is part of the correct forum channel
        if message.channel.parent_id == RESUME_REVIEW_TEST_CHANNEL_ID or message.channel.parent_id == RESUME_REVIEW_CHANNEL_ID:
            logging.info(f"Message received in the correct resume review channel with ID: {message.channel.parent_id}")

            if message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.lower().endswith('.pdf'):
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
                            description="Currently, the resume review tool will only give feedback on your bullet points for experiences and projects. This does not serve as a complete resume review, so you should still seek feedback from peers. Additionally, this tool relies on AI and may not always provide the best feedback, so take it with a grain of salt.\n\n**Disclaimer:** Any suggestions provided are purely examples and should not be added as-is without verification of accuracy.",
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
            logging.info(f"Message is not in the specified forum channel")
            
def start_bot(token):
    # Discord Bot Setup
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = ResumeBot(command_prefix="!", intents=intents)
    bot.run(token)