# Architecture Notes

## Positioning

This is not meant to replace Oracle EPM or NetSuite Planning and Budgeting.

It is meant to demonstrate a practical pattern:
1. governed planning data stays in the finance platform
2. approved exports or API extracts feed a lightweight AI workflow
3. AI generates narrative, driver commentary, and scenario framing
4. finance leadership reviews the result before wider distribution

## Reference flow

Oracle EPM / NSPB / controlled CSV export  
→ Python transformation layer  
→ OpenAI Responses API  
→ Streamlit review app  
→ board memo or management discussion draft

## Why this matters

Most finance organizations do not need AI to replace the planning tool.
They need AI to reduce the effort involved in:
- synthesizing monthly results
- drafting commentary
- framing risks and scenarios
- preparing board summaries
