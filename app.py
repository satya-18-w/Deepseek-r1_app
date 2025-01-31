import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate,HumanMessagePromptTemplate,AIMessagePromptTemplate,ChatPromptTemplate

# Custom CSS styling
st.markdown("""
<style>
    /* Existing styles */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    
    /* Add these new styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    
    .stSelectbox svg {
        fill: white !important;
    }
    
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    /* For dropdown menu items */
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Deepseek Code Companion")
st.caption("🚀 Your AI Pair Programmer with Debugging Superpowers")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model=st.selectbox(
        "Select amodel",
        ["deepseek-r1:1.5b","mistral:latest"],
        index=0
    )
    st.divider()
    st.markdown("Model Capabilities")
    st.markdown(
        """
    - 🐍 Python Expert
    - 🐞 Debugging Assistant
    - 📝 Code Documentation
    - 💡 Solution Design
    """
    )
    st.divider()
    st.markdown("APP Built with [Ollama](https://ollama.ai) | [Langchain](https://python.langchain.com/)")
    
    
    
    
# Intitatye the chat engine

if selected_model == "deepseek-r1:1.5b":
    llm_model=ChatOllama(model=selected_model,base_url="http://localhost:11434",temperature=0.8)
    
else:
    llm_model=ChatOllama(model="mistral:latest",temperature=0.9)    

# System Prompt Configuration
system_prompt=SystemMessagePromptTemplate.from_template(
    "You are an expert AI Coding assistant. provide concise,exact solutions"
    "with strategic print statements for debugging. Always respond in english"
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today? 💻"}]
    
    
# chat Container

chat_container=st.container()

# Display chat Messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            
user_query=st.chat_input("Type your coding question here...")

def generate_ai_response(prompt_chain):
    preprocessing_pipeline=prompt_chain | llm_model | StrOutputParser()
    
    return preprocessing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence=[system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
            
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))    
            
            
    return ChatPromptTemplate.from_messages(prompt_sequence)        


if user_query:
    # Add user messsage to the quert
    st.session_state.message_log.append({"role":"user","content":user_query})
    
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain=build_prompt_chain()
        ai_response=generate_ai_response(prompt_chain)
        
    # ADD AI response to log
    st.session_state.message_log.append({"role":"ai","content":ai_response})
    # RErun to update chat display
    st.rerun()