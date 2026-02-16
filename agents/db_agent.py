# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from tools.db_manager import DBManager

# from langgraph.graph import StateGraph
# from langgraph.prebuilt import ToolNode
# from langgraph.store.memory import InMemoryStore
# from langgraph.graph import StateGraph, END
# from uuid import uuid4

# from typing import TypedDict

# tools = [
#     DBManager.health_check,
#     DBManager.create_reminder,
#     DBManager.fetch_upcoming,
#     DBManager.mark_done
# ]

# llm = ChatOpenAI(
#     model="gpt-4.1-mini",
#     temperature=0
# ).bind_tools(tools)

# class DBSessionMemory(TypedDict):
#     response: dict
#     router_message: str

# def llm_node(state: DBSessionMemory):
#     response = llm.invoke(state["messages"])
#     return {"messages": [response]}


# def DatabaseAgent():

#     builder = StateGraph(DBSessionMemory)

#     builder.add_node("llm", llm_node)
#     builder.add_node("tools", ToolNode(tools))

#     builder.set_entry_point("llm")

#     builder.add_conditional_edges(
#         "llm",
#         lambda x: "tools" if x["messages"][-1].tool_calls else END
#     )

#     builder.add_edge("tools", "llm")

#     graph = builder.compile()

#     return graph


# # tools = [
# #     DBManager.health_check,
# #     DBManager.create_reminder,
# #     DBManager.fetch_upcoming,
# #     DBManager.mark_done
# # ]

# # llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, verbose=True)

# # agent = llm.bind_tools(tools=tools)


from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from tools.db_manager import DBManager


# ---------------------------
# Agent State
# ---------------------------
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], "conversation"]


# ---------------------------
# Tools
# ---------------------------
tools = [
    DBManager.health_check,
    DBManager.create_reminder,
    DBManager.fetch_upcoming,
    DBManager.mark_done
]


# ---------------------------
# LLM
# ---------------------------
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
).bind_tools(tools)


# ---------------------------
# LLM Node
# ---------------------------
def llm_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# ---------------------------
# Build Graph
# ---------------------------
def DatabaseAgent():

    builder = StateGraph(AgentState)

    builder.add_node("llm", llm_node)
    builder.add_node("tools", ToolNode(tools))

    builder.set_entry_point("llm")

    builder.add_conditional_edges(
        "llm",
        lambda x: x["messages"][-1].tool_calls[0]["name"] if x["messages"][-1].tool_calls else END
    )

    builder.add_edge("tools", "llm")

    graph = builder.compile()

    return graph
