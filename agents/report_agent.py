def report_node(state):
    """Generate final structured report for the user."""
    
    repository = state.get("repository", {})
    repo_understanding = state.get("repository_understanding", {})
    architecture = state.get("architecture", {})
    issue_intel = state.get("issue_intelligence", {})
    plan = state.get("plan", {})
    learning = state.get("learning_path", {})
    
    state["report"] = {
        "repository": {
            "name": repository.get("name"),
            "owner": repository.get("owner"),
            "description": repository.get("description"),
            "language": repository.get("language"),
            "stars": repository.get("stars"),
            "url": f"https://github.com/{repository.get('owner')}/{repository.get('name')}",
        },
        "understanding": {
            "purpose": repo_understanding.get("purpose"),
            "summary": repo_understanding.get("summary"),
            "technologies": repo_understanding.get("technologies"),
            "beginner_explanation": repo_understanding.get("beginner_explanation"),
        },
        "architecture": {
            "summary": architecture.get("architecture_summary"),
            "main_modules": [m["name"] for m in architecture.get("main_modules", [])],
            "entry_points": architecture.get("entry_points", []),
            "reading_order": architecture.get("reading_order", []),
        },
        "recommended_issue": issue_intel.get("top_recommendation"),
        "all_ranked_issues": issue_intel.get("ranked_issues", []),
        "contribution_plan": plan,
        "learning_roadmap": learning,
        "next_steps": [
            "1. Fork the repository",
            "2. Clone your fork locally",
            "3. Set up development environment",
            "4. Read the contribution guide",
            "5. Start with the learning roadmap",
            "6. Implement the contribution",
            "7. Submit a pull request",
        ],
    }
    
    state["execution"]["current_stage"] = "report_generated"
    state["execution"]["status"] = "completed"
    return state