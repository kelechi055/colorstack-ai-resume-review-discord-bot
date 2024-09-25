from pydantic import BaseModel, Field

# Pydantic Models for Validation
class ResumeBullet(BaseModel):
    content: str = Field(..., description="Content of the resume bullet")
    feedback: str = Field(..., description="Feedback on the resume bullet")
    rewrites: list[str] = Field(default=[], max_items=2, description="Possible rewrites for the resume bullet")
    score: int = Field(..., ge=0, le=10, description="Score for the resume bullet")

class ResumeExperience(BaseModel):
    bullets: list[ResumeBullet] = Field(..., description="List of resume bullets for the experience")
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Role at the company")

class ResumeProject(BaseModel):
    bullets: list[ResumeBullet] = Field(..., description="List of resume bullets for the project")
    title: str = Field(..., description="Title of the project")
    
class FormattingAspect(BaseModel):
    issue: bool = Field(..., description="Whether there is an issue with this aspect")
    feedback: str = Field(..., description="Feedback on this aspect")
    score: int = Field(..., ge=0, le=10, description="Score for this aspect")

class FormattingFeedback(BaseModel):
    font_consistency: FormattingAspect = Field(..., description="Assessment of font consistency")
    font_choice: FormattingAspect = Field(..., description="Assessment of font choice")
    font_size: FormattingAspect = Field(..., description="Assessment of font size")
    alignment: FormattingAspect = Field(..., description="Assessment of text alignment")
    margins: FormattingAspect = Field(..., description="Assessment of margin settings")
    line_spacing: FormattingAspect = Field(..., description="Assessment of line spacing")
    section_spacing: FormattingAspect = Field(..., description="Assessment of spacing between sections")
    headings: FormattingAspect = Field(..., description="Assessment of heading styles")
    bullet_points: FormattingAspect = Field(..., description="Assessment of bullet point formatting")
    contact_information: FormattingAspect = Field(..., description="Assessment of contact information formatting")
    overall_layout: FormattingAspect = Field(..., description="Assessment of overall layout and visual appeal")
    page_utilization: FormattingAspect = Field(..., description="Assessment of efficient use of page space")
    is_single_page: FormattingAspect = Field(..., description="Assessment of whether the resume is single-page")
    consistency: FormattingAspect = Field(..., description="Assessment of consistency across all sections")
    overall_score: int = Field(..., ge=0, le=10, description="Overall formatting score")

class ResumeFeedback(BaseModel):
    experiences: list[ResumeExperience] = Field(..., description="List of experiences in the resume")
    projects: list[ResumeProject] = Field(..., description="List of projects in the resume")
    formatting: FormattingFeedback = Field(..., description="Feedback on the resume's formatting")