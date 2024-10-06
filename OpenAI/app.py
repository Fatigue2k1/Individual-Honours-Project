import os
import openai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI API key
openai.api_key = api_key

# Function to sanitize and process the output from OpenAI
def _sanitize_output(llm_output, code_type="python"):
    try:
        code = llm_output.split(f'```{code_type}')[1].split('```')[0].strip()
        return code
    except IndexError:
        return f"Error: Unable to extract {code_type} code from the response."

# Function to generate code using OpenAI API
def generate_code(prompt1, prompt2, code_type="python"):
    try:
        template = f"""Write some {code_type} code to solve the user's problem.

        Return only {code_type} code in Markdown format, e.g.:

        ```{code_type}
        ....
        ```
        {prompt1} {prompt2}"""
        
        # Call the OpenAI API for generating code
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": template}
            ],
            max_tokens=500  # Adjust the token limit based on your use case
        )
        
        llm_output = response.choices[0].message['content']
        output = _sanitize_output(llm_output, code_type)
        return output
    except Exception as e:
        return f"Error: {e}"

# Function to run predefined test cases
def run_test_cases():
    test_cases = [
        {
            "prompt1": "Calculate the sum of two numbers.",
            "prompt2": "Input: a = 5, b = 10",
        },
        {
            "prompt1": "Sort a list of integers.",
            "prompt2": "Input: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]",
        },
        {
            "prompt1": "Find the maximum value in a list.",
            "prompt2": "Input: [10, 22, 5, 75, 65, 80]",
        },
    ]

    results = []
    for test in test_cases:
        code = generate_code(test["prompt1"], test["prompt2"])
        results.append({
            "prompt1": test["prompt1"],
            "prompt2": test["prompt2"],
            "actual_output": code
        })
    
    return results

# Page functions
def code_generation():
    st.title("Code Generation")
    prompt1 = st.text_area("Enter your question (e.g., how can I code Python this math):", height=100, key='cg_prompt1')
    prompt2 = st.text_area("Enter your data:", height=100, key='cg_prompt2')

    if st.button("Generate Code", key='cg_generate_code'):
        if prompt1 and prompt2:
            code = generate_code(prompt1, prompt2)
            st.session_state.generated_code = code  # Store generated code in session state

    if 'generated_code' in st.session_state:
        st.subheader("Generated Python Code:")
        st.code(st.session_state.generated_code, language='python')

    if st.button("Run Test Cases", key='cg_run_test_cases'):
        results = run_test_cases()
        for result in results:
            st.write(f"Prompt 1: {result['prompt1']}")
            st.write(f"Prompt 2: {result['prompt2']}")
            st.subheader("Actual Output:")
            st.code(result['actual_output'], language='python')
            st.write("---")

def sql_generation():
    st.title("SQL Code Generation")
    prompt1 = st.text_area("Enter your SQL query problem:", height=100, key='sql_prompt1')
    prompt2 = st.text_area("Enter your data:", height=100, key='sql_prompt2')

    if st.button("Generate SQL Code", key='sql_generate_code'):
        if prompt1 and prompt2:
            code = generate_code(prompt1, prompt2, code_type="sql")
            st.session_state.generated_sql_code = code  # Store generated SQL code in session state

    if 'generated_sql_code' in st.session_state:
        st.subheader("Generated SQL Code:")
        st.code(st.session_state.generated_sql_code, language='sql')

def unit_test_generation():
    st.title("Unit Test Case Generation")
    prompt1 = st.text_area("Enter the function you want to test:", height=100, key='ut_prompt1')
    prompt2 = st.text_area("Enter the scenarios you want to test:", height=100, key='ut_prompt2')

    if st.button("Generate Unit Test Cases", key='ut_generate_code'):
        if prompt1 and prompt2:
            code = generate_code(
                f"Generate unit test cases for the following function:\n\n{prompt1}\n\nTest scenarios:\n{prompt2}", 
                "", 
                code_type="python"
            )
            st.session_state.generated_unit_test_code = code  # Store generated unit test code in session state

    if 'generated_unit_test_code' in st.session_state:
        st.subheader("Generated Unit Test Code:")
        st.code(st.session_state.generated_unit_test_code, language='python')

def regex_generation():
    st.title("Regular Expression Generation")
    prompt1 = st.text_area("Enter the pattern you want to match:", height=100, key='re_prompt1')
    prompt2 = st.text_area("Enter the string data to match against:", height=100, key='re_prompt2')

    if st.button("Generate Regular Expression", key='re_generate_code'):
        if prompt1 and prompt2:
            code = generate_code(prompt1, prompt2, code_type="python")
            st.session_state.generated_regex_code = code  # Store generated regex code in session state

    if 'generated_regex_code' in st.session_state:
        st.subheader("Generated Regular Expression Code:")
        st.code(st.session_state.generated_regex_code, language='python')

def main():
    # Mapping page names to their respective functions
    PAGES = {
        "Code Generation": code_generation,
        "SQL Code Generation": sql_generation,
        "Unit Test Case Generation": unit_test_generation,
        "Regular Expression Generation": regex_generation,
    }

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Display the selected page
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()
