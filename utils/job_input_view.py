import discord
from discord.ui import Button, View

class JobInputView(View):
    def __init__(self, bot, message):
        super().__init__(timeout=60)
        self.bot = bot
        self.message = message

        yes_button = Button(label="Yes", style=discord.ButtonStyle.success)
        yes_button.callback = self.yes_button_callback
        self.add_item(yes_button)

        no_button = Button(label="No", style=discord.ButtonStyle.danger)
        no_button.callback = self.no_button_callback
        self.add_item(no_button)

    async def yes_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Great! Let's get started with the job description comparison.", ephemeral=True)
        
        # Step 2: Job Title
        await self.message.channel.send("🔖 **Job Title**: Please enter the job title for this role.")
        job_title = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=60)
        
        # Step 3: Company
        await self.message.channel.send("🔖 **Company**: Please enter the company for this role.")
        company = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=60)
        
        # Step 4: Minimum Qualifications
        await self.message.channel.send("💼 **Minimum Qualifications**: Please enter the minimum qualifications for the job.")
        min_qual = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=120)
        
        # Step 5: Preferred Qualifications
        await self.message.channel.send("📅 **Preferred Qualifications**: Please enter the preferred qualifications for the job.")
        pref_qual = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=120)
        
        job_details = {
            "job_title": job_title.content,
            "company": company.content,
            "minimum_qualifications": min_qual.content,
            "preferred_qualifications": pref_qual.content
        }
        
        # Confirm and process
        await self.message.channel.send(f"Thank you! Here’s what you provided:\n\n**Job Title**: {job_title.content}\n**Minimum Qualifications**: {min_qual.content}\n**Preferred Qualifications**: {pref_qual.content}")
        
        return job_details

    async def no_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("No problem! I'll just provide general resume formatting feedback.", ephemeral=True)