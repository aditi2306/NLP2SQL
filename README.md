# NLP2SQL: Natural Language to SQL Query Generator

[![Streamlit App](https://img.shields.io/badge/Streamlit-LiveApp-ff4b4b?logo=streamlit)](https://aditi2306-nlp2sql-app-r0bk17.streamlit.app/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Powered-10a37f?logo=openai)](https://platform.openai.com/)

NLP2SQL is an interactive Streamlit-based application that translates natural language questions into executable SQL queries. It leverages OpenAI's GPT models and tools for intelligent query generation, table understanding, and result retrieval.

---

## Features

- Translate natural language questions into SQL queries
- Uses OpenAI for context-aware query generation
- Executes SQL queries and displays results in real time

---

## Live Demo

Try the app at: [Streamlit App](https://aditi2306-nlp2sql-app-r0bk17.streamlit.app/)

---

## Configuration
Create a .env file in the root directory or set the environment variable:
OPENAI_API_KEY=your_api_key_here

---
## Project Structure 

NLP2SQL/
├── app.py                 # Main Streamlit application
├── sql_generator.py       # NL to SQL logic
├── utils.py               # Helper functions
├── sample.csv             # Example dataset
├── requirements.txt       # Dependencies
└── README.md              # Project documentation


---
## Installation

```bash
git clone https://github.com/aditi2306/NLP2SQL.git
cd NLP2SQL
pip install -r requirements.txt
streamlit run app.py

```

---

### Author 
developed by Aditi



