# 🤖 AI Software Development Team (Multi-Agent)

> **Capstone Project — School of Computer Science & Artificial Intelligence (CS&AI)**
> **Project Team No:** 189 | **Semester:** VII Semester

---

## 👥 Project Team Members
| Roll No | Name | Role |
| :--- | :--- | :--- |
| **2303A52367** | **K. CHARAN YADAV** | Team Lead & Multi-Agent Architecture |
| **2303A51330** | **K. AKSHITHA** | Agent Orchestration & Backend Engine |
| **2303A51320** | **A. SHIVA SPANDANA** | QA Agent & Testing Automation |
| **2303A51321** | **CH. MANMITH VARDHAN** | Frontend UI & Interactive Visualizer |

---

## 📖 Abstract
The **AI Software Development Team – Multi-Agent System** is an autonomous AI-driven software engineering framework that automates the complete lifecycle of software creation. The system replaces traditional isolated generation with a collaborative multi-agent pipeline consisting of four specialized agents:

1. **Project Manager (PM) Agent**: Understands plain-English user requirements, devises architectural blueprints, selects optimal tech stacks, and breaks down deliverables into discrete tasks.
2. **Developer Agent**: Translates the PM specification into complete, runnable multi-file source code (backend APIs, frontend templates, styles, and configurations) with zero placeholders.
3. **Testing / QA Agent**: Performs Abstract Syntax Tree (AST) code analysis, generates automated unit test suites, executes verification checks, and triggers refinement loops if defects are found.
4. **Documentation Agent**: Compiles comprehensive `README.md` guides, setup instructions, and API references.

An **Orchestrator Engine** manages inter-agent communication, state persistence, and streams real-time thought feeds to an interactive modern web interface.

---

## 🏗️ Multi-Agent Architecture Workflow

```
               +----------------------------------+
               | User Requirement (Web Dashboard) |
               +-----------------+----------------+
                                 |
                                 v
               +----------------------------------+
               |   Orchestrator State Machine     |
               +-----------------+----------------+
                                 |
        +------------------------+------------------------+
        |                        |                        |
        v                        v                        v
+---------------+        +---------------+        +---------------+
|  1. PM Agent  | -----> | 2. Dev Agent  | -----> |  3. QA Agent  |
| Architecture  |        |  Source Code  |        | AST & Tests   |
+---------------+        +---------------+        +-------+-------+
                                 ^                        |
                                 |--- (Refinement Loop) --|
                                                          | (Pass)
                                                          v
                                                  +---------------+
                                                  | 4. Doc Agent  |
                                                  |  Docs & Guide |
                                                  +-------+-------+
                                                          |
                                                          v
                                                  +---------------+
                                                  | Download .ZIP |
                                                  +---------------+
```

---

## ⚡ Key Features
- **Real-Time Live Agent Stream**: Observe agents thinking, designing, coding, and testing with live progress indicators and terminal feeds.
- **Multi-File Code Explorer**: Browse generated files with syntax highlighting for Python, JavaScript, HTML, and CSS.
- **Automated QA & Test Execution**: Live test matrices displaying pass/fail assertions and quality scores.
- **1-Click ZIP Export**: Package and download the complete generated project archive instantly.
- **Flexible LLM Integration**: Supports **Google Gemini API**, **OpenAI API**, and includes a **Built-in Autonomous Engine** for instant offline demonstrations.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10 or higher
- Pip package manager

### 2. Installation
Clone or navigate to the project directory and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure API Key
Copy the sample environment file and configure your API key (if you wish to use live LLM models):
```bash
cp .env.example .env
```
Add your key inside `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If no API key is provided, the system automatically uses its high-fidelity Built-in Autonomous Engine).*

### 4. Run the Application
```bash
python run.py
```

### 5. Access the Web Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🧪 Running Automated Unit Tests
To verify all agents, pipeline stages, and endpoints:
```bash
python -m unittest tests/test_multi_agent_system.py
```

---

## 📁 Repository Structure
```
capstone-project/
├── backend/
│   ├── app.py                     # Flask server & REST/SSE endpoints
│   ├── config.py                  # Environment & model configurations
│   ├── orchestrator.py            # Multi-agent state manager & SSE pipeline
│   ├── agents/
│   │   ├── base_agent.py          # LLM base class & smart synthesis core
│   │   ├── pm_agent.py            # Project Manager agent logic
│   │   ├── dev_agent.py           # Developer agent code synthesis
│   │   ├── qa_agent.py            # Testing agent AST validation & test generator
│   │   └── doc_agent.py           # Documentation agent README generator
│   └── utils/
│       ├── exporter.py            # Project ZIP packager
│       └── validator.py           # Code syntax validator
├── frontend/
│   ├── templates/
│   │   └── index.html             # Main dashboard UI
│   └── static/
│       ├── css/
│       │   └── styles.css         # Modern dark glassmorphic stylesheet
│       └── js/
│           └── app.js             # Real-time SSE streaming & UI logic
├── tests/
│   └── test_multi_agent_system.py # Automated test suite
├── requirements.txt               # Dependencies
├── .env.example                   # Environment configuration template
├── run.py                         # Single-command launcher
└── README.md                      # Complete project documentation
```
