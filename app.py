import streamlit as st
import pandas as pd
from agent import build_graph

# Wide layout
st.set_page_config(
    layout="wide",
    page_title="Strategic Research Analyst",
    page_icon="🧠"
)

st.markdown(
    """
    <h1 style='text-align: center;'>🧠 Strategic Research Analyst Agent</h1>
    <p style='text-align: center; color: gray;'>
    Autonomous multi-step AI agent for structured research, evidence evaluation, and strategic synthesis.
    </p>
    """,
    unsafe_allow_html=True
)

question = st.text_input("Enter your research question:")

if st.button("Analyze") and question:
    graph = build_graph()

    initial_state = {
        "question": question,
        "domain": "",
        "strategy": "",
        "queries": [],
        "raw_evidence": [],
        "scored_evidence": [],
        "report": "",
        "conflicts": "",
        "confidence": 0.0,
        "confidence_history": [],
        "iteration": 0,
        "thinking_log": []
    }

    result = graph.invoke(initial_state)

    left_col, right_col = st.columns([1, 2])

    # ==============================
    # LEFT PANEL → Agent Intelligence
    # ==============================
    with left_col:
        st.subheader("🧠 Agent Intelligence")

        # Domain
        st.markdown("### 📌 Domain")
        st.write(result.get("domain", ""))

        # Confidence
        st.markdown("### 📊 Confidence Score")
        confidence = result.get("confidence", 0.0)
        st.write(confidence)

        if confidence >= 0.75:
            st.success("High confidence in gathered evidence.")
        elif confidence >= 0.5:
            st.warning("Moderate confidence. Some uncertainty remains.")
        else:
            st.error("Low confidence. Evidence may be weak or conflicting.")

        # Iterations
        st.markdown("### 🔁 Iterations")
        st.write(result.get("iteration", 0))

        # Confidence Evolution Chart
        if result.get("confidence_history"):
            st.markdown("### 📈 Confidence Evolution")
            history_df = pd.DataFrame({
                "Iteration": range(len(result["confidence_history"])),
                "Confidence": result["confidence_history"]
            })
            st.line_chart(history_df.set_index("Iteration"))

        # Strategy
        with st.expander("Strategic Dimensions"):
            st.write(result.get("strategy", ""))

        # Queries
        with st.expander("Generated Research Queries"):
            for q in result.get("queries", []):
                st.write("•", q)

        # Evidence + Bar Chart
        with st.expander("Evidence Ranking"):
            evidence = result.get("scored_evidence", [])
            if evidence:
                sorted_evidence = sorted(
                    evidence,
                    key=lambda x: x["final_score"],
                    reverse=True
                )

                top_evidence = sorted_evidence[:5]

                df = pd.DataFrame(top_evidence)
                st.bar_chart(df.set_index("url")["final_score"])

                for item in top_evidence:
                    st.markdown(f"**Score:** {item['final_score']}")
                    st.markdown(f"🔗 {item['url']}")
                    st.markdown("---")
            else:
                st.write("No evidence found.")

        # Thinking Log
        with st.expander("Agent Thinking Log", expanded=True):
            for log in result.get("thinking_log", []):
                st.write("•", log)

    # ==============================
    # RIGHT PANEL → Strategic Report
    # ==============================
    with right_col:
        st.subheader("📊 Strategic Intelligence Report")

        report = result.get("report", "")

        # Executive Summary Highlight
        if report:
            first_section = report.split("\n")[0]
            st.success("Executive Summary: " + first_section)

        # Conflict Section
        if result.get("conflicts"):
            st.markdown("### ⚖ Conflicting Perspectives")
            st.write(result["conflicts"])

        # Full Report
        if report:
            st.markdown("---")
            st.markdown(report)
        else:
            st.write("Report not generated.")

        st.markdown("---")

        st.download_button(
            label="Download Strategic Report",
            data=report,
            file_name="strategic_analysis.txt"
        )