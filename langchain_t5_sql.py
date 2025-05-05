from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from t5_wrapper import HuggingFaceT5  
import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-S9P3MUJN;DATABASE=Northwind;Trusted_Connection=yes"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

db = SQLDatabase(engine)
llm = HuggingFaceT5()
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    handle_parsing_errors=True
)

def run_query(nl_question):
    print("Prompt:", nl_question)
    result = agent_executor.run(nl_question)
    print("Result:", result)
    return result
