from pydantic import BaseModel, Field

# Pydantic Models for Validation
class ResumeBullet(BaseModel):
    content: str = Field(..., description="Content of the resume bullet")
    feedback: str = Field(..., description="Feedback on the resume bullet")
    rewrites: list[str] = Field(default=[], max_items=2, description="Possible rewrites for the resume bullet")
    score: int = Field(..., ge=1, le=10, description="Score for the resume bullet")

class ResumeExperience(BaseModel):
    bullets: list[ResumeBullet] = Field(..., description="List of resume bullets for the experience")
    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Role at the company")

class ResumeProject(BaseModel):
    bullets: list[ResumeBullet] = Field(..., description="List of resume bullets for the project")
    title: str = Field(..., description="Title of the project")
    
class FormattingFeedback(BaseModel):
    font_consistency: bool = Field(..., description="Whether there is an issue with font consistency")
    font_feedback: str = Field(..., description="Feedback on font consistency")
    alignment: bool = Field(..., description="Whether there is an issue with alignment")
    alignment_feedback: str = Field(..., description="Feedback on alignment")
    spacing: bool = Field(..., description="Whether there is an issue with spacing")
    spacing_feedback: str = Field(..., description="Feedback on spacing")
    headings: bool = Field(..., description="Whether there is an issue with headings")
    headings_feedback: str = Field(..., description="Feedback on headings")
    overall_score: int = Field(..., ge=1, le=10, description="Overall formatting score")
    
class FormattingFeedback(BaseModel):
    font_consistency: bool
    font_feedback: str = Field(..., description="Feedback on font consistency")
    alignment: bool
    alignment_feedback: str = Field(..., description="Feedback on text alignment")
    spacing: bool
    spacing_feedback: str = Field(..., description="Feedback on spacing")
    headings: bool
    headings_feedback: str = Field(..., description="Feedback on heading styles")
    is_one_page: bool
    bullets_two_lines_or_less: bool
    excessive_white_space: bool

class ResumeFeedback(BaseModel):
    experiences: list[ResumeExperience] = Field(..., description="List of experiences in the resume")
    projects: list[ResumeProject] = Field(..., description="List of projects in the resume")
    formatting: FormattingFeedback = Field(..., description="Feedback on the resume's formatting")