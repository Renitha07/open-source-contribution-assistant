import json
import logging
from typing import Any

from prompts.issue_intelligence import SYSTEM_PROMPT
from schemas.issue_schema import IssueIntelligence, IssueInfo, RankedIssue
from state.graph_state import GraphState
from tools.github_tool import GitHubTool
from utils.llm_service import invoke_llm

logger = logging.getLogger(__name__)

github_tool = GitHubTool()

BEGINNER_LABELS = [
    "good first issue",
    "good-first-issue",
    "first-timers-only",
    "starter",
    "help wanted",
    "help-wanted",
    "documentation",
    "docs",
    "bug",
    "easy",
]


def _build_issue_prompt(issues: list[dict]) -> str:
    """Build user prompt with issue data for LLM ranking."""
    issue_summaries = []
    for issue in issues:
        summary = f"""
Issue #{issue['number']}: {issue['title']}
URL: {issue['url']}
Labels: {', '.join(issue['labels']) if issue['labels'] else 'none'}
Created: {issue['created_at']}
Comments: {issue['comments']}
Body: {issue['body'][:1500]}...
"""
        issue_summaries.append(summary)

    return f"""Analyze these GitHub issues and rank them by beginner-friendliness:

{'=' * 60}
{'\n\n'.join(issue_summaries)}
{'=' * 60}

Return JSON with ranked_issues array. Each entry must include: issue_number, score (0-100), reasoning, difficulty (easy/medium/hard), estimated_hours (int), suggested_approach (step-by-step)."""


def _parse_llm_response(response: str, issues: list[dict]) -> IssueIntelligence:
    """Parse and validate LLM response."""
    data = json.loads(response)

    issue_lookup = {issue["number"]: issue for issue in issues}

    ranked_issues = []
    for ranked in data["ranked_issues"]:
        issue_num = ranked["issue_number"]
        issue_data = issue_lookup.get(issue_num)

        if issue_data:
            issue_info = IssueInfo(
                number=issue_data["number"],
                title=issue_data["title"],
                url=issue_data["url"],
                labels=issue_data["labels"],
                created_at=issue_data["created_at"],
                comments=issue_data["comments"],
            )

            ranked_issue = RankedIssue(
                issue=issue_info,
                score=ranked["score"],
                reasoning=ranked["reasoning"],
                difficulty=ranked["difficulty"],
                estimated_hours=ranked["estimated_hours"],
                suggested_approach=ranked["suggested_approach"],
            )
            ranked_issues.append(ranked_issue)

    top_recommendation = ranked_issues[0] if ranked_issues else None

    return IssueIntelligence(
        total_fetched=len(issues),
        filtered_count=len(ranked_issues),
        ranked_issues=ranked_issues,
        top_recommendation=top_recommendation,
    )


def _fetch_issues_with_fallback(owner: str, name: str) -> list[dict]:
    """Fetch issues with beginner labels, fallback to all open issues."""
    repo_url = f"https://github.com/{owner}/{name}"

    issues = github_tool.get_issues(repo_url, labels=BEGINNER_LABELS, max_issues=30)

    if not issues:
        logger.info("No labeled issues found, fetching all open issues")
        issues = github_tool.get_issues(repo_url, max_issues=30)

    return issues


def issue_intelligence_node(state: GraphState) -> GraphState:
    """Fetch and rank beginner-friendly issues."""
    try:
        repo = state["repository"]
        owner = repo["owner"]
        name = repo["name"]

        logger.info(f"Fetching issues for {owner}/{name}")

        issues = _fetch_issues_with_fallback(owner, name)

        if not issues:
            logger.warning("No issues found in repository")
            state["issue_intelligence"] = IssueIntelligence(
                total_fetched=0,
                filtered_count=0,
                ranked_issues=[],
                top_recommendation=None,
            ).model_dump()
            state["execution"]["current_stage"] = "issues_analyzed"
            return state

        prompt = _build_issue_prompt(issues)
        logger.info(f"Analyzing {len(issues)} issues with LLM")

        response = invoke_llm(SYSTEM_PROMPT, prompt)

        intelligence = _parse_llm_response(response, issues)

        state["issue_intelligence"] = intelligence.model_dump()
        state["execution"]["current_stage"] = "issues_analyzed"
        state["execution"]["status"] = "running"

        logger.info(f"Ranked {len(intelligence.ranked_issues)} issues, top: {intelligence.top_recommendation}")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response as JSON: {e}")
        state["execution"]["status"] = "error"
        state["execution"]["error"] = f"LLM response parsing failed: {e}"
        state["issue_intelligence"] = IssueIntelligence(
            total_fetched=0,
            filtered_count=0,
            ranked_issues=[],
            top_recommendation=None,
        ).model_dump()

    except Exception as e:
        logger.error(f"Issue intelligence node failed: {e}")
        state["execution"]["status"] = "error"
        state["execution"]["error"] = str(e)
        state["issue_intelligence"] = IssueIntelligence(
            total_fetched=0,
            filtered_count=0,
            ranked_issues=[],
            top_recommendation=None,
        ).model_dump()

    return state