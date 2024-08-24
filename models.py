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

class ResumeFeedback(BaseModel):
    experiences: list[ResumeExperience] = Field(..., description="List of experiences in the resume")
    projects: list[ResumeProject] = Field(..., description="List of projects in the resume")