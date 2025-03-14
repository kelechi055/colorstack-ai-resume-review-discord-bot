import discord
from discord.ui import View, Button
import logging
from utils.analytics import analytics

class FeedbackView(View):
    def __init__(self, user_id, server_id):
        super().__init__(timeout=300)  # 5 minute timeout
        self.user_id = user_id
        self.server_id = server_id
        self.add_rating_buttons()
        
    def add_rating_buttons(self):
        # Add buttons for ratings 1-5
        for i in range(1, 6):
            button = Button(
                label=f"{i} {'⭐' * i}",
                style=discord.ButtonStyle.primary,
                custom_id=f"rating_{i}"
            )
            button.callback = self.rating_callback
            self.add_item(button)
    
    async def rating_callback(self, interaction):
        # Extract rating from button custom_id
        rating = int(interaction.data['custom_id'].split('_')[1])
        
        # Track the feedback rating
        analytics.track_feedback_rating(rating)
        
        # Create a thank you embed
        thank_you_embed = discord.Embed(
            title="Thank You for Your Feedback!",
            description=f"You rated this resume review {rating}/5 {'⭐' * rating}",
            color=0x00ff00
        )
        
        # Send the thank you message and disable the view
        await interaction.response.edit_message(embed=thank_you_embed, view=None)
        
        # Log the feedback
        logging.info(f"User {self.user_id} rated the resume review {rating}/5")
        
        # Stop listening for interactions
        self.stop() 