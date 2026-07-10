#!/usr/bin/env python
"""
Run the OSCA workflow from terminal.
Usage: python run.py "https://github.com/owner/repo"
"""

import sys
import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

from graph.builder import graph


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"https://github.com/owner/repo\"")
        sys.exit(1)

    repo_url = sys.argv[1]

    initial_state = {
        "repository_url": repo_url,
        "repository": {},
        "repository_understanding": {},
        "architecture": {},
        "issue_intelligence": {},
        "execution": {
            "current_stage": "start",
            "status": "running",
        },
    }

    print(f"Analyzing: {repo_url}")
    print("=" * 60)

    result = graph.invoke(initial_state)

    print()
    print("=" * 60)
    print("REPOSITORY UNDERSTANDING")
    print("=" * 60)
    ru = result["repository_understanding"]
    print(f"Purpose: {ru['purpose']}")
    print(f"Summary: {ru['summary']}")
    print(f"Technologies: {', '.join(ru['technologies'])}")
    print(f"Beginner Explanation: {ru['beginner_explanation']}")

    print()
    print("=" * 60)
    print("ARCHITECTURE ANALYSIS")
    print("=" * 60)
    arch = result["architecture"]
    print(f"Architecture Summary: {arch['architecture_summary']}")
    print(f"Reading Order: {arch['reading_order']}")
    print(f"Entry Points: {arch['entry_points']}")
    print(f"Main Modules: {[m['name'] for m in arch['main_modules']]}")

    print()
    print("=" * 60)
    print("ISSUE INTELLIGENCE")
    print("=" * 60)
    issues = result.get("issue_intelligence", {})
    if issues:
        print(f"Total Fetched: {issues.get('total_fetched', 0)}")
        print(f"Ranked Issues: {issues.get('filtered_count', 0)}")
        
        top = issues.get("top_recommendation")
        if top:
            print(f"\nTOP RECOMMENDATION:")
            print(f"  Issue #{top['issue']['number']}: {top['issue']['title']}")
            print(f"  Score: {top['score']}/100")
            print(f"  Difficulty: {top['difficulty']}")
            print(f"  Estimated Hours: {top['estimated_hours']}")
            print(f"  Reasoning: {top['reasoning']}")
            print(f"  Approach: {top['suggested_approach']}")
        
        ranked = issues.get("ranked_issues", [])
        if ranked:
            print(f"\nALL RANKED ISSUES (top 5):")
            for i, issue in enumerate(ranked[:5], 1):
                print(f"  {i}. #{issue['issue']['number']}: {issue['issue']['title']} (Score: {issue['score']}, {issue['difficulty']})")

    print()
    print("=" * 60)
    print("CONTRIBUTION PLAN")
    print("=" * 60)
    plan = result.get("plan", {})
    if plan:
        print(f"Issue: #{plan.get('issue_number', 'N/A')}")
        print(f"Difficulty: {plan.get('difficulty', 'N/A')}")
        print(f"Estimated Hours: {plan.get('estimated_hours', 'N/A')}")
        print(f"Steps: {plan.get('implementation_steps', [])}")

    print()
    print("=" * 60)
    print("LEARNING PATH")
    print("=" * 60)
    learning = result.get("learning_path", {})
    if learning:
        print(f"Prerequisites: {learning.get('prerequisites', [])}")
        print(f"Concepts: {learning.get('concepts_to_learn', [])}")
        print(f"Estimated Study Hours: {learning.get('estimated_study_hours', 0)}")

    print()
    print(f"Final Stage: {result['execution']['current_stage']}")
    print(f"Status: {result['execution']['status']}")


if __name__ == "__main__":
    main()