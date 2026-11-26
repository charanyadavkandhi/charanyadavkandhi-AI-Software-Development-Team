import os
import io
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, Response, send_file
from flask_cors import CORS

from backend.config import Config
from backend.orchestrator import MultiAgentOrchestrator
from backend.utils.exporter import ProjectExporter

# Setup directories
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / 'frontend' / 'templates'
STATIC_DIR = BASE_DIR / 'frontend' / 'static'

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path='/static'
)
CORS(app)

orchestrator = MultiAgentOrchestrator()

@app.route('/')
def index():
    """Render the Main Multi-Agent Workspace UI."""
    return render_template('index.html')

@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Returns sample project prompts for quick testing and demos."""
    return jsonify({
        "success": True,
        "presets": Config.PRESETS
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Returns status of AI API integration."""
    has_gemini = bool(Config.GEMINI_API_KEY)
    has_openai = bool(Config.OPENAI_API_KEY)
    
    mode = "Gemini API" if has_gemini else ("OpenAI API" if has_openai else "Built-in Autonomous Engine")
    return jsonify({
        "success": True,
        "has_gemini": has_gemini,
        "has_openai": has_openai,
        "active_engine": mode,
        "model_name": Config.GEMINI_MODEL if has_gemini else (Config.OPENAI_MODEL if has_openai else "Smart Agent Synthesis Core")
    })

@app.route('/api/config/update', methods=['POST'])
def update_config():
    """Allows updating API keys dynamically from the web UI."""
    data = request.json or {}
    gemini_key = data.get('gemini_api_key', '').strip()
    openai_key = data.get('openai_api_key', '').strip()
    
    if gemini_key:
        Config.GEMINI_API_KEY = gemini_key
    if openai_key:
        Config.OPENAI_API_KEY = openai_key
        
    return jsonify({"success": True, "message": "API credentials updated successfully."})

@app.route('/api/stream')
def stream_agents():
    """Server-Sent Events endpoint for real-time live streaming of multi-agent execution."""
    requirement = request.args.get('prompt', '').strip()
    if not requirement:
        return jsonify({"error": "Prompt parameter is required"}), 400

    def event_stream():
        for event_chunk in orchestrator.run_pipeline_generator(requirement):
            yield event_chunk

    return Response(event_stream(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
        'Connection': 'keep-alive'
    })

@app.route('/api/generate', methods=['POST'])
def generate_project():
    """Synchronous execution endpoint."""
    data = request.json or {}
    requirement = data.get('prompt', '').strip()
    if not requirement:
        return jsonify({"success": False, "error": "Prompt is required"}), 400

    result = orchestrator.run_pipeline_sync(requirement)
    return jsonify({"success": True, "result": result})

@app.route('/api/export', methods=['POST'])
def export_project():
    """Generates and streams a downloadable .zip archive of the multi-agent artifacts."""
    data = request.json or {}
    project_name = data.get('project_name', 'AI_Generated_Project')
    files = data.get('files', {})
    test_code = data.get('test_file_content', '')
    readme_md = data.get('readme_markdown', '')

    if not files:
        return jsonify({"success": False, "error": "No files provided for export"}), 400

    zip_buffer = ProjectExporter.create_zip_archive(
        project_name=project_name,
        files=files,
        test_file_content=test_code,
        readme_markdown=readme_md
    )

    filename = f"{project_name.lower().replace(' ', '_')}.zip"
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    print(f"Starting Multi-Agent Capstone Server on port {Config.PORT}...")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
