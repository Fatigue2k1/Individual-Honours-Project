import streamlit as st

def main():
    st.set_page_config(layout="centered")
    st.header("Natural Language to Code Generation")

    # Add line between title and input section with reduced opacity
    st.markdown("<div class='line faded-line'></div>", unsafe_allow_html=True)

    # Custom CSS to style the input and rerun boxes
    st.markdown("""
        <style>
        .expanding-box {
            background-color: #2D2D3B;  /* Dark background color */
            padding: 15px;  /* Padding inside the box */
            border-radius: 10px;  /* Rounded corners */
            color: white;  /* Text color */
            font-size: 16px;  /* Font size */
            border: none;  /* No border */
            display: inline-block;
            white-space: pre-wrap;  /* Preserve whitespace and wrap text */
            width: 100%;  /* Take full width */
            min-height: 50px;  /* Minimum height */
        }
        .line {
            border-top: 1px solid white;  /* White line */
            margin: 15px 0;  /* Margin space */
        }
        .faded-line {
            opacity: 0.5;  /* Reduced opacity */
        }
        </style>
        """, unsafe_allow_html=True)

    # Create the input boxes
    st.subheader("Natural Language Input")
    natural_language_input = st.text_area("Enter your question here", height=100)
    
    # Insert line between input boxes with reduced opacity
    st.markdown("<div class='line faded-line'></div>", unsafe_allow_html=True)
    
    st.subheader("Data Input")
    data_input = st.text_area("Enter the data here", height=50)

    # Add a button to trigger the chatbot response
    if st.button("Rerun"):
        # Check for specific keyword
        if "summarize" in natural_language_input.lower():
            # Generate specific output for summarization
            rerun = generate_summarization(data_input)
        else:
            # Call the chatbot function to generate the response
            rerun = generate_rerun(natural_language_input, data_input)
        
        st.session_state.rerun = rerun  # Store the rerun in session state

    # Display the "Output" section
    st.subheader("Output")
    if "rerun" in st.session_state:
        st.markdown(f"""
            <div class="expanding-box">{st.session_state.rerun}</div>
        """, unsafe_allow_html=True)

def generate_rerun(natural_language, data):
    # Placeholder function for the chatbot logic
    return f"The rerun for the '{natural_language}' with data '{data}' is: This is a sample rerun."

def generate_summarization(data):
    # Placeholder function for summarization logic
    # Implement your summarization logic here
    return (
    "GPT-like language models have made building chat-based applications easier. "
    "Streamlit's Chat elements, combined with session state management, let developers "
    "create conversational interfaces effortlessly using Python alone. "
    "It's a fast way to prototype and deploy AI-powered chatbots."
    )


if __name__ == "__main__":
    main()
