import json
import logging
from pydantic import ValidationError
from models import ResumeFeedback
from utils.anthropic_utils import get_chat_completion
from utils.pdf_utils import analyze_font_consistency, check_single_page, convert_pdf_to_image, extract_text_and_formatting

def review_resume(resume: bytes, job_title: str = None, company: str = None, min_qual: str = None, pref_qual: str = None) -> dict:
    job_details = {
        "job_title": "Software Engineer" if job_title is None else job_title,
        "company": "Google" if company is None else company,
        "min_qual": "Education: Currently pursuing a Bachelor's or Master's degree in Computer Science, a related technical field, or equivalent practical experience.\nProgramming Skills: Proficiency in at least one programming language (e.g., Python, Java, C++, Go).\nComputer Science Fundamentals: Solid understanding of data structures, algorithms, and complexity analysis.\nTechnical Experience: Experience with software development, demonstrated through personal projects, coursework, or internships.\nProblem-Solving Ability: Strong analytical and problem-solving skills, with the ability to apply theoretical concepts to practical scenarios.\nCollaboration and Communication: Ability to work effectively in a team environment, with strong written and verbal communication skills." if min_qual is None else min_qual,
        "pref_qual": "Advanced Coursework: Completed coursework or have practical experience in advanced computer science topics such as distributed systems, machine learning, or security.\nTechnical Experience: Internships or co-op experience in a software development role, or significant contributions to open-source projects.\nCoding Competitions: Participation in coding competitions or technical challenges, such as competitive programming or hackathons.\nProject Experience: Demonstrated experience with complex software projects, either through internships, personal projects, or academic coursework.\nSoft Skills: Proven ability to take initiative, manage multiple tasks effectively, and adapt to new challenges in a fast-paced environment.\nLeadership and Impact: Experience in leadership roles, or demonstrated impact through technical or non-technical contributions." if pref_qual is None else pref_qual
    }
        
    system_prompt = f"""
    You are an expert resume reviewer for a {job_details["job_title"]} internship or new grad role at {job_details["company"]}. Your review should be highly detailed and focused on the following aspects:

    Ensure the resume aligns with the job's qualifications. 
    - Minimum Qualifications: {job_details["min_qual"]}
    - Preferred Qualifications: {job_details["pref_qual"]}
    
    Here are your guidelines for a great bullet point:
    - It starts with a strong, relevant action verb that pertains to {job_details["job_title"]} or related technical roles.
    - It is specific, technical, and directly related to {job_details["job_title"]} tasks or achievements.
    - It talks about significant, measurable achievements within a {job_details["job_title"]} context.
    - It is concise and professional. No fluff or irrelevant details.
    - If possible, it quantifies impact, especially in technical or {job_details["job_title"]}-related terms.
    - Two lines or less.
    - Does not have excessive white space.
    - Avoids any mention of irrelevant skills, hobbies, or experiences that do not directly contribute to a {job_details["job_title"]} role.

    Here are your guidelines for giving feedback:
    - Be kind, but firm.
    - Be specific.
    - Be actionable.
    - Ask questions like "how many...", "how much...", "what was the technical impact...", "how did this experience contribute to your {job_details["job_title"]} skills...".
    - Be critical about the relevance of the content to a {job_details["job_title"]} role.
    - If the bullet point is NOT a 10/10, then the last sentence of your feedback MUST be an actionable improvement item focused on how to make the experience or achievement more relevant to software engineering.

    Here are your guidelines for rewriting bullet points:
    - If the original bullet point is a 10/10 and highly relevant to {job_details["job_title"]}, do NOT suggest any rewrites.
    - If the original bullet point is not a 10/10 or not relevant to {job_details["job_title"]}, suggest 1-2 rewrite options that make the content more technical, professional, and directly related to the field.
    - Be 1000% certain that the rewrites address all of your feedback.

    Formatting guidelines:
    - Ensure consistency in font size and type.
    - Align bullet points and headings properly.
    - Check for sufficient spacing between sections.
    - Ensure clear and readable section headings.
    - Highlight important details without overwhelming with too much text.
    - Be particularly critical of resumes that include unprofessional language, irrelevant experiences, or inappropriate formatting.
    """
    # Check if the resume is a single page
    is_single_page = check_single_page(resume)

    # Extract text and formatting information
    extracted_data = extract_text_and_formatting(resume)
    resume_text = extracted_data["text"]
    formatting_info = extracted_data["formatting"]

    # Analyze font consistency
    font_consistency_feedback = analyze_font_consistency(formatting_info)

    # Adjust feedback based on page count
    if not is_single_page:
        logging.warning("The resume is more than one page.")
        additional_feedback = "Note: Your resume exceeds one page. Consider condensing your content to fit on a single page for better readability."
        page_utilization_score = 4  # Example score for multi-page resumes
        is_single_page_feedback = "The resume is not a single page."
    else:
        additional_feedback = "Your resume is appropriately formatted to fit on a single page."
        page_utilization_score = 10  # Example score for single-page resumes
        is_single_page_feedback = "The resume is a single page."

    # Include is_single_page feedback in the formatting section
    formatting_info['is_single_page'] = {
        "issue": not is_single_page,  # Adjust based on your logic
        "feedback": is_single_page_feedback,
        "score": page_utilization_score
    }

    user_prompt = f"""
    Please review this resume for the role of {job_title} at {company}. 
    The job's minimum qualifications are as follows:
    {min_qual}
    The job's preferred qualifications are as follows:
    {pref_qual}
    The resume text is as follows:
    {resume_text}
    Font consistency feedback:
    {font_consistency_feedback['feedback']}
    Additional feedback: {additional_feedback}
    Only return JSON that respects the following schema:
    experiences: [
        {{
            bullets: [
                {{
                    content: string,
                    feedback: string,
                    rewrites: [string, string],
                    score: number
                }}
            ],
            company: string,
            role: string
        }}
    ],
    projects: [
        {{
            bullets: [
                {{
                    content: string,
                    feedback: string,
                    rewrites: [string, string],
                    score: number
                }}
            ],
            title: string
        }}
    ],
    formatting: {{
        font_consistency: {{ issue: boolean, feedback: string, score: number }},
        font_choice: {{ issue: boolean, feedback: string, score: number }},
        font_size: {{ issue: boolean, feedback: string, score: number }},
        alignment: {{ issue: boolean, feedback: string, score: number }},
        margins: {{ issue: boolean, feedback: string, score: number }},
        line_spacing: {{ issue: boolean, feedback: string, score: number }},
        section_spacing: {{ issue: boolean, feedback: string, score: number }},
        headings: {{ issue: boolean, feedback: string, score: number }},
        bullet_points: {{ issue: boolean, feedback: string, score: number }},
        contact_information: {{ issue: boolean, feedback: string, score: number }},
        overall_layout: {{ issue: boolean, feedback: string, score: number }},
        page_utilization: {{ issue: boolean, feedback: string, score: number }},
        is_single_page: {{ issue: boolean, feedback: string, score: number }},
        consistency: {{ issue: boolean, feedback: string, score: number }},
        overall_score: number
    }}
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