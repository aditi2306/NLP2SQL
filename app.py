import streamlit as st
from langchain_t5_sql import run_query
import asyncio
import os


os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


st.title("NLP to SQL with LangChain + T5")

question = st.text_input("Enter your question:")

if st.button("Run Query"):
    with st.spinner("Running..."):
        try:
            result = run_query(question)
            st.success("Success!")
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")


try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
