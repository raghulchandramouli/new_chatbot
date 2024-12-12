import os
import streamlit as st
import google.generativeai as genai

# Configure the API key
genai.configure(api_key='AIzaSyBWbzlo2o88kUoZVyAV-jGBDLubOt7yVx8')

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
)

# Streamlit application layout
st.title("Chat bot")

# User input for the chat
user_input = st.text_input("Your question:")

# Initialize session state for storing responses and feedback
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []

if st.button("Submit"):
    if user_input:
        # Start a chat session
        chat_session = model.start_chat(history=[])
        
        # Send the user's message and get a response
        response = chat_session.send_message(user_input)
        
        # Store the response in session state
        st.session_state.responses.append(response.text)
        
        # Display the response
        st.write("AI Response:")
        st.write(response.text)
        
        # Feedback options
        feedback = st.radio("How helpful was this response?", ["Select", "Helpful", "Not Helpful"])
        
        if feedback != "Select":
            # Store feedback in session state
            st.session_state.feedback.append(feedback)
            st.write(f"Thank you for your feedback: {feedback}")
            
            # Optionally, you could save this data to a file or database here
            
    else:
        st.write("Please enter a question.")

# Display all previous responses and their feedback (optional)
if st.session_state.responses:
    for i, (resp, fb) in enumerate(zip(st.session_state.responses, st.session_state.feedback)):
        st.write(f"*Response {i + 1}:* {resp} (Feedback: {fb})")
