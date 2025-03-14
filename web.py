import os
import logging
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    """Home endpoint that confirms the app is running."""
    logger.info("Home endpoint accessed")
    return "Resume Review Discord Bot is running!"

@app.route('/health')
def health():
    """Health check endpoint for monitoring services."""
    logger.info("Health check endpoint accessed")
    return jsonify({"status": "ok", "service": "resume-review-bot"})

@app.route('/ping')
def ping():
    """Simple ping endpoint for uptime monitoring services."""
    return "pong"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port) 