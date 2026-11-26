import io
import zipfile

class ProjectExporter:
    """Packages all generated files, test suites, and documentation into a ZIP buffer."""

    @staticmethod
    def create_zip_archive(project_name: str, files: dict, test_file_content: str = "", readme_markdown: str = "") -> io.BytesIO:
        buffer = io.BytesIO()
        folder_prefix = project_name.lower().replace(" ", "_").replace("-", "_")
        
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as z:
            # 1. Add all generated source code files
            added_files = set()
            for filepath, content in files.items():
                archive_path = f"{folder_prefix}/{filepath}"
                z.writestr(archive_path, content)
                added_files.add(filepath.lower())
            
            # 2. Add test suite file if present
            if test_file_content and "tests/test_app.py" not in added_files:
                z.writestr(f"{folder_prefix}/tests/test_app.py", test_file_content)
                
            # 3. Add README.md if not already written
            if readme_markdown and "readme.md" not in added_files:
                z.writestr(f"{folder_prefix}/README.md", readme_markdown)
                
        buffer.seek(0)
        return buffer
