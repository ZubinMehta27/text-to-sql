def load_markdown_content(filename):
    """Reads the content of a markdown file into a string."""
    try:
        # Use 'utf-8' encoding for compatibility across different platforms
        with open(filename, 'r', encoding='utf-8') as f:
            markdown_string = f.read()
        return markdown_string
    except FileNotFoundError:
        return f"Error: The file {filename} was not found."
    except Exception as e:
        return f"An error occurred: {e}"