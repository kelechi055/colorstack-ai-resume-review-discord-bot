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
- **Analytics & Monitoring**: Tracks usage statistics, API consumption, and user feedback
- **User Feedback System**: Collects user ratings to improve the service
- **Help Command**: Provides guidance on how to use the bot

## 📋 Requirements

- Python 3.7+
- Discord Bot Token
- Anthropic API Key (for Claude AI)
- PDF processing capabilities
- Poppler (required for PDF processing):
  - **Ubuntu/Debian/Raspberry Pi**: `sudo apt-get install poppler-utils`
  - **macOS**: `brew install poppler`
  - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/)
  - **Heroku**: Automatically installed via the included Aptfile

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
   - Rate your experience with the feedback (1-5 stars)

3. **Bot Commands**
   - `!resumehelp` - Shows information about how to use the bot and available features
   - `!stats` - Shows usage statistics (admin only)

## 🤖 Adding the Bot to Your Discord Server

To add this bot to your own Discord server, you'll need to create a Discord application, set up a bot user, and invite it to your server.

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "Resume Review Bot")
3. Navigate to the "Bot" tab and click "Add Bot"
4. Under the bot settings:
   - Enable "Message Content Intent" under Privileged Gateway Intents
   - Enable "Server Members Intent" under Privileged Gateway Intents

### 2. Get Your Bot Token

1. In the Bot tab, click "Reset Token" and copy your bot token
2. Keep this token secure and never share it publicly

### 3. Invite the Bot to Your Server

1. Go to the "OAuth2" tab, then "URL Generator"
2. Select the following scopes:
   - `bot`
   - `applications.commands`
3. Select the following bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use External Emojis
   - Add Reactions
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 4. Set Up Your Environment

1. Follow the installation steps in this README
2. Create a `.env` file with your bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   RESUME_REVIEW_CHANNEL_ID=your_channel_id_here
   ```
3. To get your channel ID:
   - Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
   - Right-click on your resume review channel and select "Copy ID"

### 5. Deploy the Bot

Choose one of the deployment options described in this README and start the bot.

### 6. Set Up a Resume Review Forum Channel

This bot is designed to work with Discord forum channels for organizing resume reviews:

1. **Create a Forum Channel**:
   - Go to your Discord server
   - Click the "+" icon next to "TEXT CHANNELS"
   - Select "Create Forum"
   - Name it (e.g., "Resume Reviews")

2. **Configure Forum Settings**:
   - Set appropriate permissions (consider making it private to specific roles)
   - Enable "Require topic tags" and create tags like "Software Engineering", "Data Science", etc.
   - Set guidelines explaining how to use the resume review service

3. **Update Your Environment Variables**:
   - Copy the forum channel ID as described above
   - Update your `RESUME_REVIEW_CHANNEL_ID` environment variable with this ID

4. **Using the Forum**:
   - Users should create a new post in the forum
   - They should upload their resume as a PDF in the first message
   - The bot will automatically respond with review options and feedback

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

### Free Deployment Alternatives

#### Replit (Free)

1. **Create a Replit account** at [replit.com](https://replit.com)
2. **Create a new Python repl**
3. **Upload your code** or connect your GitHub repository
4. **Add a `.replit` file** with:
   ```
   run = "python main.py"
   ```
5. **Set up environment variables** in the Secrets tab
6. **Enable the "Always On" feature** (free for students with the Hacker plan)

#### Railway (Free Tier)

1. **Create a Railway account** at [railway.app](https://railway.app)
2. **Create a new project** and connect your GitHub repository
3. **Set up environment variables** in the Variables tab
4. **Deploy your application**
5. **Note**: Free tier includes $5 of free credits per month

#### Oracle Cloud Free Tier (Always Free)

1. **Create an Oracle Cloud account** at [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
2. **Set up a VM instance** using the Always Free resources
3. **Clone your repository** and set up the bot as you would on a local machine
4. **Create a systemd service** to keep the bot running
5. **Note**: Includes 2 AMD-based Compute VMs with 1 GB RAM each that never expire

#### Google Cloud Free Tier (Always Free)

1. **Create a Google Cloud account** at [cloud.google.com](https://cloud.google.com/)
2. **Set up a VM instance** using the e2-micro instance type (always free)
3. **Clone your repository** and set up the bot as you would on a local machine
4. **Create a systemd service** to keep the bot running
5. **Note**: Includes 1 e2-micro VM instance in US regions that never expires

### Deployment Options Comparison

| Platform | Cost | Pros | Cons | Best For |
|----------|------|------|------|----------|
| **Heroku** | $7/month (Basic)<br>$5/month (Eco) | Easy deployment<br>Managed platform<br>Good logging | Sleep restrictions on Eco<br>Limited resources | Quick setup, testing |
| **Replit** | Free (with limitations) | Zero setup<br>Web-based IDE<br>Always On option | Limited resources<br>Occasional restarts | Students, beginners |
| **Railway** | Free tier ($5 credit/month) | Simple deployment<br>GitHub integration | Credit expires monthly<br>Requires card for verification | Small projects, testing |
| **Oracle Cloud** | Free forever | 2 VMs always free<br>Never expires<br>Full control | Complex setup<br>Requires sysadmin knowledge | Long-term production |
| **Google Cloud** | Free forever | VM always free<br>Never expires<br>Full control | Complex setup<br>Requires sysadmin knowledge | Long-term production |
| **Raspberry Pi** | One-time hardware cost | Complete control<br>No ongoing costs<br>No sleep restrictions | Hardware maintenance<br>Power/internet dependency | Self-hosting enthusiasts |

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

4. **Analytics not working**
   - Check that the `analytics_data.json` file is writable by the application
   - Verify that the analytics module is properly imported
   - Check logs for any errors related to analytics tracking
   - Ensure the bot has permission to write files in the deployment environment

5. **Feedback mechanism not working**
   - Verify that the Discord bot has the necessary permissions to create buttons
   - Check that the bot has the "Use External Emojis" permission
   - Ensure the bot has the "Message Content Intent" enabled in the Discord Developer Portal

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

## 🚀 Future Enhancements

Here are some potential future enhancements for the bot:

### Analytics Improvements
- **Visualization Dashboard**: Create a web dashboard for analytics visualization
- **Export Functionality**: Allow exporting analytics data to CSV/Excel
- **User-Specific Tracking**: Enable users to track their resume improvement over time
- **Trend Analysis**: Implement trend analysis to identify patterns in resume quality

### User Experience Enhancements
- **Resume Templates**: Provide example templates for different industries
- **Scheduled Reviews**: Allow users to schedule follow-up reviews
- **Comparative Analysis**: Compare resume scores against industry averages
- **Personalized Tips**: Provide personalized improvement tips based on user history

### Technical Improvements
- **Database Integration**: Move from file-based to database storage for analytics
- **API Rate Limiting**: Implement more sophisticated API usage controls
- **Caching**: Add caching for common operations to improve performance
- **Automated Testing**: Expand test coverage for all components

If you're interested in contributing to any of these enhancements, please check the Issues tab for current development priorities or open a new issue to discuss your ideas.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by [Oyster](https://github.com/colorstackorg/oyster) 🦪
- Powered by ColorStack UF ResumeAI
- Uses [Jake's Resume](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs) as a reference template

## 📊 Analytics & Monitoring

The bot includes a comprehensive analytics system that tracks:

- **Resume Reviews**: Total number of reviews, breakdown by server and user
- **Scores**: Average scores for experiences, projects, formatting, and overall
- **API Usage**: Token consumption and estimated costs
- **User Feedback**: Ratings provided by users after receiving resume feedback

### Usage Statistics Command

Administrators can view these statistics using the `!stats` command in Discord, which displays:

- Total number of resume reviews processed
- Average scores across all resume sections
- API usage metrics and estimated costs
- User feedback ratings and satisfaction metrics

### Analytics Data Storage

Analytics data is stored in a JSON file (`analytics_data.json`) and includes:

- Daily usage metrics for tracking trends over time
- Server-specific statistics to understand usage across different communities
- User engagement metrics to identify power users
- API consumption tracking to monitor costs
- Feedback ratings to measure user satisfaction

This data helps administrators understand usage patterns and make informed decisions about bot improvements.

### Implementation Details

The analytics system is implemented in the `utils/analytics.py` file and provides:

- Persistent storage with error handling
- Atomic updates to prevent data corruption
- Weighted average calculations for accurate scoring metrics
- Cost estimation based on Claude API pricing

### Testing Analytics

The repository includes a test script (`test_analytics.py`) to verify the analytics functionality:

```bash
python test_analytics.py
```

This script:
- Creates test resume review entries
- Simulates API usage tracking
- Records sample feedback ratings
- Generates a usage report
- Verifies that the analytics file is created correctly

Running this test is recommended after deployment to ensure the analytics system is functioning properly in your environment.

## 🤖 User Experience Features

### Help Command

The bot provides a helpful `!resumehelp` command that explains:

- How to get a resume review
- What's included in the review
- Available commands and their usage

### Feedback Collection

After each resume review, the bot asks users to rate their experience:

- Simple 1-5 star rating system
- Feedback is stored in the analytics system
- Helps identify areas for improvement

### Error Handling

The bot includes robust error handling to ensure a smooth user experience:

- Graceful handling of malformed PDFs
- Clear error messages for users
- Detailed logging for administrators
