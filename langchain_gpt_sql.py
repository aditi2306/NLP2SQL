from sqlalchemy import create_engine, inspect
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_toolkits.sql.base import create_sql_agent
import urllib
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)

# SQL Server connection string
uid = os.getenv("AZURE_SQL_UID")
pwd = os.getenv("AZURE_SQL_PWD")
server = os.getenv("AZURE_SQL_SERVER")
database = os.getenv("AZURE_SQL_DB")

# Create the connection string
params = urllib.parse.quote_plus(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{server},1433;"
    f"Database={database};"
    f"Uid={uid};"
    f"Pwd={pwd};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Connect LangChain SQL wrapper
db = SQLDatabase(engine)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create agent with intermediate steps support
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_executor_kwargs={"return_intermediate_steps": True}
)

# --------------------
# MAIN QUERY FUNCTION
# --------------------
def run_query(question, schema=None):
    print("[Running Agent for Question]:", question)

    try:
        output = agent_executor.invoke({"input": question})

        # Print full agent output
        print("\n[Agent Output]:")
        print(output)

        answer = output.get("output", "")
        steps = output.get("intermediate_steps", [])

        # Show steps (LLM reasoning)
        print("\n[Intermediate Steps]:")
        for idx, step in enumerate(steps):
            print(f"Step {idx+1}:")
            print("  Tool:", step[0].tool)
            print("  Input:", step[0].tool_input)
            print("  Output:", step[1])

        # Try to extract SQL
        sql_query = None
        for action, _ in steps:
            if hasattr(action, "tool") and action.tool == "sql_db_query":
                sql_query = action.tool_input
                break

        if not sql_query:
            print("[ Warning] SQL query not found in intermediate steps.")
            return answer, [], []

        print("\n[Extracted SQL Query]:", sql_query)
        

        with engine.connect() as conn:
            result = conn.execute(text(sql_query))  # Wrap the string with `text()`
            rows = result.fetchall()
            columns = result.keys()

            return sql_query, rows, columns



    except Exception as e:
        print("[ SQL Execution Error]", e)
        return None, [], [f"Execution failed: {e}"]

# --------------------
# SCHEMA HELPER FUNCTION
# --------------------
def get_schema_for_tables(table_names):
    inspector = inspect(engine)
    schema_strings = []

    for table in table_names:
        columns = inspector.get_columns(table)
        col_defs = [f'"{col["name"]}" {col["type"]}' for col in columns]

        # Primary key info
        pk_constraint = inspector.get_pk_constraint(table)
        primary_keys = pk_constraint.get("constrained_columns", [])
        pk_str = f", primary key: {', '.join(f'\"{pk}\"' for pk in primary_keys)}" if primary_keys else ""

        table_schema = f'"{table}" ' + ", ".join(col_defs) + pk_str + " [SEP]"
        schema_strings.append(table_schema)

    return "\n".join(schema_strings)
