import json
import os
import logging
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class Analytics:
    def __init__(self, storage_file="analytics_data.json"):
        self.storage_file = storage_file
        self.data = self._load_data()
        
    def _load_data(self):
        """Load analytics data from file or create default structure if file doesn't exist"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error decoding analytics file {self.storage_file}. Creating new data structure.")
                return self._create_default_data()
        else:
            return self._create_default_data()
    
    def _create_default_data(self):
        """Create default data structure for analytics"""
        return {
            "resume_reviews": {
                "total": 0,
                "by_server": {},
                "by_user": {},
                "by_date": {},
                "average_scores": {
                    "overall": 0,
                    "experiences": 0,
                    "projects": 0,
                    "formatting": 0
                }
            },
            "api_usage": {
                "total_tokens": 0,
                "total_requests": 0,
                "estimated_cost": 0
            },
            "feedback_ratings": {
                "total": 0,
                "average": 0,
                "ratings": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0
                }
            }
        }
    
    def _save_data(self):
        """Save analytics data to file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics data: {e}")
    
    def track_resume_review(self, user_id, server_id, scores):
        """Track a resume review"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Update total count
        self.data["resume_reviews"]["total"] += 1
        
        # Update by server
        server_id_str = str(server_id)
        if server_id_str not in self.data["resume_reviews"]["by_server"]:
            self.data["resume_reviews"]["by_server"][server_id_str] = 0
        self.data["resume_reviews"]["by_server"][server_id_str] += 1
        
        # Update by user
        user_id_str = str(user_id)
        if user_id_str not in self.data["resume_reviews"]["by_user"]:
            self.data["resume_reviews"]["by_user"][user_id_str] = 0
        self.data["resume_reviews"]["by_user"][user_id_str] += 1
        
        # Update by date
        if today not in self.data["resume_reviews"]["by_date"]:
            self.data["resume_reviews"]["by_date"][today] = 0
        self.data["resume_reviews"]["by_date"][today] += 1
        
        # Update average scores
        total = self.data["resume_reviews"]["total"]
        prev_total = total - 1
        
        # Calculate new averages using weighted average formula
        for score_type, score in scores.items():
            if score_type in self.data["resume_reviews"]["average_scores"]:
                prev_avg = self.data["resume_reviews"]["average_scores"][score_type]
                new_avg = (prev_avg * prev_total + score) / total if total > 0 else score
                self.data["resume_reviews"]["average_scores"][score_type] = round(new_avg, 2)
        
        self._save_data()
        logger.info(f"Tracked resume review for user {user_id} on server {server_id}")
    
    def track_api_usage(self, tokens_used, estimated_cost=None):
        """Track API usage"""
        if estimated_cost is None:
            # Estimate cost based on Claude 3.5 Sonnet pricing ($3 per 1M input tokens, $15 per 1M output tokens)
            # Assuming a 50/50 split between input and output tokens for simplicity
            estimated_cost = (tokens_used / 2 * 3 / 1000000) + (tokens_used / 2 * 15 / 1000000)
        
        self.data["api_usage"]["total_tokens"] += tokens_used
        self.data["api_usage"]["total_requests"] += 1
        self.data["api_usage"]["estimated_cost"] += estimated_cost
        
        self._save_data()
        logger.info(f"Tracked API usage: {tokens_used} tokens, ${estimated_cost:.6f} estimated cost")
    
    def track_feedback_rating(self, rating):
        """Track user feedback rating (1-5)"""
        if rating < 1 or rating > 5:
            logger.warning(f"Invalid feedback rating: {rating}. Must be between 1-5.")
            return
        
        # Update total and specific rating count
        self.data["feedback_ratings"]["total"] += 1
        self.data["feedback_ratings"]["ratings"][str(rating)] += 1
        
        # Update average rating
        total_ratings = self.data["feedback_ratings"]["total"]
        rating_sum = sum(int(r) * count for r, count in self.data["feedback_ratings"]["ratings"].items())
        self.data["feedback_ratings"]["average"] = round(rating_sum / total_ratings, 2) if total_ratings > 0 else 0
        
        self._save_data()
        logger.info(f"Tracked feedback rating: {rating}/5")
    
    def get_usage_report(self):
        """Generate a usage report"""
        return {
            "total_reviews": self.data["resume_reviews"]["total"],
            "average_scores": self.data["resume_reviews"]["average_scores"],
            "api_usage": {
                "total_tokens": self.data["api_usage"]["total_tokens"],
                "total_requests": self.data["api_usage"]["total_requests"],
                "estimated_cost": round(self.data["api_usage"]["estimated_cost"], 2)
            },
            "feedback": {
                "total_ratings": self.data["feedback_ratings"]["total"],
                "average_rating": self.data["feedback_ratings"]["average"]
            }
        }

# Create a singleton instance
analytics = Analytics() 