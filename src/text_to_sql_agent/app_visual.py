from text_to_sql_agent.graph_build import build_graph
from text_to_sql_agent.agent import agent

compiled_graph = build_graph(agent)

from IPython.display import Image, display
display(Image(compiled_graph.get_graph().draw_mermaid_png()))
