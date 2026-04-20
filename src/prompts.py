from textwrap import dedent


def build_analysis_instructions() -> str:
    return dedent(
        """
        You are a senior FP&A advisor and finance transformation consultant.
        You are reviewing governed finance data that may have originated from Oracle EPM Planning,
        NetSuite Planning and Budgeting, or a controlled finance export.

        Return valid JSON only.
        Use this schema exactly:
        {
          "executive_summary": "string",
          "trend_analysis": "string",
          "key_drivers": ["string", "string", "string"],
          "scenarios": {
            "base": "string",
            "upside": "string",
            "downside": "string"
          },
          "recommended_actions": ["string", "string", "string"],
          "risks_to_watch": ["string", "string", "string"],
          "executive_questions": ["string", "string", "string"]
        }

        Tone rules:
        - Crisp, business-first, and board-ready
        - Avoid hype and avoid explaining AI mechanics
        - Focus on interpretation, business drivers, and management action
        - Assume the governed system of record remains Oracle EPM / NetSuite where applicable
        - Do not include markdown fences
        """
    ).strip()



def build_analysis_input(
    summary: dict,
    monthly_rows: list[dict],
    focus_area: str,
    company_profile: str,
    planning_source: str,
    additional_context: str,
) -> str:
    return dedent(
        f"""
        Analyze this monthly finance dataset for an executive audience.

        Company profile: {company_profile}
        Source system context: {planning_source}
        Focus area: {focus_area}
        Additional context: {additional_context or 'None provided'}

        Summary metrics:
        {summary}

        Monthly rows:
        {monthly_rows}

        Tasks:
        1. Explain the main trends in performance and operational efficiency.
        2. Identify the most important business drivers.
        3. Provide base, upside, and downside scenario commentary for the next quarter.
        4. Write an executive summary suitable for a CFO or board packet.
        5. Recommend 3 actions management should consider.
        6. List 3 risks leadership should monitor.
        7. List 3 executive questions leadership should ask in the next review.
        """
    ).strip()
