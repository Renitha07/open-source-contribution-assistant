from pydantic import BaseModel
from typing import Optional


class IssueInfo(BaseModel):
    number: int
    title: str
    url: str
    labels: list[str]
    created_at: str
    comments: int


class RankedIssue(BaseModel):
    issue: IssueInfo
    score: float
    reasoning: str
    difficulty: str
    estimated_hours: int
    suggested_approach: str


class IssueIntelligence(BaseModel):
    total_fetched: int
    filtered_count: int
    ranked_issues: list[RankedIssue]
    top_recommendation: Optional[RankedIssue] = None