import json
import logging
import tiktoken
from pydantic import ValidationError
from models import ResumeFeedback
from utils.anthropic_utils import get_chat_completion
from utils.pdf_utils import analyze_font_consistency, check_single_page, convert_pdf_to_image, extract_text_and_formatting

def review_resume(resume_user: bytes, resume_jake: bytes, job_title: str = None, company: str = None, min_qual: str = None, pref_qual: str = None) -> dict:
    job_details = {
        "job_title": "Software Engineer" if job_title is None else job_title,
        "company": "Google" if company is None else company,
        "min_qual": "Education: Currently pursuing a Bachelor's or Master's degree in Computer Science, a related technical field, or equivalent practical experience.\nProgramming Skills: Proficiency in at least one programming language (e.g., Python, Java, C++, Go).\nComputer Science Fundamentals: Solid understanding of data structures, algorithms, and complexity analysis.\nTechnical Experience: Experience with software development, demonstrated through personal projects, coursework, or internships.\nProblem-Solving Ability: Strong analytical and problem-solving skills, with the ability to apply theoretical concepts to practical scenarios.\nCollaboration and Communication: Ability to work effectively in a team environment, with strong written and verbal communication skills." if min_qual is None else min_qual,
        "pref_qual": "Advanced Coursework: Completed coursework or have practical experience in advanced computer science topics such as distributed systems, machine learning, or security.\nTechnical Experience: Internships or co-op experience in a software development role, or significant contributions to open-source projects.\nCoding Competitions: Participation in coding competitions or technical challenges, such as competitive programming or hackathons.\nProject Experience: Demonstrated experience with complex software projects, either through internships, personal projects, or academic coursework.\nSoft Skills: Proven ability to take initiative, manage multiple tasks effectively, and adapt to new challenges in a fast-paced environment.\nLeadership and Impact: Experience in leadership roles, or demonstrated impact through technical or non-technical contributions." if pref_qual is None else pref_qual
    }

    extracted_data_jake_resume = extract_text_and_formatting(resume_jake)

    logging.debug(f"Extracted data: {extracted_data_jake_resume}")

    if not isinstance(extracted_data_jake_resume, dict):
        logging.error("Extracted Jake resume data is not a dictionary.")
        raise ValueError("Extracted Jake resume data must be a dictionary.")

    formatting_info_jake_resume = extracted_data_jake_resume["formatting"]

    # Example of processing formatting_info
    for index, item in enumerate(formatting_info_jake_resume):
        # Ensure item is a dictionary
        if isinstance(item, dict):
            text = item.get("text")
            font = item.get("font")
            size = item.get("size")
            bbox = item.get("bbox")
            
            # Log the extracted formatting information
            logging.info(f"Formatting info [{index}]: text='{text}', font='{font}', size={size}, bbox={bbox}")
        else:
            logging.error(f"Formatting info item at index {index} is not a dictionary: {item}")

    system_prompt = f"""
    You are an expert resume reviewer for a {job_details["job_title"]} internship or new grad role at {job_details["company"]}. Your review should be highly detailed and focused on the following aspects:

    Ensure the resume aligns with the job's qualifications. 
    - Minimum Qualifications: {job_details["min_qual"]}
    - Preferred Qualifications: {job_details["pref_qual"]}

    Here are the extracted text elements of the default resume for comparison:
    {json.dumps(extracted_data_jake_resume, indent=2)}
    
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

    Here are your guidelines for great formatting:
    - Ensure consistency in font size and type.
    - Align bullet points and headings properly.
    - Check for sufficient spacing between sections.
    - Ensure clear and readable section headings.
    - Highlight important details without overwhelming with too much text.
    - Be particularly critical of resumes that include unprofessional language, irrelevant experiences, or inappropriate formatting.

    Here are your guidelines for giving formatting feedback:
    - Compare the user's resume formatting to the default resume.
    - Identify specific formatting issues in the user's resume.
    - Explain why each identified issue is problematic for a {job_details["job_title"]} resume.
    - Be precise in describing the location and nature of formatting problems.
    - Acknowledge any formatting aspects that are well-executed.


    Here are your guidelines for suggesting formatting improvements:
    - If the formatting is a 10/10, do not suggest any improvements.
    - If the formatting is not a 10/10, provide 1-2 suggestions that are clear, specific, and actionable to address each formatting issue.
    - Explain how each improvement will enhance the resume's readability and professionalism.
    - Prioritize formatting changes that will have the most impact for a {job_details["job_title"]} position.
    - If applicable, reference the default resume as an example of good formatting.
    - Suggest tools or techniques (e.g., specific word processor features) that can help implement the improvements.
    - Emphasize the importance of consistency throughout the resume.
    """
    # Check if the resume is a single page
    is_single_page_user_resume = check_single_page(resume_user )

    # Extract text and formatting information
    extracted_data_user_resume = extract_text_and_formatting(resume_user)

    logging.debug(f"Extracted data: {extracted_data_user_resume}")

    # Ensure extracted_data is a dictionary
    if not isinstance(extracted_data_user_resume, dict):
        logging.error("Extracted user resume data is not a dictionary.")
        raise ValueError("Extracted user resume data must be a dictionary.")

    formatting_info_user_resume = extracted_data_user_resume["formatting"]

    # Example of processing formatting_info
    for index, item in enumerate(formatting_info_user_resume):
        # Ensure item is a dictionary
        if isinstance(item, dict):
            text = item.get("text")
            font = item.get("font")
            size = item.get("size")
            bbox = item.get("bbox")
            
            # Log the extracted formatting information
            logging.info(f"Formatting info [{index}]: text='{text}', font='{font}', size={size}, bbox={bbox}")
        else:
            logging.error(f"Formatting info item at index {index} is not a dictionary: {item}")

    # Analyze font consistency
    font_consistency_feedback = analyze_font_consistency(formatting_info_user_resume)

    # Adjust feedback based on page count
    if not is_single_page_user_resume:
        logging.warning("The resume is more than one page.")
        additional_feedback = "Your resume exceeds one page. Consider condensing your content to fit on a single page for better readability."
    else:
        additional_feedback = "Your resume is appropriately formatted to fit on a single page."


    logging.info("FONT CONSISTENCY: ", font_consistency_feedback['feedback'])

    user_prompt = f"""
    Please review this resume for the role of {job_title} at {company}. 
    The first image is the user's resume, and the second image is the default resume for comparison.
    The job's minimum qualifications are as follows:
    {min_qual}
    The job's preferred qualifications are as follows:
    {pref_qual}
    Here are the extracted text elements with their bounding box information:
    {json.dumps(extracted_data_user_resume, indent=2)}
    Additional feedback: {additional_feedback}
    Now, compare the formatting of this resume with the default resume data provided in the system prompt.
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
        font_consistency: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        font_choice: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        font_size: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        alignment: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        margins: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        line_spacing: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        section_spacing: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        headings: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        bullet_points: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        contact_information: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        overall_layout: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        page_utilization: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        is_single_page: {{ issue: {not is_single_page_user_resume}, feedback: {additional_feedback}, suggestions: [string, string], score: {10 if is_single_page_user_resume else 0} }},
        consistency: {{ issue: boolean, feedback: string, suggestions: [string, string], score: number }},
        overall_score: number
    }}
    """

    image_base64_user_resume = convert_pdf_to_image(resume_user)
    image_base64_jake_resume = convert_pdf_to_image(resume_jake)
    
    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': f"Here is the user's resume: "},
                {'type': 'image', 'source': {'data': image_base64_user_resume, 'media_type': 'image/png', 'type': 'base64'}},
                {'type': 'text', 'text': f"Here is the default resume: "},
                {'type': 'image', 'source': {'data': image_base64_jake_resume, 'media_type': 'image/png', 'type': 'base64'}},  
                {'type': 'text', 'text': user_prompt}       
            ]
        }
    ]

    encoding = tiktoken.encoding_for_model("gpt-4o")
    num_tokens = len(encoding.encode(user_prompt)) + len(encoding.encode(system_prompt))
    logging.info(f"Number of tokens in user and system prompt: {num_tokens}")
    
    try:
        completion = get_chat_completion(max_tokens=8192, messages=messages, system=system_prompt, temperature=0.25)
        result = json.loads(completion)
        logging.info(f"Result structure: {result}")
        logging.info(result['content'][0])
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