import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.builder import graph

st.set_page_config(
    page_title="OSCA - Open Source Contribution Assistant",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Open Source Contribution Assistant (OSCA)")
st.markdown("""
Enter a GitHub repository URL and OSCA will analyze it to help you make your first open-source contribution.
""")

# Input
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/owner/repo",
    help="Enter any public GitHub repository URL"
)

if st.button("Analyze Repository", type="primary", disabled=not repo_url):
    if not repo_url.startswith("https://github.com/"):
        st.error("Please enter a valid GitHub URL (https://github.com/...)")
    else:
        initial_state = {
            "repository_url": repo_url,
            "repository": {},
            "repository_understanding": {},
            "architecture": {},
            "issue_intelligence": {},
            "plan": {},
            "learning_path": {},
            "report": {},
            "execution": {
                "current_stage": "start",
                "status": "running",
            },
        }

        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        stages = [
            ("repository_fetch", "Fetching repository data..."),
            ("repository_understanding", "Understanding repository purpose..."),
            ("architecture", "Analyzing architecture..."),
            ("issue_intelligence", "Finding beginner-friendly issues..."),
            ("planner", "Generating contribution plan..."),
            ("learning", "Creating learning roadmap..."),
            ("report", "Generating final report..."),
        ]

        try:
            # Run the full workflow
            status_text.text("Running analysis...")
            result = graph.invoke(initial_state)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")

            st.success(f"Analysis complete for: {repo_url}")

            # Repository Understanding
            st.header("📋 Repository Understanding")
            ru = result["repository_understanding"]
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Purpose")
                st.write(ru["purpose"])
                st.subheader("Summary")
                st.write(ru["summary"])
            with col2:
                st.subheader("Technologies")
                st.write(", ".join(ru["technologies"]))
                st.subheader("Beginner Explanation")
                st.write(ru["beginner_explanation"])

            # Architecture Analysis
            st.header("🏗️ Architecture Analysis")
            arch = result["architecture"]
            st.subheader("Architecture Summary")
            st.write(arch["architecture_summary"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Reading Order")
                for idx, item in enumerate(arch["reading_order"], 1):
                    st.write(f"{idx}. {item}")
            with col2:
                st.subheader("Entry Points")
                for idx, item in enumerate(arch["entry_points"], 1):
                    st.write(f"{idx}. {item}")

            st.subheader("Main Modules")
            for module in arch["main_modules"]:
                with st.expander(module["name"]):
                    st.write(module["purpose"])

            # Issue Intelligence
            st.header("🎯 Issue Intelligence")
            ii = result["issue_intelligence"]
            st.write(f"**Total issues fetched:** {ii.get('total_fetched', 0)}  |  **Beginner-relevant:** {ii.get('filtered_count', 0)}")
            
            if ii.get("top_recommendation"):
                top = ii["top_recommendation"]
                st.subheader("🏆 Top Recommendation")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Score", f"{top['score']}/100")
                with col2:
                    st.metric("Difficulty", top['difficulty'].capitalize())
                with col3:
                    st.metric("Estimated Hours", top['estimated_hours'])
                
                st.write(f"**Issue:** [#{top['issue']['number']}]({top['issue']['url']}) - {top['issue']['title']}")
                st.write(f"**Labels:** {', '.join(top['issue']['labels']) if top['issue']['labels'] else 'none'}")
                st.write(f"**Reasoning:** {top['reasoning']}")
                st.write(f"**Suggested Approach:** {top['suggested_approach']}")
                
                st.subheader("All Ranked Issues")
                for idx, r in enumerate(ii.get("ranked_issues", []), 1):
                    with st.expander(f"#{idx} - Issue #{r['issue']['number']} ({r['score']}/100) - {r['issue']['title'][:80]}"):
                        st.write(f"**Difficulty:** {r['difficulty'].capitalize()}  |  **Est. Hours:** {r['estimated_hours']}")
                        st.write(f"**Reasoning:** {r['reasoning']}")
                        st.write(f"**Approach:** {r['suggested_approach']}")
                        st.write(f"**URL:** [{r['issue']['url']}]({r['issue']['url']})")
            else:
                st.warning("No beginner-friendly issues found. Try a different repository.")

            # Contribution Plan
            st.header("📋 Contribution Plan")
            plan = result.get("plan", {})
            if plan and not plan.get("error"):
                st.write(f"**Issue:** #{plan.get('issue_number', 'N/A')} - {plan.get('issue_title', 'N/A')}")
                st.write(f"**Difficulty:** {plan.get('difficulty', 'N/A')}")
                st.write(f"**Estimated Hours:** {plan.get('estimated_hours', 'N/A')}")
                st.subheader("Files to Modify")
                for f in plan.get("files_to_modify", ["TBD"]):
                    st.write(f"- {f}")
                st.subheader("Implementation Steps")
                for i, step in enumerate(plan.get("implementation_steps", []), 1):
                    st.write(f"{i}. {step}")
                if plan.get("risks"):
                    st.subheader("Risks")
                    for risk in plan["risks"]:
                        st.write(f"- ⚠️ {risk}")
            else:
                st.info("Plan will be generated after issue analysis.")

            # Learning Path
            st.header("📚 Learning Roadmap")
            learning = result.get("learning_path", {})
            if learning:
                st.subheader("Prerequisites")
                for p in learning.get("prerequisites", []):
                    st.write(f"- {p}")
                st.subheader("Concepts to Learn")
                for c in learning.get("concepts_to_learn", []):
                    st.write(f"- {c}")
                st.subheader("Resources")
                for r in learning.get("resources", []):
                    st.write(f"- {r}")
                st.write(f"**Estimated Study Hours:** {learning.get('estimated_study_hours', 0)}")
                st.subheader("Learning Sequence")
                for step in learning.get("sequence", []):
                    st.write(f"- {step}")
            else:
                st.info("Learning roadmap will be generated after planning.")

            # Final Report
            st.header("📊 Final Report")
            report = result.get("report", {})
            if report:
                st.json(report)
            else:
                st.info("Report will be generated at the end of the workflow.")

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.exception(e)

# Sidebar info
with st.sidebar:
    st.header("About OSCA")
    st.markdown("""
    **Open Source Contribution Assistant** helps beginners make their first successful open-source contribution.
    
    **Workflow:**
    1. Enter GitHub URL
    2. Repository Analysis
    3. Repository Understanding
    4. Architecture Analysis
    5. Issue Intelligence ✅
    6. Contribution Planning ✅
    7. Learning Roadmap ✅
    8. Final Report ✅
    
    **Built with:**
    - LangGraph (workflow)
    - NVIDIA Nemotron (LLM)
    - GitHub API
    - Streamlit (UI)
    """)