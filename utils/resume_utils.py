import json
import logging
from pydantic import ValidationError
from models import ResumeFeedback
from utils.anthropic_utils import get_chat_completion
from utils.pdf_utils import convert_pdf_to_image

def review_resume(resume: bytes, job_title: str, company: str, min_qual: str, pref_qual: str) -> dict:
    system_prompt = """
    You are the best resume reviewer in the world, specifically for resumes aimed at getting a software engineering internship or new grad role.
    Here are your guidelines for a great bullet point:
    - It starts with a strong, relevant action verb that pertains to software engineering or related technical roles.
    - It is specific, technical, and directly related to software engineering tasks or achievements.
    - It talks about significant, measurable achievements within a software engineering context.
    - It is concise and professional. No fluff or irrelevant details.
    - If possible, it quantifies impact, especially in technical or software-related terms.
    - Two lines or less.
    - Does not have excessive white space.
    - Avoids any mention of irrelevant skills, hobbies, or experiences that do not directly contribute to a software engineering role.

    Here are your guidelines for giving feedback:
    - Be kind, but firm.
    - Be specific.
    - Be actionable.
    - Ask questions like "how many...", "how much...", "what was the technical impact...", "how did this experience contribute to your software engineering skills...".
    - Be critical about the relevance of the content to a software engineering role.
    - If the bullet point is NOT a 10/10, then the last sentence of your feedback MUST be an actionable improvement item focused on how to make the experience or achievement more relevant to software engineering.

    Here are your guidelines for rewriting bullet points:
    - If the original bullet point is a 10/10 and highly relevant to software engineering, do NOT suggest any rewrites.
    - If the original bullet point is not a 10/10 or not relevant to software engineering, suggest 1-2 rewrite options that make the content more technical, professional, and directly related to the field.
    - Be 1000% certain that the rewrites address all of your feedback.

    Formatting guidelines:
    - Ensure consistency in font size and type.
    - Align bullet points and headings properly.
    - Check for sufficient spacing between sections.
    - Ensure clear and readable section headings.
    - Highlight important details without overwhelming with too much text.
    - Be particularly critical of resumes that include unprofessional language, irrelevant experiences, or inappropriate formatting.
    """
    
    job_details = "Please review this resume."
    
    if job_title and company and min_qual and pref_qual:
        job_details = f"""
        Please review this resume for the role of {job_title} at {company}. 
        The job's minimum qualifications are as follows:
        {min_qual}
        The job's preferred qualifications are as follows:
        {pref_qual}
        """

    user_prompt = f"""
    {job_details}
    Only return JSON that respects the following schema:
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
    ],
    formatting: {
        font_consistency: { issue: boolean, feedback: string, score: number },
        font_choice: { issue: boolean, feedback: string, score: number },
        font_size: { issue: boolean, feedback: string, score: number },
        alignment: { issue: boolean, feedback: string, score: number },
        margins: { issue: boolean, feedback: string, score: number },
        line_spacing: { issue: boolean, feedback: string, score: number },
        section_spacing: { issue: boolean, feedback: string, score: number },
        headings: { issue: boolean, feedback: string, score: number },
        bullet_points: { issue: boolean, feedback: string, score: number },
        contact_information: { issue: boolean, feedback: string, score: number },
        overall_layout: { issue: boolean, feedback: string, score: number },
        page_utilization: { issue: boolean, feedback: string, score: number },
        consistency: { issue: boolean, feedback: string, score: number },
        overall_score: number
    }
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