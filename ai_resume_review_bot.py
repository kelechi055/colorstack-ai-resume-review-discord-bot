import logging
import random
import discord
from discord.ext import commands

from config import RESUME_REVIEW_CHANNEL_ID, RESUME_REVIEW_TEST_CHANNEL_ID
from utils.gif_picker import get_gif
from utils.job_input_view import JobInputView
from utils.resume_utils import review_resume
from utils.score_color import get_score_color
from utils.score_emoji import get_score_emoji


class ResumeBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name}')
        logging.info('Bot is ready to process messages and threads')
    
    async def on_message(self, message):
        # logging.info(f"Message event received: {message.id} in channel {message.channel.parent_id}")

        # Avoid processing the bot's own messages
        if message.author == self.user:
            return

        # Verify that the message is part of the correct forum channel
        if isinstance(message.channel, discord.Thread) and message.channel.parent_id == RESUME_REVIEW_TEST_CHANNEL_ID or message.channel.parent_id == RESUME_REVIEW_CHANNEL_ID:
            logging.info(f"Message received in the correct resume review channel with ID: {message.channel.parent_id}")

            if message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.lower().endswith('.pdf'):
                        logging.info(f"Processing attachment: {attachment.filename}")
                        
                        # Sending the initial feedback embed
                        main_embed = discord.Embed(
                            title="AI Resume Feedback",
                            description="Would you like to proceed with the review?",
                            color=0x0699ab
                        )
                        view = JobInputView(self, message)
                        message_with_view = await message.channel.send(embed=main_embed, view=view)
                        
                        # Wait for user interaction
                        await view.wait()
                        
                        if view.value is None:
                            await message.channel.send("No response received. Review canceled.")
                        elif view.value:
                            await message.channel.send("Proceeding with the review...")
                            # Place the logic for processing the resume here
                        else:
                            await message.channel.send("Review canceled.")
                        
                        job_input_view = JobInputView(self, message)
                        
                        gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnlrNXdsdWRnbTA2ZTNjbHIxOG1jOGc4ZndpM3o2aWY2YW04d2cwdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/paKhPtCfM7RDQyRyGf/giphy.gif"  # Example GIF URL
                        loading_embed = discord.Embed(
                            title="This could take a minute or two -- our reviewer is hard at work! 😜",
                            color=0x0699ab
                        )
                        loading_embed.set_image(url=gif_url)
                        loading_embed.set_footer(text="• Powered by ColorStack UF ResumeAI •\n•       Inspired by [Oyster](https://github.com/colorstackorg/oyster) 🦪      •")
                        loading_message = await message.channel.send(embed=loading_embed)

                        main_embed = discord.Embed(
                            title="AI Resume Feedback",
                            description="Currently, the resume review tool will only give feedback on your bullet points for experiences and projects, as well as, resume formatting. This does not serve as a complete resume review, so you should still seek feedback from peers. Additionally, this tool relies on AI and may not always provide the best feedback, so take it with a grain of salt.\n\n**Disclaimer:** Any suggestions provided are purely examples and should not be added as-is without verification of accuracy.",
                            color=0x0699ab
                        )
                        await message.channel.send(embed=main_embed)
                        pdf_bytes = await attachment.read()
                        try:
                            feedback = review_resume(resume=pdf_bytes)
                            
                            total_experiences_score = 0
                            total_projects_score = 0
                            total_formatting_score = 0
                            total_experiences_bullets = 0
                            total_projects_bullets = 0

                            # Experiences Section
                            for experience in feedback.get("experiences", []):
                                experience_embed = discord.Embed(title=f"**Experience at {experience['company']} - {experience['role']}**\n", color=0xe5e7eb)
                                await message.channel.send(embed=experience_embed)
                                for idx, bullet in enumerate(experience['bullets']):
                                    total_experiences_score += bullet['score']
                                    total_experiences_bullets += 1
                                    rewrites = "\n\n> ".join(bullet['rewrites']) if bullet['rewrites'] else None
                                    bullet_embed = discord.Embed(title=f"{bullet['score']}/10", color=get_score_color(bullet['score']))
                                    bullet_embed.add_field(name="", value=f"> *{bullet['content']}*\n", inline=False)
                                    bullet_embed.add_field(name="Feedback", value=f"> {bullet['feedback']}\n", inline=False)
                                    if rewrites:
                                        bullet_embed.add_field(name="Suggestions ", value=f"> {rewrites}", inline=False)
                                    await message.channel.send(embed=bullet_embed)
                                    
                            avg_expereinces_final_score = 0 if total_experiences_bullets == 0 else total_experiences_score / total_experiences_bullets
                            expereinces_final_embed = discord.Embed(
                                title="Experience Section Score",
                                color=get_score_color(avg_expereinces_final_score)
                            )
                            expereinces_final_embed.add_field(name=f"{round(avg_expereinces_final_score,1)}/10", value="", inline=False)
                            await message.channel.send(embed=expereinces_final_embed)

                            # Projects Section
                            for project in feedback.get("projects", []):
                                project_embed = discord.Embed(title=f"**Project: {project['title']}**\n", color=0xe5e7eb)
                                await message.channel.send(embed=project_embed)
                                for idx, bullet in enumerate(project['bullets']):
                                    total_projects_score += bullet['score']
                                    total_projects_bullets += 1
                                    rewrites = "\n\n> ".join(bullet['rewrites']) if bullet['rewrites'] else None
                                    bullet_embed = discord.Embed(title=f"{bullet['score']}/10", color=get_score_color(bullet['score']))
                                    bullet_embed.add_field(name="", value=f"> *{bullet['content']}*\n", inline=False)
                                    bullet_embed.add_field(name="Feedback", value=f"> {bullet['feedback']}\n", inline=False)
                                    if rewrites:
                                        bullet_embed.add_field(name="Suggestions ", value=f"> {rewrites}", inline=False)
                                    await message.channel.send(embed=bullet_embed)
                                    
                            avg_projects_final_score = 0 if total_projects_bullets == 0 else total_projects_score / total_projects_bullets
                            projects_final_embed = discord.Embed(
                                title="Project Section Score",
                                color=get_score_color(avg_projects_final_score)
                            )
                            projects_final_embed.add_field(name=f"{round(avg_projects_final_score, 1)}/10", value="", inline=False)
                            await message.channel.send(embed=projects_final_embed)
                            
                            # Formatting Feedback Section
                            formatting = feedback.get("formatting")
                            if formatting:
                                total_formatting_score = formatting['overall_score']
                                formatting_embed = discord.Embed(title="📄 Resume Formatting Feedback", color=get_score_color(formatting['overall_score']))

                                # Add fields for each formatting aspect
                                for aspect in ['font_consistency', 'font_choice', 'font_size', 'alignment', 'margins', 
                                            'line_spacing', 'section_spacing', 'headings', 'bullet_points', 
                                            'contact_information', 'overall_layout', 'page_utilization', 'consistency']:
                                    if aspect in formatting:
                                        aspect_data = formatting[aspect]
                                        emoji = "✅" if not aspect_data['issue'] else "❌"
                                        score_emoji = get_score_emoji(aspect_data['score'])
                                        field_name = f"{emoji} {aspect.replace('_', ' ').title()}: {aspect_data['score']}/10 {score_emoji}"
                                        field_value = f"{aspect_data['feedback']}"
                                        formatting_embed.add_field(name=field_name, value=field_value, inline=False)

                                await message.channel.send(embed=formatting_embed)
                                
                                # Overall score
                                overall_score = formatting['overall_score']
                                overall_score_embed = discord.Embed(title="Formatting Score", color=get_score_color(overall_score))
                                overall_score_embed.add_field(name=f"{round(overall_score,1)}/10", value="", inline=False)
                                await message.channel.send(embed=overall_score_embed)

                            final_score = (avg_projects_final_score + avg_expereinces_final_score + total_formatting_score) / 3
                            gif_url = get_gif(final_score)
                            # Completion message
                            final_embed = discord.Embed(
                                title="AI Resume Review Complete! 🎉",
                                color=get_score_color(final_score)
                            )
                            final_embed.set_image(url=gif_url)
                            final_embed.set_footer(text="• Powered by ColorStack UF ResumeAI •")
                            await loading_message.edit(embed=final_embed)
                            
                            final_score_embed = discord.Embed(title=f"Final Score: {round(final_score, 1)}/10", color=get_score_color(final_score))
                            final_score_embed.set_image(url=gif_url)
                            final_score_embed.set_footer(text="• Powered by ColorStack UF ResumeAI •")
                            await message.channel.send(embed=final_score_embed)
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