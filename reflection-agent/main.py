from typing import List, Sequence
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import END, MessageGraph

from chains import generate_chain, refelection_chain

from dotenv import load_dotenv
load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"

def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})

def reflection_node(messages: Sequence[BaseMessage]) -> List [BaseMessage]:
    res = refelection_chain.invoke({"messages": messages})
    return HumanMessage(content=res.content)

builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
#graph.get_graph().draw_mermaid_png(output_file_path="flow.png")
print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

if __name__ == "__main__":
    print("LangGraph Reflection Agent")
    inputs = HumanMessage(content="""Make this tweet better:"
                                @LangChainAI
        — newly Tool Calling feature is seriously underrated.

        After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.

        Made a video covering their newest blog post

                                """)
    response = graph.invoke(inputs)