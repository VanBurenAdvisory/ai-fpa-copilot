# AI FP&A Copilot

A portfolio-ready demo showing how governed finance data can be turned into executive narrative, driver analysis, and scenario commentary using the OpenAI Responses API.

This project is intentionally positioned as an **AI layer on top of Oracle EPM / NetSuite Planning exports**, not as a replacement for governed planning tools. The point is to show how AI can accelerate interpretation, board prep, and scenario storytelling while the system of record remains the planning platform.

## Why this repo exists

This is designed as a hiring portfolio project for roles that sit between:
- customer success
- solution architecture
- AI adoption
- enterprise workflow design

It demonstrates the ability to:
- turn raw finance data into usable workflows
- connect business context to AI outputs
- position AI within a real enterprise architecture
- communicate clearly to executive audiences

## What the app does

- Upload a monthly finance CSV
- Validate the dataset with pandas
- Generate summary metrics and charts
- Call the OpenAI Responses API for:
  - executive summary
  - trend analysis
  - key drivers
  - base / upside / downside scenarios
  - recommended actions
  - risks to watch
  - executive questions
- Export a board memo draft in Markdown
- Show how the use case maps back to Oracle EPM / NetSuite Planning

## UI sections

### 1. Dataset & Charts
A quick review surface for uploaded data, summary metrics, and visual trends.

### 2. AI Narrative
The core portfolio demo. This is where the app produces CFO-ready commentary and scenario framing.

### 3. Oracle / NetSuite EPM Story
A positioning tab that explains how this app would sit alongside governed planning systems.

### 4. Portfolio Notes
Suggested GitHub positioning and screenshot ideas.

## Expected CSV columns

Required:
- `month`
- `revenue`
- `opex`
- `headcount`

Optional:
- `cogs`
- `gross_margin`
- `ebitda`
- `cash`

If `ebitda` is not provided, the app estimates it.

## Quickstart

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Then set your API key in `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.4
```

## Suggested screenshots for GitHub

1. Main dashboard with hero metrics and charts
2. AI Narrative tab with executive summary and scenarios
3. Oracle / NetSuite EPM Story tab with mapping table and reference architecture

## Suggested resume bullet

Built an AI-powered FP&A Copilot using Python, Streamlit, pandas, and the OpenAI Responses API to transform governed finance exports into executive summaries, scenario analysis, and board-ready commentary.

## Suggested LinkedIn framing

I built a lightweight AI FP&A Copilot to explore how Oracle EPM / NetSuite planning data can be paired with LLMs for board prep, scenario storytelling, and executive narrative generation—without replacing the governed planning system underneath.

## Technical notes

This repo uses the current OpenAI Python SDK pattern with `from openai import OpenAI` and `client.responses.create(...)`. It also includes basic retry handling for transient API and rate-limit errors.
