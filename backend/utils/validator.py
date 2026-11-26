import ast

class CodeValidator:
    """Validates source code syntax and structural integrity."""

    @staticmethod
    def validate_python(code_str: str) -> dict:
        try:
            ast.parse(code_str)
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"SyntaxError at line {e.lineno}: {e.msg}",
                "lineno": e.lineno
            }
        except Exception as e:
            return {"valid": False, "error": str(e), "lineno": 1}

    @staticmethod
    def validate_files(files_dict: dict) -> dict:
        results = {}
        all_valid = True
        for filepath, content in files_dict.items():
            if filepath.endswith('.py'):
                res = CodeValidator.validate_python(content)
                results[filepath] = res
                if not res["valid"]:
                    all_valid = False
            else:
                results[filepath] = {"valid": True, "error": None}
        return {"all_valid": all_valid, "file_results": results}
