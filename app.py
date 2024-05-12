import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import warnings
import os
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=UserWarning) 
        
model = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, google_api_key=os.getenv('GOOGLE_API_KEY'))

def get_response(user_prompt):
    message = HumanMessage([
    f"""SystemMessage: You are acting as a general purpose answering bot that answers even realtime questions, just give answers, nothing more.
        HumanMessage: {user_prompt}
    """
    ])
    result = model.invoke([
        message
    ])
    return result.content

st.title("Langchain Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# response = get_response(prompt)

if prompt is not None:
    with st.spinner("Waiting for response..."):
        # Get the response
        response = get_response(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})