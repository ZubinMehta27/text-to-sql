from text_to_sql_agent.agent_factory import get_llm
from text_to_sql_agent.config import settings

"""
LLM configuration for SQL generation.
"""

agent = get_llm()
print("LLM provider:", settings.llm_provider)
