from pydantic import BaseModel


class RepositoryUnderstanding(BaseModel):
    purpose: str
    summary: str
    technologies: list[str]
    beginner_explanation: str