# 🤖 AI Software Development Team – Multi-Agent System

**Capstone Project | School of Computer Science & Artificial Intelligence**  
**SR University | VII Semester | Project Team No. 189**

An AI-powered multi-agent system designed to assist and automate different stages of software development, including project planning, code generation, syntax validation, and documentation.

---

## 👥 Project Team Members

| Roll Number | Team Member | Responsibility |
|---|---|---|
| 2303A52367 | K. Charan Yadav | Team Lead & Multi-Agent Architecture |
| 2303A51330 | K. Akshitha | Agent Orchestration & Backend Engine |
| 2303A51320 | A. Shiva Spandana | QA Agent & Testing |
| 2303A51321 | CH. Manmith Vardhan | Frontend UI & Interactive Visualizer |

---

## 📖 Abstract

Traditional software development involves several stages, such as understanding requirements, designing architecture, selecting technologies, writing code, testing, and preparing documentation. Performing all these tasks manually can be time-consuming and complex.

The **AI Software Development Team – Multi-Agent System** addresses this challenge through a collaborative system of specialized AI agents. Each agent is responsible for a particular stage of the software development process.

The system consists of four specialized agents coordinated by an Orchestrator Engine. Users provide project requirements through a web dashboard, and the agents work together to generate a project plan, source code, quality feedback, and documentation.

The main objective is to demonstrate how multiple AI agents can collaborate to simplify and streamline software development.

---

## 🎯 Project Objectives

- Automate important stages of the software development workflow.
- Use specialized AI agents for different development responsibilities.
- Generate multi-file source code based on user requirements.
- Perform Python syntax validation using AST analysis.
- Generate testing-related outputs and quality feedback.
- Automatically prepare project documentation.
- Provide an interactive dashboard to monitor the agent workflow.

---

## 🏗️ System Architecture

The system uses four specialized agents coordinated by an Orchestrator Engine.

### 1. Project Manager Agent
- Understands the user's project requirements.
- Creates a project plan and architecture.
- Identifies suitable technologies.
- Divides the project into development tasks.

### 2. Developer Agent
- Uses the project plan to generate source code.
- Creates multiple project files.
- Generates backend and frontend components based on the requirements.

### 3. Testing and QA Agent
- Performs Python syntax validation using Abstract Syntax Tree (AST) analysis.
- Generates testing-related outputs.
- Provides quality feedback and validation reports.

### 4. Documentation Agent
- Generates project documentation.
- Prepares README content and setup instructions.
- Organizes relevant project information.

### Orchestrator Engine

The Orchestrator Engine coordinates the agents and manages the execution workflow. It connects the user request with the different agents and communicates progress to the frontend.

### Workflow

```text
        User Requirements
                |
                v
        Web Dashboard
                |
                v
       Orchestrator Engine
                |
                v
      Project Manager Agent
                |
                v
         Developer Agent
                |
                v
        Testing & QA Agent
                |
                v
       Documentation Agent
                |
                v
       Generated Project
                |
                v
          ZIP Export
```

---

## ⚡ Key Features

- **Multi-Agent Collaboration:** Four specialized AI agents work together across different development stages.
- **Project Planning:** Converts user requirements into a structured project plan.
- **Multi-File Code Generation:** Generates source-code files based on the project requirements.
- **Python Syntax Validation:** Uses AST-based analysis to identify Python syntax issues.
- **Testing Support:** Generates testing-related outputs and quality feedback.
- **Automatic Documentation:** Creates project documentation and setup instructions.
- **Interactive Web Dashboard:** Provides a user interface to submit requirements and monitor progress.
- **Real-Time Progress Updates:** Uses Server-Sent Events (SSE) to stream workflow updates.
- **ZIP Export:** Packages generated project files for download.
- **AI Model Integration:** Supports the configured Gemini and OpenAI API integrations.
- **Demo/Fallback Mode:** Provides a fallback engine for demonstrations when live API credentials are unavailable.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| AI Integration | Google Gemini API, OpenAI API |
| Code Validation | Python AST |
| Communication | Server-Sent Events (SSE) |
| Project Export | ZIP |
| Development Tools | Visual Studio Code, Git, GitHub |

---

## 📁 Project Structure

```text
AI-Software-Development-Team/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── orchestrator.py
│   │
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── pm_agent.py
│   │   ├── dev_agent.py
│   │   ├── qa_agent.py
│   │   └── doc_agent.py
│   │
│   └── utils/
│       ├── exporter.py
│       └── validator.py
│
├── frontend/
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── styles.css
│       └── js/
│           └── app.js
│
├── tests/
│   └── test_multi_agent_system.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
├── README.md
├── Capstone project.pdf
└── AI_Software_Dev_Team_Multi_Agent.pptx
```

---

## 🚀 Installation and Execution

### Prerequisites

Make sure the following are installed:

- Python 3.10 or higher
- pip package manager
- Visual Studio Code (recommended)
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/charanyadavkandhi/charanyadavkandhi-AI-Software-Development-Team.git
```

### Step 2: Open the Project Folder

```bash
cd charanyadavkandhi-AI-Software-Development-Team
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

If you want to use live AI API services, create a `.env` file using `.env.example` as a template.

**Windows:**

```cmd
copy .env.example .env
```

Open `.env` and add the required API credentials using the variable names specified in `.env.example`.

**Important:** Never upload your actual `.env` file or API keys to GitHub.

The fallback/demo mode can be used when API credentials are unavailable, subject to the project's configured fallback behavior.

### Step 7: Run the Application

```bash
python run.py
```

### Step 8: Open the Web Dashboard

Open your browser and visit:

```text
http://localhost:5000
```

---

## 🧪 Testing

The project includes a test suite for checking the implemented system components.

To discover and run the available unit tests, execute:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Review the test output to identify passed and failed tests.

**Note:** The QA agent's AST-based syntax validation is different from full runtime testing. Successful syntax validation does not guarantee that generated applications will execute correctly.

---

## 📸 Project Screenshots

Screenshots of the actual application can be added here to demonstrate its interface and functionality.

Suggested screenshots:

1. Main application dashboard.
2. Project requirement input screen.
3. Project planning output.
4. Developer agent code-generation output.
5. QA validation and quality report.
6. Documentation generation output.
7. Generated project files and ZIP export.

<!-- Add your actual screenshots here after uploading them to the repository. -->

---

## 🎥 Project Demonstration Video

A demonstration video will showcase the complete project workflow, including requirement submission, agent coordination, code generation, QA validation, documentation, and project export.

**Demo Video:** Add your published project video link here.

---

## 📝 Project Blog

Read our project blog to learn more about the motivation, architecture, implementation, workflow, challenges, and future scope.

**Blog:** Add your published blog URL here.

---

## ⚠️ Limitations

- AST-based validation checks Python syntax but does not guarantee runtime correctness.
- Generated code may require manual review, debugging, or modifications.
- Output quality depends on the clarity of user requirements and the responses from configured AI services.
- The fallback/demo engine may not provide the same behavior as live AI model integrations.
- Automatic iterative code repair is not currently implemented.

---

## 🔮 Future Enhancements

- Implement sandbox-based execution of generated applications.
- Introduce advanced automated testing and runtime validation.
- Develop an iterative feedback and automatic code-repair mechanism.
- Extend support to additional programming languages.
- Improve communication and feedback between specialized agents.
- Enhance generated code quality and error-handling capabilities.

---

## 🎓 Conclusion

The AI Software Development Team – Multi-Agent System demonstrates how specialized AI agents can collaborate to assist different stages of software development.

By combining project planning, multi-file code generation, syntax validation, and documentation generation in a coordinated workflow, the system provides an approach to simplifying software development tasks.

This project also provides practical experience in multi-agent architecture, AI integration, backend development, frontend development, and software testing.

---

## 👨‍💻 Repository

**GitHub:** https://github.com/charanyadavkandhi/charanyadavkandhi-AI-Software-Development-Team

**Developed as a Capstone Project at SR University.**
