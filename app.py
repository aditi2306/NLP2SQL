import streamlit as st
from langchain_t5_sql import run_query, get_schema_for_tables
import asyncio
import os

# Environment settings
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# UI Title
st.title("Natural Language to SQL")

# Input: NL question
question = st.text_input("Enter your natural language question:")

# Table selection
st.subheader(" Select Tables to Include in Schema")
available_tables = ["Products", "Employees", "Orders", "Customers","Categories","Region","Shippers","Suppliers","Territories","CustomerCustomerDemo","CustomerDemographics","EmployeeTerritories","Order Details"]  # Or fetch dynamically
selected_tables = st.multiselect("Select one or more tables:", available_tables)

# Preview schema
if selected_tables:
    schema_preview = get_schema_for_tables(selected_tables)
    st.markdown("###  Preview Schema")
    st.code(schema_preview, language="sql")

# Async-safe query execution wrapper
def safe_run_query(q, schema):
    try:
        return run_query(q, schema)
    except RuntimeError as e:
        if "no running event loop" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(run_query(q, schema))
        else:
            raise

# Run button
if st.button(" Run Query"):
    if not question or not selected_tables:
        st.warning("⚠️ Please enter a question and select at least one table.")
    else:
        with st.spinner(" Running query..."):
            try:
                schema = get_schema_for_tables(selected_tables)
                sql_query, rows, columns = safe_run_query(question, schema)

                st.success(" SQL generated and executed successfully!")
                
                # Show SQL
                st.subheader(" Generated SQL")
                st.code(sql_query, language="sql")

                # Show result
                if rows:
                    st.subheader(" Query Result")
                    st.dataframe([dict(zip(columns, row)) for row in rows])
                else:
                    st.info("No rows returned or the result set is empty.")
            except Exception as e:
                st.error(f" Error: {e}")
