import asyncio
import logging
import random
import discord
from discord.ext import commands

from config import RESUME_REVIEW_CHANNEL_ID
from utils.gif_picker import get_gif
from utils.job_input_view import JobInputView
from utils.resume_utils import review_resume
from utils.score_color import get_score_color
from utils.score_emoji import get_score_emoji


class ResumeBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        self.job_details=None
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name}')
        logging.info('Bot is ready to process messages and threads')
    
    async def on_message(self, message):
        # logging.info(f"Message event received: {message.id} in channel {message.channel.parent_id}")

        # Avoid processing the bot's own messages
        if message.author == self.user:
            return

        # Verify that the message is part of the correct forum channel
        if isinstance(message.channel, discord.Thread) and message.channel.parent_id == RESUME_REVIEW_CHANNEL_ID:
            logging.info(f"Message received in the correct resume review channel with ID: {message.channel.parent_id}")

            if message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.lower().endswith('.pdf'):
                        logging.info(f"Processing attachment: {attachment.filename}")
                        
                        # Sending the initial feedback embed
                        main_embed = discord.Embed(
                            title="Do you have job posting to review for?",
                            color=0x0699ab
                        )
                        view = JobInputView(self, message)
                        message_with_view = await message.channel.send(embed=main_embed, view=view)
                        
                        await view.wait()
                        
                        if view.job_details:
                            self.job_details = view.job_details
                        else:
                            await message.channel.send("No job details provided. Providing general resume formatting feedback.")
                            self.job_details = None
                        
                        await message_with_view.delete()
                        
                        gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnlrNXdsdWRnbTA2ZTNjbHIxOG1jOGc4ZndpM3o2aWY2YW04d2cwdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/paKhPtCfM7RDQyRyGf/giphy.gif"  # Example GIF URL
                        loading_embed = discord.Embed(
                            title="This could take a minute or two -- our reviewer is hard at work! 😜",
                            color=0x0699ab
                        )
                        loading_embed.set_image(url=gif_url)
                        loading_embed.add_field(name="\u200b", value="• Inspired by [Oyster](https://github.com/colorstackorg/oyster) 🦪 •", inline=False)
                        loading_embed.set_footer(text="• Powered by ColorStack UF ResumeAI •")
                        loading_message = await message.channel.send(embed=loading_embed)

                        main_embed = discord.Embed(
                            title="AI Resume Feedback",
                            description="Currently, the resume review tool will only give feedback on your bullet points for experiences and projects, as well as, resume formatting. This does not serve as a complete resume review, so you should still seek feedback from peers. Additionally, this tool relies on AI and may not always provide the best feedback, so take it with a grain of salt.\n\n**Disclaimer:** Any suggestions provided are purely examples and should not be added as-is without verification of accuracy.\n\n**Note:** We are comparing your resume to Jake's resume for formatting feedback. You can view Jake's resume [here](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs).",
                            color=0x0699ab
                        )
                        await message.channel.send(embed=main_embed)
                        user_resume_bytes = await attachment.read()
                        jake_resume_bytes = open("resumes/jakes-resume.pdf", "rb").read()

                        try:
                            if self.job_details:
                                feedback = review_resume(resume_user=user_resume_bytes, resume_jake=jake_resume_bytes, job_title=self.job_details["job_title"], company=self.job_details["company"], min_qual=self.job_details["min_qual"], pref_qual=self.job_details["pref_qual"])
                            else:
                                feedback = review_resume(resume_user=user_resume_bytes, resume_jake=jake_resume_bytes)

                            # Log the feedback structure
                            logging.info(f"Feedback structure: {feedback}")

                            # Check if feedback is a dictionary
                            if not isinstance(feedback, dict):
                                logging.error("Feedback is not a dictionary.")
                                return

                            # Access experiences safely
                            experiences = feedback.get("experiences", [])
                            if not isinstance(experiences, list):
                                logging.error("Expected 'experiences' to be a list.")
                                return

                            logging.info(f"Experiences: {experiences}")  # Log the experiences

                            total_experiences_score = 0
                            total_projects_score = 0
                            total_formatting_score = 0
                            total_experiences_bullets = 0
                            total_projects_bullets = 0

                            for experience in experiences:
                                if isinstance(experience, dict):
                                    experience_embed = discord.Embed(title=f"**Experience at {experience.get('company', 'Unknown')} - {experience.get('role', 'Unknown')}**\n", color=0xe5e7eb)
                                    await message.channel.send(embed=experience_embed)
                                    bullets = experience.get('bullets', [])
                                    if not isinstance(bullets, list):
                                        logging.error("Expected 'bullets' to be a list.")
                                        continue

                                    for idx, bullet in enumerate(bullets):
                                        if isinstance(bullet, dict):
                                            total_experiences_score += bullet.get('score', 0)
                                            total_experiences_bullets += 1
                                            rewrites = "\n\n> ".join(bullet.get('rewrites', [])) if bullet.get('rewrites') else None
                                            bullet_embed = discord.Embed(title=f"{bullet.get('score', 0)}/10.0", color=get_score_color(bullet.get('score', 0)))
                                            bullet_embed.add_field(name="", value=f"> *{bullet.get('content', 'No content')}*\n", inline=False)
                                            bullet_embed.add_field(name="Feedback", value=f"> {bullet.get('feedback', 'No feedback')}\n", inline=False)
                                            if rewrites:
                                                bullet_embed.add_field(name="Suggestions ", value=f"> {rewrites}", inline=False)
                                            await message.channel.send(embed=bullet_embed)
                                        else:
                                            logging.error("Bullet item is not a dictionary.")
                                else:
                                    logging.error("Experience item is not a dictionary.")

                            avg_expereinces_final_score = 0 if total_experiences_bullets == 0 else total_experiences_score / total_experiences_bullets
                            expereinces_final_embed = discord.Embed(
                                title="Experience Section Score",
                                color=get_score_color(avg_expereinces_final_score)
                            )
                            expereinces_final_embed.add_field(name=f"{round(avg_expereinces_final_score,1)}/10.0", value="", inline=False)
                            await message.channel.send(embed=expereinces_final_embed)

                            # Projects Section
                            for project in feedback.get("projects", []):
                                project_embed = discord.Embed(title=f"**Project: {project['title']}**\n", color=0xe5e7eb)
                                await message.channel.send(embed=project_embed)
                                for idx, bullet in enumerate(project['bullets']):
                                    total_projects_score += bullet['score']
                                    total_projects_bullets += 1
                                    rewrites = "\n\n> ".join(bullet['rewrites']) if bullet['rewrites'] else None
                                    bullet_embed = discord.Embed(title=f"{bullet['score']}/10.0", color=get_score_color(bullet['score']))
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
                            projects_final_embed.add_field(name=f"{round(avg_projects_final_score, 1)}/10.0", value="", inline=False)
                            await message.channel.send(embed=projects_final_embed)
                            
                            # Formatting Feedback Section
                            formatting = feedback.get("formatting")
                            logging.info("Formatting: ", formatting)
                            if formatting:
                                total_formatting_score = formatting['overall_score']
                                formatting_embed = discord.Embed(title="📄 Resume Formatting Feedback", color=0xe5e7eb)
                                await message.channel.send(embed=formatting_embed)
                                
                                # Add fields for each formatting aspect
                                for aspect in ['font_consistency', 'font_choice', 'font_size', 'alignment', 'margins', 
                                            'line_spacing', 'section_spacing', 'headings', 'bullet_points', 
                                            'contact_information', 'overall_layout', 'page_utilization', 'is_single_page', 'consistency']:
                                    if aspect in formatting:
                                        formatting_embed = discord.Embed(title=f"**{aspect.replace('_', ' ').title()}**", color=get_score_color(formatting['overall_score']))
                                        aspect_data = formatting[aspect]
                                        emoji = "✅" if not aspect_data['issue'] else "❌"
                                        score_emoji = get_score_emoji(aspect_data['score'])
                                        field_name = f"{emoji} {aspect.replace('_', ' ').title()}: {aspect_data['score']}/10.0 {score_emoji}"
                                        field_value = f"{aspect_data['feedback']}"
                                        suggestions = "\n\n> ".join(aspect_data['suggestions']) if 'suggestions' in aspect_data and aspect_data['suggestions'][0] != "" else None
                                        formatting_embed.add_field(name=field_name, value=field_value, inline=False)
                                        if suggestions:
                                            formatting_embed.add_field(name="Suggestions ", value=f"> {suggestions}", inline=False)
                                    await message.channel.send(embed=formatting_embed)
                                
                                # Overall score
                                overall_score = formatting['overall_score']
                                overall_score_embed = discord.Embed(title="Formatting Score", color=get_score_color(overall_score))
                                overall_score_embed.add_field(name=f"{round(overall_score,1)}/10.0", value="", inline=False)
                                await message.channel.send(embed=overall_score_embed)

                            final_score = (avg_projects_final_score + avg_expereinces_final_score + total_formatting_score) / 3.0  # Ensure float division
                            gif_url = get_gif(final_score)
                            # Completion message
                            final_embed = discord.Embed(
                                title="AI Resume Review Complete! 🎉",
                                color=get_score_color(final_score)
                            )
                            final_embed.set_image(url=gif_url)
                            final_embed.add_field(name="\u200b", value="• Inspired by [Oyster](https://github.com/colorstackorg/oyster) 🦪 •", inline=False)
                            final_embed.set_footer(text="• Powered by ColorStack UF ResumeAI •")
                            await loading_message.edit(embed=final_embed)
                            
                            final_score_embed = discord.Embed(title=f"Final Score: {round(final_score, 1)}/10.0", color=get_score_color(final_score))
                            final_score_embed.set_image(url=gif_url)
                            final_score_embed.add_field(name="\u200b", value="• Inspired by [Oyster](https://github.com/colorstackorg/oyster) 🦪 •", inline=False)
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