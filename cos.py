from dotenv import load_dotenv
import os
from agent_resources.query_templates import PREDEFINED_QUERIES
from agent_resources.schema import DATABASE_SCHEMA
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
load_dotenv()

def create_execute_query_tool():
    description = f"""
    Execute a SQL query on  database.
    
    DATABASE SCHEMA:
    {DATABASE_SCHEMA}

    QUERY TEMPLATES:
    {PREDEFINED_QUERIES}
    
    Args:
        query: The SQL SELECT query to execute
    
    Returns:
        Query results
    """
    @tool("execute_query", return_direct=True, description=description)
    def execute_query(query: str) -> str:
        print(f"Executing query: {query}")
        return "Mock query result"
    return execute_query

system_prompt = """
You are a production data assistant.

To answer any question about production data, you MUST use the execute_query tool.
Generate the correct SQL query and call the tool.
"""

tools = [create_execute_query_tool()]

model = ChatOpenAI(model="gpt-4.1", temperature=0)
agent = create_agent(model=model, tools=tools, system_prompt=system_prompt)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Show me production KPI from all machines from the last 30 days."}]}
)

print(result["messages"][-1].content)
