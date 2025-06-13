import os
import logging

from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.llms.llm import get_llm_by_type

env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


class State(MessagesState):
    """
    Represents the mutable state of the video graph.
    """
    locale: str
    paragraphs_nums: int


def script_node(state: State) -> State:
    """
    generate script node 
    """""
    logging.info(f"script_node messages: {state.get('messages')}")
    try:
        template = env.get_template("script.md")
    except Exception as e:
        raise ValueError(f"Error loading script template: {e}")

    system_prompt = template.render(**state)
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    llm = get_llm_by_type()
    response = llm.invoke(messages)
    return state


def build_graph():
    """Build and return the agent workflow graph without memory."""
    # build state graph
    builder = StateGraph(State)
    builder.add_node("script", script_node)
    builder.add_edge(START, "script")
    builder.add_edge("script", END)
    return builder.compile()


def build_graph_with_memory():
    """Build and return the agent workflow graph with memory."""
    # use persistent memory to save conversation history
    memory = MemorySaver()

    builder = StateGraph(State)
    builder.add_node("script", script_node)
    builder.add_edge(START, "script")
    builder.add_edge("script", END)

    return builder.compile(checkpointer=memory)


graph = build_graph()

if __name__ == "__main__":
    graph.invoke({
        "messages": [{
            "role": "user",
            "content": "海绵宝宝和派大星",
        }]
    })
