from __future__ import annotations

import json
from io import StringIO

import streamlit as st

from src.analysis import (
    build_board_memo_markdown,
    build_dataset_summary,
    generate_ai_analysis,
    validate_finance_dataframe,
)
from src.charts import (
    build_ebitda_chart,
    build_headcount_chart,
    build_margin_chart,
    build_revenue_chart,
)
from src.data_utils import load_dataframe_from_upload
from src.epm import (
    build_epm_integration_notes,
    build_epm_mapping_table,
    build_reference_architecture,
)

st.set_page_config(page_title="AI FP&A Copilot", page_icon="📈", layout="wide")

st.title("AI FP&A Copilot")
st.caption(
    "Portfolio demo: an AI layer on top of governed finance data, designed to illustrate how Oracle EPM / NetSuite exports can be turned into executive-ready insight."
)

with st.sidebar:
    st.header("Run settings")
    uploaded_file = st.file_uploader("Upload monthly finance CSV", type=["csv"])
    use_sample = st.checkbox("Use included sample dataset", value=True)
    company_profile = st.selectbox(
        "Company profile",
        ["B2B SaaS", "Multi-entity services", "Consumer products", "Custom"],
    )
    focus_area = st.selectbox(
        "Primary focus",
        [
            "Board summary",
            "Forecast scenarios",
            "Cost discipline",
            "Headcount efficiency",
            "Cash and margin",
        ],
    )
    planning_source = st.selectbox(
        "Source system context",
        ["Oracle EPM Planning", "NetSuite Planning and Budgeting", "CSV export only"],
    )
    additional_context = st.text_area(
        "Business context",
        placeholder=(
            "Example: Mid-market SaaS company preparing for Q3 board review. "
            "Focus on revenue durability, margin pressure, and hiring pace."
        ),
        height=150,
    )
    run_analysis = st.button("Generate portfolio analysis", type="primary", use_container_width=True)

if use_sample and uploaded_file is None:
    with open("sample_data/demo_financials.csv", "r", encoding="utf-8") as f:
        uploaded_file = StringIO(f.read())

if uploaded_file is None:
    st.info("Upload a CSV or leave the sample dataset enabled.")
    st.stop()

try:
    df = load_dataframe_from_upload(uploaded_file)
    df = validate_finance_dataframe(df)
except Exception as exc:
    st.error(f"Could not load the file: {exc}")
    st.stop()

summary = build_dataset_summary(df)
mapping_df = build_epm_mapping_table(df)
integration_notes = build_epm_integration_notes(planning_source)
architecture_text = build_reference_architecture(planning_source)

hero1, hero2, hero3, hero4 = st.columns(4)
hero1.metric("Periods", summary["periods"])
hero2.metric("Total revenue", f"${summary['total_revenue']:,.0f}")
hero3.metric("Revenue growth", f"{summary['revenue_growth_pct']:.1f}%")
hero4.metric("Avg EBITDA margin", f"{summary['average_ebitda_margin_pct']:.1f}%")

preview_tab, insight_tab, epm_tab, repo_tab = st.tabs(
    ["Dataset & Charts", "AI Narrative", "Oracle / NetSuite EPM Story", "Portfolio Notes"]
)

with preview_tab:
    left, right = st.columns([1.05, 0.95])
    with left:
        st.subheader("Dataset preview")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Summary metrics")
        st.json(summary)

    with right:
        st.subheader("Revenue trend")
        st.pyplot(build_revenue_chart(df))

        st.subheader("EBITDA trend")
        st.pyplot(build_ebitda_chart(df))

        chart_left, chart_right = st.columns(2)
        with chart_left:
            st.subheader("EBITDA margin")
            st.pyplot(build_margin_chart(df))
        with chart_right:
            st.subheader("Headcount")
            st.pyplot(build_headcount_chart(df))

with insight_tab:
    st.subheader("Executive-ready AI commentary")
    st.write(
        "This is the part of the demo that shows how governed financial data can be transformed into board-ready narrative, drivers, and next-step recommendations."
    )

    if run_analysis:
        with st.spinner("Generating AI narrative..."):
            try:
                result = generate_ai_analysis(
                    df=df,
                    summary=summary,
                    focus_area=focus_area,
                    company_profile=company_profile,
                    planning_source=planning_source,
                    additional_context=additional_context,
                )
            except Exception as exc:
                st.error(f"AI analysis failed: {exc}")
                st.stop()

        memo_text = build_board_memo_markdown(result, summary, planning_source)

        a, b = st.columns([1.05, 0.95])
        with a:
            st.markdown("### Executive summary")
            st.write(result.get("executive_summary", ""))

            st.markdown("### Trend analysis")
            st.write(result.get("trend_analysis", ""))

            st.markdown("### Key drivers")
            for item in result.get("key_drivers", []):
                st.write(f"- {item}")

            st.markdown("### Management actions")
            for item in result.get("recommended_actions", []):
                st.write(f"- {item}")

        with b:
            st.markdown("### Forecast scenarios")
            scenarios = result.get("scenarios", {})
            for name in ["base", "upside", "downside"]:
                if name in scenarios:
                    st.markdown(f"**{name.title()}**")
                    st.write(scenarios[name])

            st.markdown("### Risks to watch")
            for item in result.get("risks_to_watch", []):
                st.write(f"- {item}")

            st.markdown("### Suggested executive questions")
            for item in result.get("executive_questions", []):
                st.write(f"- {item}")

        st.download_button(
            "Download analysis JSON",
            data=json.dumps(result, indent=2),
            file_name="ai_fpa_analysis.json",
            mime="application/json",
        )
        st.download_button(
            "Download board memo (Markdown)",
            data=memo_text,
            file_name="board_memo.md",
            mime="text/markdown",
        )
    else:
        st.info("Click **Generate portfolio analysis** in the sidebar to produce the AI narrative.")

with epm_tab:
    st.subheader("How this fits Oracle EPM / NetSuite Planning")
    st.write(
        "This framing is what turns the app from a generic AI demo into a finance transformation use case. The goal is not to replace governed planning tools, but to add an AI interpretation layer on top of approved exports and planning snapshots."
    )

    left, right = st.columns([0.95, 1.05])
    with left:
        st.markdown("### Example source mapping")
        st.dataframe(mapping_df, use_container_width=True, hide_index=True)

        st.markdown("### Integration notes")
        for item in integration_notes:
            st.write(f"- {item}")

    with right:
        st.markdown("### Reference architecture")
        st.code(architecture_text, language="text")

        st.markdown("### Positioning statement")
        st.info(
            "Governed planning, approvals, and multidimensional models stay in Oracle EPM / NetSuite. "
            "The AI layer accelerates interpretation, executive summarization, and scenario storytelling using controlled exports or API-driven extracts."
        )

with repo_tab:
    st.subheader("What makes this portfolio-ready")
    st.markdown(
        """
        - Clean Streamlit UI with clear business story
        - Sample dataset designed for board-style commentary
        - Oracle / NetSuite EPM integration framing for your niche
        - Exportable board memo for a practical deliverable
        - Clear repo structure so a hiring team can scan it quickly
        """
    )

    st.markdown("### Suggested GitHub description")
    st.code(
        "AI FP&A Copilot: a portfolio demo showing how Oracle EPM / NetSuite finance data can be turned into executive narrative and scenario insight using the OpenAI Responses API.",
        language="text",
    )

    st.markdown("### Suggested screenshots")
    st.write("1. Hero metrics + charts")
    st.write("2. AI Narrative tab with executive summary and scenarios")
    st.write("3. Oracle / NetSuite EPM Story tab showing mapping and architecture")
