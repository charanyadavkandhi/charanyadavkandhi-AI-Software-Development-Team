import json
from backend.agents.base_agent import BaseAgent

class ProjectManagerAgent(BaseAgent):
    """Agent 1: Project Manager Agent responsible for understanding requirements,
    architectural design, file breakdown, and execution planning."""

    def __init__(self):
        system_prompt = (
            "You are an Elite Technical Project Manager & Software Architect. "
            "Your task is to analyze user software requirements and design a complete, production-ready system specification. "
            "You decide the project name, architecture, tech stack, directory structure, and granular implementation tasks. "
            "Always return a clean JSON object."
        )
        super().__init__(name="Project Manager Agent", role="Architecture & Planning", system_prompt=system_prompt)

    def plan_project(self, requirement: str) -> dict:
        prompt = (
            f"User Requirement:\n{requirement}\n\n"
            "Generate a comprehensive software development plan including:\n"
            "1. project_name: A clean slug and title\n"
            "2. summary: High-level overview of the solution\n"
            "3. architecture: Architecture pattern (e.g. Modular MVC, RESTful API + SPA)\n"
            "4. tech_stack: List of technologies (Languages, Frameworks, Libraries, Storage)\n"
            "5. file_structure: Array of file paths to be created (e.g. ['app.py', 'templates/index.html', 'static/css/styles.css', 'static/js/main.js', 'requirements.txt'])\n"
            "6. tasks: Ordered list of tasks for the Developer and QA Agents\n"
            "7. acceptance_criteria: Key deliverables to verify success\n"
        )
        
        schema_hint = """{
  "project_name": "Project Title",
  "slug": "project_slug",
  "summary": "Detailed summary...",
  "architecture": "Architecture details...",
  "tech_stack": ["Python", "Flask", "HTML5", "CSS3", "JavaScript", "SQLite"],
  "file_structure": ["app.py", "models.py", "templates/index.html", "static/css/styles.css", "static/js/main.js", "requirements.txt"],
  "tasks": [
    {"id": "TASK-1", "title": "Setup Backend & API Endpoints", "agent": "Developer Agent", "description": "Build REST routes..."},
    {"id": "TASK-2", "title": "Frontend Interface & Interactions", "agent": "Developer Agent", "description": "Create responsive modern UI..."},
    {"id": "TASK-3", "title": "Automated Unit Tests & QA", "agent": "Testing Agent", "description": "Test data flow, routes, and edge cases..."},
    {"id": "TASK-4", "title": "Documentation & Deployment Guide", "agent": "Documentation Agent", "description": "Create complete setup guide..."}
  ],
  "acceptance_criteria": ["Clean modular code", "Zero syntax errors", "Responsive UI", "Passing test suite"]
}"""
        response_text = self.call_llm(prompt, schema_hint)
        plan_data = self.extract_json(response_text)
        
        # If response was not valid JSON, use intelligent structured fallback
        if "project_name" not in plan_data:
            plan_data = self.get_smart_plan(requirement)
            
        return plan_data

    def smart_fallback(self, user_prompt: str) -> str:
        return json.dumps(self.get_smart_plan(user_prompt))

    def get_smart_plan(self, requirement: str) -> dict:
        """Intelligent fallback generator when running offline without an API key."""
        req_lower = requirement.lower()
        
        if "weather" in req_lower:
            name = "Weather Analytics Studio"
            slug = "weather_analytics_studio"
            summary = "An interactive weather intelligence dashboard featuring real-time city forecasting, 7-day analytics, temperature trend charts, and cached API responses."
            files = ["app.py", "weather_service.py", "templates/index.html", "static/css/styles.css", "static/js/main.js", "requirements.txt"]
        elif "url" in req_lower or "shorten" in req_lower:
            name = "Quantum URL Shortener & Analytics"
            slug = "quantum_url_shortener"
            summary = "A lightning-fast URL shortening and analytics platform with QR code generator, click tracking, custom aliases, and REST endpoints."
            files = ["app.py", "database.py", "templates/index.html", "static/css/styles.css", "static/js/main.js", "requirements.txt"]
        elif "note" in req_lower or "markdown" in req_lower:
            name = "Aether Markdown Notes & Knowledge Base"
            slug = "aether_notes"
            summary = "A distraction-free real-time Markdown notes platform with split-screen preview, tag indexing, dark glass UI, and local storage sync."
            files = ["app.py", "storage.py", "templates/index.html", "static/css/styles.css", "static/js/main.js", "requirements.txt"]
        else:
            name = "Nexus Task & Project Hub"
            slug = "nexus_task_hub"
            summary = f"A modern full-stack web application designed for: {requirement.strip()} with structured REST endpoints, clean database models, and an ultra-modern glassmorphic UI."
            files = ["app.py", "models.py", "templates/index.html", "static/css/styles.css", "static/js/main.js", "requirements.txt"]

        return {
            "project_name": name,
            "slug": slug,
            "summary": summary,
            "architecture": "Modular MVC Architecture (Python Flask REST Backend + Modern SPA Frontend with Reactive DOM State)",
            "tech_stack": ["Python 3.10+", "Flask", "SQLite3", "HTML5 & Semantic Markup", "Vanilla CSS3 Glassmorphism", "ES6+ JavaScript"],
            "file_structure": files,
            "tasks": [
                {"id": "TASK-01", "title": "Project Scaffold & Data Model", "agent": "Developer Agent", "description": "Initialize database schemas, configurations, and core dependencies."},
                {"id": "TASK-02", "title": "REST API & Backend Controllers", "agent": "Developer Agent", "description": "Implement CRUD endpoints, input sanitization, and error handling."},
                {"id": "TASK-03", "title": "Interactive Modern User Interface", "agent": "Developer Agent", "description": "Construct dark-mode glassmorphic interface with animations and dynamic interactions."},
                {"id": "TASK-04", "title": "Automated Unit Testing & Linting", "agent": "Testing Agent", "description": "Verify API responses, test database consistency, and benchmark response speed."},
                {"id": "TASK-05", "title": "Technical Documentation & Setup Guide", "agent": "Documentation Agent", "description": "Compile comprehensive README, API specification, and architecture walkthrough."}
            ],
            "acceptance_criteria": [
                "100% runnable multi-file codebase without missing imports",
                "Responsive modern UI with zero external bulky dependencies",
                "Automated test coverage passing with >= 90% score",
                "Complete setup and execution guide included in README.md"
            ]
        }
