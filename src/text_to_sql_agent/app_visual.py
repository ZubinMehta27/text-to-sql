from text_to_sql_agent.graph_build import compiled_graph

from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

display(Image(compiled_graph.get_graph().draw_mermaid_png()))