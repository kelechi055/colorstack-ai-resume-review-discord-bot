# ColorStack AI Resume Review Discord Bot

A Discord bot that provides automated AI-powered resume reviews for ColorStack members. The bot analyzes resumes posted in a designated Discord channel, providing detailed feedback on formatting, bullet points, and overall resume quality.

![ColorStack Logo](https://colorstack.org/wp-content/uploads/2023/01/ColorStack-Logo-Horizontal-1.png)

## 🌟 Features

- **AI-Powered Resume Analysis**: Uses Claude AI to analyze resumes and provide detailed feedback
- **Formatting Feedback**: Compares user resumes to a reference resume template for formatting suggestions
- **Bullet Point Analysis**: Evaluates each bullet point in experience and project sections
- **Job-Specific Feedback**: Tailors feedback based on specific job postings (optional)
- **Scoring System**: Provides numerical scores for each section and an overall resume score
- **Visual Feedback**: Uses embeds and GIFs to present feedback in an engaging way

## 📋 Requirements

- Python 3.7+
- Discord Bot Token
- Anthropic API Key (for Claude AI)
- PDF processing capabilities

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/colorstack-ai-resume-review-discord-bot.git
   cd colorstack-ai-resume-review-discord-bot
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file with your credentials**
   ```
   DISCORD_TOKEN=your_discord_bot_token
   ANTHROPIC_API_KEY=your_anthropic_api_key
   RESUME_REVIEW_CHANNEL_ID=your_channel_id
   ```

5. **Add a reference resume**
   - Place a reference resume PDF in the `resumes/` directory named `jakes-resume.pdf`

## 💻 Usage

1. **Start the bot**
   ```bash
   python main.py
   ```

2. **Using the bot in Discord**
   - Upload a PDF resume to the designated resume review channel
   - The bot will ask if you want to provide job details
   - Receive detailed feedback on your resume

## 🌐 Deployment Options

### Heroku Deployment

1. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set DISCORD_TOKEN=your_discord_bot_token
   heroku config:set ANTHROPIC_API_KEY=your_anthropic_api_key
   heroku config:set RESUME_REVIEW_CHANNEL_ID=your_channel_id
   ```

3. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

4. **Scale the worker dyno**
   ```bash
   heroku ps:scale worker=1
   ```

### Raspberry Pi Deployment

1. **Clone the repository on your Raspberry Pi**
   ```bash
   git clone https://github.com/yourusername/colorstack-ai-resume-review-discord-bot.git
   ```

2. **Create a startup script**
   ```bash
   #!/bin/bash
   cd /path/to/colorstack-ai-resume-review-discord-bot
   source venv/bin/activate
   python main.py
   ```

3. **Set up as a systemd service**
   Create a file at `/etc/systemd/system/resume-bot.service`:
   ```
   [Unit]
   Description=ColorStack Resume Review Discord Bot
   After=network.target

   [Service]
   ExecStart=/path/to/startup-script.sh
   WorkingDirectory=/path/to/colorstack-ai-resume-review-discord-bot
   StandardOutput=inherit
   StandardError=inherit
   Restart=always
   User=pi

   [Install]
   WantedBy=multi-user.target
   ```

4. **Enable and start the service**
   ```bash
   sudo systemctl enable resume-bot.service
   sudo systemctl start resume-bot.service
   ```

## 🔍 Logging

The bot uses Python's logging module to record information about its operation:

- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Format**: Timestamp, log level, and message
- **Log Location**: 
  - When running locally: Console output and `logs/resume_review.log`
  - When running on Heroku: Heroku logs (view with `heroku logs --tail`)

## 🛠️ Troubleshooting

### Common Issues

1. **Bot not responding to resume uploads**
   - Verify the bot is running (`heroku logs --tail` or check systemd status)
   - Ensure the correct channel ID is set in the environment variables
   - Check that the bot has proper permissions in the Discord server

2. **Error processing resumes**
   - Ensure the PDF is properly formatted and not password-protected
   - Check that the reference resume exists in the correct location
   - Verify the Anthropic API key is valid and has sufficient credits

3. **Deployment issues on Heroku**
   - Check for build errors in the Heroku logs
   - Ensure all environment variables are properly set
   - Verify the Procfile is correctly configured with `worker: python main.py`

## 📊 Architecture

The bot consists of several key components:

- **Discord Bot**: Handles Discord interactions and commands
- **Resume Processor**: Extracts text and formatting from PDFs
- **AI Integration**: Communicates with Claude AI for analysis
- **Feedback Formatter**: Formats AI feedback into Discord embeds

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by [Oyster](https://github.com/colorstackorg/oyster) 🦪
- Powered by ColorStack UF ResumeAI
- Uses [Jake's Resume](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs) as a reference template
