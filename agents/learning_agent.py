def learning_node(state):
    """Generate learning roadmap based on the issue and repository."""
    
    issue_intel = state.get("issue_intelligence", {})
    top_issue = issue_intel.get("top_recommendation")
    repo_understanding = state.get("repository_understanding", {})
    architecture = state.get("architecture", {})
    
    # Stub implementation - will be enhanced later
    state["learning_path"] = {
        "prerequisites": [
            "Git & GitHub basics",
            "Python fundamentals" if repo_understanding.get("technologies", []) else "Programming basics",
        ],
        "concepts_to_learn": [
            "Repository structure and architecture",
            "Issue domain knowledge",
            "Testing practices",
        ],
        "resources": [
            "Project README and CONTRIBUTING guide",
            "Official documentation for technologies used",
        ],
        "estimated_study_hours": 5,
        "sequence": [
            "1. Read project documentation",
            "2. Understand the issue context",
            "3. Explore relevant code modules",
            "4. Practice with similar examples",
        ],
    }
    
    state["execution"]["current_stage"] = "learning_completed"
    return state