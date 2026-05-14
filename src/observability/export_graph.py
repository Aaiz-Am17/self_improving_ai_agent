from src.agent.graph import graph

graph_image = graph.get_graph().draw_mermaid_png()

with open("workflow_graph.png", "wb") as f:

    f.write(graph_image)

print("Workflow graph exported successfully.")