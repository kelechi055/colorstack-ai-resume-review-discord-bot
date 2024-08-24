import json
import logging
from pydantic import ValidationError
from models import ResumeFeedback
from utils.anthropic_utils import get_chat_completion
from utils.pdf_utils import convert_pdf_to_image

def review_resume(resume: bytes) -> dict:
    system_prompt = """
    You are the best resume reviewer in the world, specifically for resumes aimed at getting a software engineering internship/new grad role.
    Here are your guidelines for a great bullet point:
    - It starts with a strong action verb.
    - It is specific.
    - It talks about achievements.
    - It is concise. No fluff.
    - If possible, it quantifies impact. Don't be as critical about this for projects as you are for work experiences.
    Here are your guidelines for giving feedback:
    - Be kind.
    - Be specific.
    - Be actionable.
    - Ask questions (ie: "how many...", "how much...", "what was the impact...").
    - Don't be overly nit-picky.
    - If the bullet point is NOT a 10/10, then the last sentence of your feedback MUST be an actionable improvement item.
    Here are your guidelines for rewriting bullet points:
    - If the original bullet point is a 10/10, do NOT suggest any rewrites.
    - If the original bullet point is not a 10/10, suggest 1-2 rewrite options.
    - Be 1000% certain that the rewrites address all of your feedback.
    """

    user_prompt = """
    Please review this resume. Only return JSON that respects the following schema:
    experiences: [
        {
            bullets: [
                {
                    content: string,
                    feedback: string,
                    rewrites: [string, string],
                    score: number
                }
            ],
            company: string,
            role: string
        }
    ],
    projects: [
        {
            bullets: [
                {
                    content: string,
                    feedback: string,
                    rewrites: [string, string],
                    score: number
                }
            ],
            title: string
        }
    ]
    """

    image_base64 = convert_pdf_to_image(resume)
    
    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': user_prompt},
                {'type': 'image', 'source': {'data': image_base64, 'media_type': 'image/png', 'type': 'base64'}}
            ]
        }
    ]
    
    try:
        completion = get_chat_completion(max_tokens=8192, messages=messages, system=system_prompt, temperature=0.25)
        result = json.loads(completion)
        logging.info(result['content'][0]['text'])
        resume_feedback = ResumeFeedback(**json.loads(result['content'][0]['text']))
        logging.info("Resume reviewed and feedback generated successfully")
        resume_feedback_model = resume_feedback.dict()
        logging.info(resume_feedback_model)
        return resume_feedback.dict()
    except ValidationError as e:
        logging.error(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error processing resume: {str(e)}")
        raise