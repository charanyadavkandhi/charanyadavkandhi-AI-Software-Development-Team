"""
Unit & Integration Tests for AI Software Development Team System
"""
import unittest
import json
import io
import zipfile
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app
from backend.agents.pm_agent import ProjectManagerAgent
from backend.agents.dev_agent import DeveloperAgent
from backend.agents.qa_agent import TestingAgent
from backend.agents.doc_agent import DocumentationAgent
from backend.utils.exporter import ProjectExporter
from backend.utils.validator import CodeValidator

class TestMultiAgentSystem(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_01_pm_agent_plan(self):
        pm = ProjectManagerAgent()
        plan = pm.plan_project("Build a modern Task Tracker with Flask")
        self.assertIn("project_name", plan)
        self.assertIn("file_structure", plan)
        self.assertTrue(len(plan["file_structure"]) > 0)
        self.assertIn("tasks", plan)

    def test_02_dev_agent_generation(self):
        pm = ProjectManagerAgent()
        dev = DeveloperAgent()
        plan = pm.plan_project("Build a weather dashboard")
        output = dev.generate_code("Build a weather dashboard", plan)
        self.assertIn("files", output)
        self.assertTrue(len(output["files"]) > 0)
        self.assertIn("app.py", output["files"])

    def test_03_qa_agent_review(self):
        pm = ProjectManagerAgent()
        dev = DeveloperAgent()
        qa = TestingAgent()
        plan = pm.plan_project("Task tracker")
        dev_out = dev.generate_code("Task tracker", plan)
        qa_out = qa.test_and_review(plan, dev_out)
        self.assertIn("quality_score", qa_out)
        self.assertIn("test_cases", qa_out)
        self.assertGreaterEqual(qa_out["quality_score"], 70)

    def test_04_doc_agent(self):
        pm = ProjectManagerAgent()
        dev = DeveloperAgent()
        qa = TestingAgent()
        doc = DocumentationAgent()
        plan = pm.plan_project("Task tracker")
        dev_out = dev.generate_code("Task tracker", plan)
        qa_out = qa.test_and_review(plan, dev_out)
        doc_out = doc.generate_docs("Task tracker", plan, dev_out, qa_out)
        self.assertIn("readme_markdown", doc_out)
        self.assertTrue(len(doc_out["readme_markdown"]) > 100)

    def test_05_zip_exporter(self):
        files = {"app.py": "print('hello')", "README.md": "# Readme"}
        zip_buf = ProjectExporter.create_zip_archive("Test Project", files, "import unittest", "# Docs")
        self.assertIsInstance(zip_buf, io.BytesIO)
        
        # Verify valid zip
        with zipfile.ZipFile(zip_buf, 'r') as z:
            names = z.namelist()
            self.assertTrue(any("app.py" in n for n in names))
            self.assertTrue(any("README.md" in n for n in names))

    def test_06_flask_api_endpoints(self):
        # 1. Presets endpoint
        res = self.client.get('/api/presets')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(len(data['presets']) > 0)

        # 2. Config endpoint
        res = self.client.get('/api/config')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

        # 3. Export endpoint
        export_payload = {
            "project_name": "Sample App",
            "files": {"app.py": "print('hello')"},
            "test_file_content": "import unittest",
            "readme_markdown": "# Sample"
        }
        res = self.client.post('/api/export', json=export_payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'application/zip')

if __name__ == '__main__':
    unittest.main()
