import logging
import os
import json
from utils.analytics import analytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_analytics():
    """Test the analytics functionality"""
    logger.info("Testing analytics functionality...")
    
    # Test tracking a resume review
    analytics.track_resume_review(
        user_id="123456789",
        server_id="987654321",
        scores={
            "overall": 7.5,
            "experiences": 8.0,
            "projects": 7.0,
            "formatting": 7.5
        }
    )
    logger.info("Tracked a test resume review")
    
    # Test tracking API usage
    analytics.track_api_usage(
        tokens_used=1000,
        estimated_cost=0.009
    )
    logger.info("Tracked test API usage")
    
    # Test tracking feedback rating
    analytics.track_feedback_rating(4)
    logger.info("Tracked test feedback rating")
    
    # Get and display the usage report
    report = analytics.get_usage_report()
    logger.info(f"Usage report: {json.dumps(report, indent=2)}")
    
    # Check if the analytics file was created
    if os.path.exists(analytics.storage_file):
        logger.info(f"Analytics file created at {analytics.storage_file}")
    else:
        logger.error(f"Analytics file not created at {analytics.storage_file}")
    
    logger.info("Analytics test completed")

if __name__ == "__main__":
    test_analytics() 