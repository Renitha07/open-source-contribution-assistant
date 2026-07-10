def planner_node(state):
    """Generate contribution plan for the top recommended issue."""
    
    issue_intel = state.get("issue_intelligence", {})
    top_issue = issue_intel.get("top_recommendation")
    
    if not top_issue:
        state["plan"] = {"error": "No issues to plan for"}
        state["execution"]["current_stage"] = "planning_failed"
        return state
    
    # Stub implementation - will be enhanced later
    state["plan"] = {
        "issue_number": top_issue["issue"]["number"],
        "issue_title": top_issue["issue"]["title"],
        "files_to_modify": ["TBD - analyze repository structure"],
        "implementation_steps": [
            "1. Study the issue and related code",
            "2. Set up development environment",
            "3. Implement the fix/feature",
            "4. Write tests",
            "5. Submit pull request"
        ],
        "difficulty": top_issue["difficulty"],
        "estimated_hours": top_issue["estimated_hours"],
        "risks": ["May require understanding unfamiliar codebase areas"],
    }
    
    state["execution"]["current_stage"] = "planning_completed"
    return state