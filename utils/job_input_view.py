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
        
        # Step 2: Job Title (Optional)
        await self.message.channel.send("🔖 **Job Title**: Please enter the job title for this role.")
        job_title = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=60)
        
        # Step 3: Key Responsibilities
        await self.message.channel.send("📝 **Key Responsibilities**: Please list the key responsibilities for this role. You can separate each responsibility with a comma.")
        responsibilities = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=120)
        
        # Step 4: Required Skills
        await self.message.channel.send("💼 **Minimum Qualifications**: Please enter the minimum qualifications for the job.")
        skills = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=120)
        
        # Step 5: Experience Requirements
        await self.message.channel.send("📅 **Experience Requirements**: Please specify the required experience, such as years in the field or specific types of experience.")
        experience = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=120)
        
        # Step 6: Educational Requirements
        await self.message.channel.send("🎓 **Educational Requirements**: Please specify the required educational qualifications.")
        education = await self.bot.wait_for('message', check=lambda m: m.author == self.message.author, timeout=120)
        
        # Confirm and process
        await self.message.channel.send(f"Thank you! Here’s what you provided:\n\n**Job Title**: {job_title.content}\n**Responsibilities**: {responsibilities.content}\n**Required Skills**: {skills.content}\n**Experience**: {experience.content}\n**Education**: {education.content}")

    async def no_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("No problem! I'll just provide general resume formatting feedback.", ephemeral=True)