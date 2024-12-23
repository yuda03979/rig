import re
import json
import ast


def get_dict(input_string):
    import ast
    # Try ast.literal_eval first (safe for Python dict-like strings)
    try:
        out = ast.literal_eval(input_string)
        if isinstance(out, dict):
            return out, True
    except (ValueError, SyntaxError):
        pass

    # Fallback to JSON parsing (for JSON formatted strings)
    try:
        out = json.loads(input_string)
        if isinstance(out, dict):
            return out, True
    except (json.JSONDecodeError, TypeError):
        pass

    # Use regex to find content between { and } that looks like a valid JSON
    input_string = re.sub(r"[\t\n]", "", input_string)
    match = re.search(r'\{[^}]*\}', input_string)

    if not match:
        return input_string, False

    json_str = match.group(0)

    try:
        # First, try standard JSON parsing
        parsed_dict = json.loads(json_str)
        return parsed_dict, True
    except json.JSONDecodeError:
        # If standard parsing fails, try some custom parsing
        try:
            json_str = re.sub(r"(None|null|'None'|\"None\"|'null'|\"null\")", '"null"', json_str)
            # Use ast for more flexible parsing
            import ast
            parsed_dict = ast.literal_eval(json_str)
            return parsed_dict, True
        except (SyntaxError, ValueError):
            return input_string, False
