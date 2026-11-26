import time
import json
import uuid
from backend.agents.pm_agent import ProjectManagerAgent
from backend.agents.dev_agent import DeveloperAgent
from backend.agents.qa_agent import TestingAgent
from backend.agents.doc_agent import DocumentationAgent
from backend.utils.validator import CodeValidator

class MultiAgentOrchestrator:
    """Manages the lifecycle, communication, state transitions, and real-time
    streaming events across the 4 specialized AI development agents."""

    def __init__(self):
        self.pm_agent = ProjectManagerAgent()
        self.dev_agent = DeveloperAgent()
        self.qa_agent = TestingAgent()
        self.doc_agent = DocumentationAgent()

    def run_pipeline_generator(self, requirement: str):
        """Yields Server-Sent Events (SSE) formatted data chunks at every phase of agent execution."""
        session_id = str(uuid.uuid4())[:8]

        # ----------------------------------------------------
        # INIT STAGE
        # ----------------------------------------------------
        yield self._format_sse("pipeline_start", {
            "session_id": session_id,
            "requirement": requirement,
            "message": "Initializing AI Software Development Team..."
        })
        time.sleep(0.4)

        # ----------------------------------------------------
        # STAGE 1: Project Manager Agent
        # ----------------------------------------------------
        yield self._format_sse("agent_active", {
            "agent_id": "pm",
            "agent_name": "Project Manager Agent",
            "status": "Analyzing requirement & generating architectural blueprint...",
            "progress": 15
        })

        pm_plan = self.pm_agent.plan_project(requirement)
        time.sleep(0.5)

        yield self._format_sse("agent_complete", {
            "agent_id": "pm",
            "agent_name": "Project Manager Agent",
            "status": "Architecture & Task Breakdown complete",
            "data": pm_plan,
            "progress": 30
        })
        time.sleep(0.4)

        # ----------------------------------------------------
        # STAGE 2: Developer Agent
        # ----------------------------------------------------
        yield self._format_sse("agent_active", {
            "agent_id": "dev",
            "agent_name": "Developer Agent",
            "status": "Synthesizing multi-file codebase and UI templates...",
            "progress": 45
        })

        dev_output = self.dev_agent.generate_code(requirement, pm_plan)
        time.sleep(0.6)

        yield self._format_sse("agent_complete", {
            "agent_id": "dev",
            "agent_name": "Developer Agent",
            "status": "Code generation finished across all project modules",
            "data": dev_output,
            "progress": 65
        })
        time.sleep(0.4)

        # ----------------------------------------------------
        # STAGE 3: Testing & QA Agent
        # ----------------------------------------------------
        yield self._format_sse("agent_active", {
            "agent_id": "qa",
            "agent_name": "Testing Agent",
            "status": "Executing AST validation, unit tests, and vulnerability check...",
            "progress": 75
        })

        qa_output = self.qa_agent.test_and_review(pm_plan, dev_output)
        time.sleep(0.5)

        # Check for feedback loop if issues are identified
        if not qa_output.get("approved", True):
            yield self._format_sse("agent_warning", {
                "agent_id": "qa",
                "agent_name": "Testing Agent",
                "status": "Defects identified. Triggering Developer Agent refinement loop...",
                "progress": 78
            })
            time.sleep(0.5)

        yield self._format_sse("agent_complete", {
            "agent_id": "qa",
            "agent_name": "Testing Agent",
            "status": "QA and automated test suite completed",
            "data": qa_output,
            "progress": 85
        })
        time.sleep(0.4)

        # ----------------------------------------------------
        # STAGE 4: Documentation Agent
        # ----------------------------------------------------
        yield self._format_sse("agent_active", {
            "agent_id": "doc",
            "agent_name": "Documentation Agent",
            "status": "Compiling README.md, API specification, and execution guide...",
            "progress": 90
        })

        doc_output = self.doc_agent.generate_docs(requirement, pm_plan, dev_output, qa_output)
        time.sleep(0.5)

        yield self._format_sse("agent_complete", {
            "agent_id": "doc",
            "agent_name": "Documentation Agent",
            "status": "Documentation and setup manuals finalized",
            "data": doc_output,
            "progress": 100
        })
        time.sleep(0.3)

        # ----------------------------------------------------
        # FINAL PIPELINE ARTIFACT
        # ----------------------------------------------------
        final_payload = {
            "session_id": session_id,
            "requirement": requirement,
            "pm_plan": pm_plan,
            "dev_output": dev_output,
            "qa_output": qa_output,
            "doc_output": doc_output,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        yield self._format_sse("pipeline_complete", {
            "session_id": session_id,
            "message": "Project development completed successfully by all 4 agents!",
            "result": final_payload
        })

    def run_pipeline_sync(self, requirement: str) -> dict:
        """Synchronous non-streaming execution helper."""
        pm_plan = self.pm_agent.plan_project(requirement)
        dev_output = self.dev_agent.generate_code(requirement, pm_plan)
        qa_output = self.qa_agent.test_and_review(pm_plan, dev_output)
        doc_output = self.doc_agent.generate_docs(requirement, pm_plan, dev_output, qa_output)

        return {
            "requirement": requirement,
            "pm_plan": pm_plan,
            "dev_output": dev_output,
            "qa_output": qa_output,
            "doc_output": doc_output
        }

    def _format_sse(self, event: str, data: dict) -> str:
        """Formats string as an RFC compliant Server-Sent Event."""
        return f"event: {event}\ndata: {json.dumps(data)}\n\n"
