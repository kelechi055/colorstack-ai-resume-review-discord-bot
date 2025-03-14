# Deployment Guide for ColorStack AI Resume Review Discord Bot

This guide provides step-by-step instructions for deploying the ColorStack AI Resume Review Discord Bot to various platforms.

## Pre-Deployment Checklist

Before deploying, ensure you have:

1. A Discord Bot Token (from the [Discord Developer Portal](https://discord.com/developers/applications))
2. An Anthropic API Key (from [Anthropic](https://console.anthropic.com/))
3. The ID of your resume review forum channel
4. A reference resume PDF named `jakes-resume.pdf` in the `resumes/` directory

## Option 1: Heroku Deployment

### 1. Set Up Heroku

```bash
# Install the Heroku CLI if you haven't already
brew install heroku/brew/heroku  # macOS
# or
curl https://cli-assets.heroku.com/install.sh | sh  # Linux

# Login to Heroku
heroku login
```

### 2. Create a Heroku App

```bash
# Create a new Heroku app
heroku create colorstack-resume-review-bot
```

### 3. Configure Environment Variables

```bash
# Set required environment variables
heroku config:set DISCORD_TOKEN=your_discord_bot_token
heroku config:set ANTHROPIC_API_KEY=your_anthropic_api_key
heroku config:set RESUME_REVIEW_CHANNEL_ID=your_channel_id
```

### 4. Deploy the Bot

```bash
# Push your code to Heroku
git push heroku main

# Scale the worker dyno (this starts the bot)
heroku ps:scale worker=1
```

### 5. Monitor the Bot

```bash
# View logs to ensure the bot is running correctly
heroku logs --tail
```

## Option 2: Replit Deployment

### 1. Set Up Replit

1. Create an account on [replit.com](https://replit.com) if you don't have one
2. Click "Create Repl" and select "Import from GitHub"
3. Enter your GitHub repository URL and click "Import"

### 2. Configure Environment Variables

1. Click on the padlock icon in the sidebar to open the Secrets panel
2. Add the following secrets:
   - `DISCORD_TOKEN`: Your Discord bot token
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `RESUME_REVIEW_CHANNEL_ID`: Your forum channel ID

### 3. Add Configuration Files

1. Create a `.replit` file with the following content:
   ```
   run = "python main.py"
   ```

2. Create a `pyproject.toml` file with your dependencies

### 4. Deploy and Run

1. Click the "Run" button to start the bot
2. Enable the "Always On" feature if you have Replit Hacker Plan

## Option 3: Railway Deployment

### 1. Set Up Railway

1. Create an account on [railway.app](https://railway.app)
2. Click "New Project" and select "Deploy from GitHub repo"
3. Connect your GitHub account and select your repository

### 2. Configure Environment Variables

1. Go to the "Variables" tab in your project
2. Add the following variables:
   - `DISCORD_TOKEN`: Your Discord bot token
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `RESUME_REVIEW_CHANNEL_ID`: Your forum channel ID

### 3. Deploy the Bot

1. Railway will automatically deploy your bot when you push changes to your repository
2. Monitor the deployment in the "Deployments" tab

## Option 4: Cloud VM Deployment (Oracle/Google Cloud)

### 1. Set Up a VM

1. Create a VM instance on Oracle Cloud or Google Cloud
2. SSH into your VM

### 2. Install Dependencies

```bash
# Update package lists
sudo apt update

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-venv git poppler-utils

# Clone your repository
git clone https://github.com/yourusername/colorstack-ai-resume-review-discord-bot.git
cd colorstack-ai-resume-review-discord-bot

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Create a .env file
cat > .env << EOF
DISCORD_TOKEN=your_discord_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
RESUME_REVIEW_CHANNEL_ID=your_channel_id
EOF
```

### 4. Create a Systemd Service

```bash
# Create a startup script
cat > start-bot.sh << EOF
#!/bin/bash
cd /path/to/colorstack-ai-resume-review-discord-bot
source venv/bin/activate
python main.py
EOF

# Make it executable
chmod +x start-bot.sh

# Create a systemd service file
sudo bash -c 'cat > /etc/systemd/system/resume-bot.service << EOF
[Unit]
Description=ColorStack Resume Review Discord Bot
After=network.target

[Service]
ExecStart=/path/to/colorstack-ai-resume-review-discord-bot/start-bot.sh
WorkingDirectory=/path/to/colorstack-ai-resume-review-discord-bot
StandardOutput=journal
StandardError=journal
Restart=always
User=your_username

[Install]
WantedBy=multi-user.target
EOF'

# Enable and start the service
sudo systemctl enable resume-bot.service
sudo systemctl start resume-bot.service

# Check the status
sudo systemctl status resume-bot.service
```

## Post-Deployment Steps

After deploying the bot, perform these steps to ensure everything is working correctly:

1. **Test the bot commands**:
   - Send `!resumehelp` in a channel where the bot has access
   - If you're an admin, try `!resumestats` to see usage statistics

2. **Test the resume review process**:
   - Upload a PDF resume to your forum channel
   - Verify the bot responds and processes the resume
   - Check that the feedback and rating system work

3. **Monitor analytics**:
   - Check that the `analytics_data.json` file is being created and updated
   - Verify API usage is being tracked correctly

4. **Set up regular backups**:
   - Consider setting up automated backups of the analytics data

## Troubleshooting

If you encounter issues during deployment:

1. **Bot not connecting to Discord**:
   - Verify your Discord token is correct
   - Check that the bot has the necessary intents enabled in the Discord Developer Portal

2. **PDF processing errors**:
   - Ensure Poppler is installed correctly
   - Verify the reference resume is in the correct location

3. **Analytics not working**:
   - Check that the bot has write permissions for the directory
   - Verify the analytics module is being imported correctly

4. **Command errors**:
   - Ensure you're using the correct command names (`!resumehelp` not `!help`)
   - Check that the bot has the necessary permissions in your Discord server

For more detailed troubleshooting, refer to the logs of your deployment platform. 