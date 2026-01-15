from pathlib import Path

def load_markdown_content(filename: str) -> str:
    """
    Reads the content of a markdown file into a string.
    Resolves paths relative to this file, not CWD.
    """
    base_dir = Path(__file__).resolve().parent
    prompt_path = base_dir / filename

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Prompt file not found: {prompt_path}") from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to load prompt file {prompt_path}: {e}"
        ) from e
