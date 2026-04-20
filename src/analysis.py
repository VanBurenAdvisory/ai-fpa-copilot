from __future__ import annotations

import json
import time
from typing import Any

import pandas as pd
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError

from src.config import OPENAI_API_KEY, OPENAI_MODEL
from src.prompts import build_analysis_input, build_analysis_instructions

REQUIRED_COLUMNS = {"month", "revenue", "opex", "headcount"}
OPTIONAL_NUMERIC_COLUMNS = {"cogs", "gross_margin", "ebitda", "cash"}


def validate_finance_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    for col in REQUIRED_COLUMNS.union(OPTIONAL_NUMERIC_COLUMNS):
        if col in df.columns and col != "month":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[["revenue", "opex", "headcount"]].isna().any().any():
        raise ValueError("One or more required numeric fields contain invalid values")

    if "ebitda" not in df.columns:
        if "cogs" in df.columns:
            df["ebitda"] = df["revenue"] - df["cogs"] - df["opex"]
        else:
            df["ebitda"] = df["revenue"] - df["opex"]

    if "gross_margin" not in df.columns:
        if "cogs" in df.columns:
            df["gross_margin"] = df["revenue"] - df["cogs"]
        else:
            df["gross_margin"] = df["revenue"]

    df["ebitda_margin_pct"] = (df["ebitda"] / df["revenue"] * 100).round(2)
    return df


def build_dataset_summary(df: pd.DataFrame) -> dict[str, Any]:
    revenue_start = float(df["revenue"].iloc[0])
    revenue_end = float(df["revenue"].iloc[-1])
    ebitda_start = float(df["ebitda"].iloc[0])
    ebitda_end = float(df["ebitda"].iloc[-1])
    headcount_start = float(df["headcount"].iloc[0])
    headcount_end = float(df["headcount"].iloc[-1])

    revenue_growth_pct = ((revenue_end - revenue_start) / revenue_start * 100) if revenue_start else 0
    ebitda_change = ebitda_end - ebitda_start
    headcount_growth_pct = ((headcount_end - headcount_start) / headcount_start * 100) if headcount_start else 0

    avg_ebitda_margin = float(df["ebitda_margin_pct"].mean())
    latest_ebitda_margin = float(df["ebitda_margin_pct"].iloc[-1])

    return {
        "periods": int(len(df)),
        "total_revenue": round(float(df["revenue"].sum()), 2),
        "average_revenue": round(float(df["revenue"].mean()), 2),
        "average_opex": round(float(df["opex"].mean()), 2),
        "average_headcount": round(float(df["headcount"].mean()), 2),
        "average_ebitda": round(float(df["ebitda"].mean()), 2),
        "average_ebitda_margin_pct": round(avg_ebitda_margin, 2),
        "latest_ebitda_margin_pct": round(latest_ebitda_margin, 2),
        "revenue_growth_pct": round(revenue_growth_pct, 2),
        "headcount_growth_pct": round(headcount_growth_pct, 2),
        "ebitda_change": round(float(ebitda_change), 2),
    }


def _clean_json_response(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    return json.loads(text)


def generate_ai_analysis(
    df: pd.DataFrame,
    summary: dict[str, Any],
    focus_area: str,
    company_profile: str,
    planning_source: str,
    additional_context: str,
) -> dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=OPENAI_API_KEY, timeout=60)
    monthly_rows = df.to_dict(orient="records")

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = client.responses.create(
                model=OPENAI_MODEL,
                instructions=build_analysis_instructions(),
                input=build_analysis_input(
                    summary=summary,
                    monthly_rows=monthly_rows,
                    focus_area=focus_area,
                    company_profile=company_profile,
                    planning_source=planning_source,
                    additional_context=additional_context,
                ),
            )
            return _clean_json_response(response.output_text)
        except (RateLimitError, APIConnectionError, APIError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(2**attempt)
            else:
                raise
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Model response was not valid JSON. Try again or tighten the prompt."
            ) from exc

    raise RuntimeError(f"AI analysis failed: {last_error}")


def build_board_memo_markdown(result: dict[str, Any], summary: dict[str, Any], planning_source: str) -> str:
    drivers = "\n".join(f"- {item}" for item in result.get("key_drivers", []))
    actions = "\n".join(f"- {item}" for item in result.get("recommended_actions", []))
    risks = "\n".join(f"- {item}" for item in result.get("risks_to_watch", []))
    questions = "\n".join(f"- {item}" for item in result.get("executive_questions", []))
    scenarios = result.get("scenarios", {})

    return f"""# Board Memo Draft\n\n**Source context:** {planning_source}\n\n## Snapshot\n- Periods analyzed: {summary['periods']}\n- Total revenue: ${summary['total_revenue']:,.0f}\n- Revenue growth: {summary['revenue_growth_pct']:.1f}%\n- Average EBITDA margin: {summary['average_ebitda_margin_pct']:.1f}%\n\n## Executive Summary\n{result.get('executive_summary', '')}\n\n## Trend Analysis\n{result.get('trend_analysis', '')}\n\n## Key Drivers\n{drivers}\n\n## Forecast Scenarios\n### Base\n{scenarios.get('base', '')}\n\n### Upside\n{scenarios.get('upside', '')}\n\n### Downside\n{scenarios.get('downside', '')}\n\n## Recommended Actions\n{actions}\n\n## Risks to Watch\n{risks}\n\n## Questions for Leadership\n{questions}\n"""
