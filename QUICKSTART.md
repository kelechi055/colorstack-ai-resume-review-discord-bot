# Quick Start Guide for ColorStack AI Resume Review Bot

This guide will help you get the Resume Review Bot up and running quickly.

## Prerequisites

- Python 3.7+
- Discord Bot Token
- Anthropic API Key
- PDF processing capabilities (Poppler)

## 5-Minute Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/colorstack-ai-resume-review-discord-bot.git
cd colorstack-ai-resume-review-discord-bot
```

### 2. Set Up Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```
DISCORD_TOKEN=your_discord_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
RESUME_REVIEW_CHANNEL_ID=your_forum_channel_id
```

### 4. Add Reference Resume

Place a reference resume PDF in the `resumes/` directory:

```bash
# Create the directory if it doesn't exist
mkdir -p resumes

# Copy your reference resume (must be named jakes-resume.pdf)
cp /path/to/your/reference/resume.pdf resumes/jakes-resume.pdf
```

### 5. Run the Bot

```bash
python main.py
```

## Testing the Bot

1. Send `!resumehelp` in a Discord channel where the bot has access
2. Upload a PDF resume to your designated forum channel
3. Follow the prompts to provide job details (optional)
4. Review the feedback and rate your experience

## Common Issues

- **Import Error**: Make sure all dependencies are installed
- **PDF Processing Error**: Ensure Poppler is installed correctly
- **Bot Not Responding**: Verify your Discord token and channel ID
- **Analytics Error**: Check file permissions for analytics_data.json

## Next Steps

For more detailed information, check:
- `README.md` for full documentation
- `DEPLOYMENT.md` for deployment options
- Run `python test_analytics.py` to test the analytics system

## Getting Help

If you encounter issues, check the troubleshooting section in the README or open an issue on GitHub. 