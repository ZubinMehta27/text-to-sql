from langchain.tools import tool


@tool
def request_user_clarification(context: str) -> str:
    """
    Ask the user a precise clarification question
    when the system cannot proceed deterministically.

    Must:
    - Ask ONE clear question
    - Be concise
    - Avoid technical jargon
    """

    return (
        "You are an analytical assistant helping a user clarify their question.\n\n"
        "The system cannot proceed because the request is ambiguous.\n\n"
        "Ask ONE short, clear clarification question that would allow the system "
        "to continue safely.\n\n"
        f"Context:\n{context}"
    )
