import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
azure_endpoint = os.getenv("azure_endpoint")
api_version = os.getenv("api_version")

# Initialize AzureOpenAI instance
llm = AzureOpenAI(
    model="gpt-3.5-turbo-instruct",
    deployment_name="gptbot",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

def generate_response(prompt):
    response = llm(prompt, max_tokens=150, temperature=0.7)
    return response

# Streamlit app
st.title("General Question Answering with Azure OpenAI")

user_input = st.text_area("Enter your prompt:")

if st.button("Get Answer"):
    if user_input:
        answer = generate_response(user_input)
        st.write(answer)
    else:
        st.error("Please enter a prompt.")
