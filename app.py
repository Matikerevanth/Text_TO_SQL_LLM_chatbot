import streamlit as st
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyAmfRxQKSWnE9hn8TzPoy_HdEg7mcrSRVA"

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser


# Streamlit Page Config
st.set_page_config(page_title="Text to SQL Generator", page_icon="🧠")



# Background Image + Glass UI Styling
def add_bg_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f2f5f9;   /* Light grey-blue */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


add_bg_color()

# --------------------------------------------------------
# Database Configuration
# --------------------------------------------------------
host = 'localhost'
user = 'root'
password = '1234'
database = 'text_to_sql'

mysql_uri = f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"

db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=2)



# --------------------------------------------------------
# Prompt Template
# --------------------------------------------------------
template = """
You are an expert SQL generator.
You MUST return only a valid SQL query.

Database Schema:
{schema}

User Question: {question}

SQL Query:
"""

prompt = ChatPromptTemplate.from_template(template)




# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
)

chain = prompt | llm | StrOutputParser()


# Streamlit UI

st.title("🧠 Text → SQL Query Generator")
st.write("Enter a natural language question and generate the SQL query.")


question = st.text_input("Enter your question:")

if st.button("Generate SQL"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        schema = db.get_table_info()
        sql = chain.invoke({"question": question, "schema": schema})

        st.subheader("Generated SQL Query:")
        st.code(sql, language="sql")
