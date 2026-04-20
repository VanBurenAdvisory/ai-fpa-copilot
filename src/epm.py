from __future__ import annotations

import pandas as pd


def build_epm_mapping_table(df: pd.DataFrame) -> pd.DataFrame:
    available = set(df.columns)
    rows = [
        ["Month", "Period", "Time dimension / CSV export", "month" in available],
        ["Revenue", "Account: Revenue", "Data export / API extract", "revenue" in available],
        ["Opex", "Account: Operating Expense", "Data export / API extract", "opex" in available],
        ["Headcount", "Workforce or HR metric", "Joined from planning export", "headcount" in available],
        ["COGS", "Account: COGS", "Optional export field", "cogs" in available],
        ["EBITDA", "Calculated KPI", "Derived in app if missing", "ebitda" in available],
    ]
    return pd.DataFrame(rows, columns=["Business metric", "Typical EPM source", "How app uses it", "Present in file"])



def build_epm_integration_notes(planning_source: str) -> list[str]:
    common = [
        "Use approved exports or API-driven extracts rather than manual copy/paste.",
        "Keep planning, approvals, and dimensional governance in the source EPM platform.",
        "Use the AI layer for narrative generation, driver interpretation, and scenario storytelling.",
    ]

    if planning_source == "Oracle EPM Planning":
        common.insert(0, "Position this as a post-export narrative layer on top of Oracle EPM Planning data or reporting extracts.")
    elif planning_source == "NetSuite Planning and Budgeting":
        common.insert(0, "Position this as a NetSuite Planning and Budgeting companion that accelerates board commentary and scenario framing.")
    else:
        common.insert(0, "Use this mode when demonstrating value before wiring into a governed planning platform.")
    return common



def build_reference_architecture(planning_source: str) -> str:
    source = planning_source if planning_source != "CSV export only" else "Finance CSV / controlled export"
    return f"""{source}
    -> approved export or REST/API extract
    -> lightweight Python / pandas transformation layer
    -> OpenAI Responses API for executive narrative and scenario commentary
    -> Streamlit interface for review, charts, and memo export
    -> optional memo / board packet workflow"""
