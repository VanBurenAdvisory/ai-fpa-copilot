# AI FP&A Copilot

An AI-powered financial planning assistant that transforms raw financial data into executive-ready insights, forecasts, and scenario analysis.

---

## 🚀 Overview

AI FP&A Copilot demonstrates how Large Language Models (LLMs) can augment — not replace — enterprise planning platforms like Oracle EPM and NetSuite Planning.

This project simulates a real-world workflow:

* Export financial data from EPM / ERP
* Run AI-driven analysis
* Generate executive-level insights instantly

---

## 💡 Why This Matters

Finance teams today face a gap:

| Traditional EPM           | AI Capabilities          |
| ------------------------- | ------------------------ |
| Structured, governed data | Rapid, flexible analysis |
| Auditability              | Narrative generation     |
| Workflow & controls       | Scenario exploration     |

👉 The opportunity is combining both.

This project represents a **Hybrid Planning Model**:

* **EPM** = system of record
* **AI** = system of insight

---

## 🧠 Key Features

* 📂 Upload financial CSV data
* 📊 Automated trend and KPI analysis
* 🤖 AI-generated:

  * Executive summary
  * Key business drivers
  * Risk assessment
  * Scenario modeling (Base / Upside / Downside)
* 📈 Visualization of revenue and margin trends
* 📝 Exportable board-level narrative

---

## 🏗️ Architecture

```text
[ Oracle EPM / NetSuite ]
            ↓
     CSV Export Layer
            ↓
   Python + Pandas Processing
            ↓
   OpenAI API (LLM Analysis)
            ↓
   Streamlit UI (Insights + Charts)
```

---

## 🔗 EPM Integration Perspective

This is not a replacement for Oracle EPM or NetSuite Planning.

Instead, it represents an **AI augmentation layer**:

| Function                 | System     |
| ------------------------ | ---------- |
| Consolidation / Close    | EPM        |
| Budgeting Workflow       | EPM        |
| Ad-hoc Scenario Analysis | AI Copilot |
| Executive Narrative      | AI Copilot |

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/VanBurenAdvisory/ai-fpa-copilot.git
cd ai-fpa-copilot
```

---

### 2. Set up environment

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

---

### 3. Add your API key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📊 Sample Data

Use:

```
sample_data/demo_financials.csv
```

---

## 🎯 Use Case

This project is designed for:

* Finance leaders exploring AI adoption
* EPM consultants extending their value beyond implementation
* Organizations evaluating AI-driven planning workflows

---

## 🧭 Future Enhancements

* Direct API integration with NetSuite / Oracle EPM
* Automated data pipelines (OCI / S3 / Snowflake)
* Multi-entity consolidation simulation
* Power BI / dashboard integration

---

## 👤 Author

Jason Wells
AI & Finance Technology Leader | EPM SME | Solutions Architect

---

## ⚠️ Disclaimer

This is a demonstration project intended for educational and exploratory purposes. Not intended for production financial reporting without validation controls.
