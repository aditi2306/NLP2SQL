from sqlalchemy import create_engine, inspect
from t5_wrapper import HuggingFaceT5
import urllib

# Set up the SQL Server connection
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-S9P3MUJN;"
    "DATABASE=Northwind;"
    "Trusted_Connection=yes"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Initialize your HuggingFace T5 model
llm = HuggingFaceT5()

def run_query(question, schema):
    # Format the prompt in the way your model expects
    prompt = f"Question: {question}\nSchema: {schema}"
    print("[Formatted Prompt]", prompt)

    # Generate SQL using your T5 model
    sql_query = llm(prompt)
    print("[Generated SQL]", sql_query)

    # Try to execute the SQL against the database
    try:
        with engine.connect() as conn:
            result = conn.execute(sql_query)
            rows = result.fetchall()
            columns = result.keys()
            return sql_query, rows, columns
    except Exception as e:
        print("[Execution Error]", str(e))
        return sql_query, [], [f"Execution failed: {e}"]

def get_schema_for_tables(table_names):
    inspector = inspect(engine)
    schema_strings = []

    for table in table_names:
        columns = inspector.get_columns(table)
        col_defs = [f'"{col["name"]}" {col["type"]}' for col in columns]

        # Safely get primary keys
        pk_constraint = inspector.get_pk_constraint(table)
        primary_keys = pk_constraint.get("constrained_columns", [])

        if primary_keys:
            pk_joined = ", ".join(f'"{pk}"' for pk in primary_keys)
            pk_str = f", primary key: {pk_joined}"
        else:
            pk_str = ""

        table_schema = f'"{table}" ' + ", ".join(col_defs) + pk_str + " [SEP]"
        schema_strings.append(table_schema)

    return "\n".join(schema_strings)
