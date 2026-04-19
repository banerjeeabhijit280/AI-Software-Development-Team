import os
import streamlit as st
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# LangChain Imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

# ==========================================
# PAGE CONFIGURATION FOR PREMIUM SCREENSHOTS
# ==========================================
st.set_page_config(page_title="AI Dev Team", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #B0BEC5;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #FFF;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚀 Multi-Agent AI Software Development Team</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Enter a project idea, and watch 5 specialized AI agents collaboratively define, design, code, test, and review the project in parallel.</p>', unsafe_allow_html=True)


# ==========================================
# LANGCHAIN AGENT PIPELINE LOGIC
# ==========================================

# 1. Project Idea Prompt
ProjectIdea = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a system planner for a multi-agent AI software team.

Divide the project into EXACTLY 5 sections:

1. Product Manager Agent → Define requirements
2. Architect Agent → Design system
3. Developer Agent → Write code
4. Tester Agent → Create test cases
5. Reviewer Agent → Review code

Return output in STRICT structured format:

Product_Manager:
...
Architect:
...
Developer:
...
Tester:
...
Reviewer:
..."""),
        ("human", "{text}")
    ]
)

llm_ola = ChatOllama(model="mistral", temperature=0)
str_parser = StrOutputParser()

def dictionary_maker(text: str) -> dict:
    return {"text": text}

dictionary_maker_runnable = RunnableLambda(dictionary_maker)


def Product_Manager(text):
    text = text["text"]
    PromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "you are the Product Manager of a company, search for the section that deals with product management and convert it into clear requirements"),
        ("human", "Give me the requirements, Features list, API endpoints and Constraints for the following project: {text}")
    ])
    chain = PromptTemplate | llm_ola | str_parser
    return chain.invoke(text)

def Architect(text):
    text = text["text"]
    PromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "you are the Architect of a company, search for the section that deals with Architect and design system structure"),
        ("human", "Give me the design, Folder structure, Tech stack decisions, DB schema for the following project: {text}")
    ])
    chain = PromptTemplate | llm_ola | str_parser
    return chain.invoke(text)

def Developer(text):
    text = text["text"]
    PromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "you are the Developer of a company, search for the section that deals with Developer"),
        ("human", "Give me the details how you will write the code with examples for the following project: {text}")
    ])
    chain = PromptTemplate | llm_ola | str_parser
    return chain.invoke(text)

def Tester(text):
    text = text["text"]
    PromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "you are the Tester of a company, search for the section that deals with Tester"),
        ("human", "Generate test cases for the following project: {text}")
    ])
    chain = PromptTemplate | llm_ola | str_parser
    return chain.invoke(text)

def Reviewer(text):
    text = text["text"]
    PromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "you are the Reviewer of a company, search for the section that deals with Reviewer"),
        ("human", "Review everything for the following project: {text}")
    ])
    chain = PromptTemplate | llm_ola | str_parser
    return chain.invoke(text)

# Agent Wrappers (Bugs from original notebook fixed!)
Product_Manager_agent = RunnableLambda(Product_Manager)    
Architect_agent = RunnableLambda(Architect)   
Developer_agent = RunnableLambda(Developer)   
Tester_agent = RunnableLambda(Tester)   
Reviewer_agent = RunnableLambda(Reviewer)


# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================

st.markdown("---")

col1, col2 = st.columns([4, 1])

with col1:
    project_idea = st.text_area(
        "💡 Your Project Idea", 
        placeholder="E.g., Build a cross-platform battery monitor utility app over websockets...", 
        height=100,
        label_visibility="collapsed"
    )

with col2:
    submit_btn = st.button("Assemble Team & Build ✨", type="primary", use_container_width=True)

if submit_btn:
    if not project_idea:
        st.warning("Please enter a project idea first!")
    else:
        with st.spinner("🧠 Initializing AI Cores and Planning Architecture..."):
            try:
                # Execution Pipeline
                chain = ProjectIdea | llm_ola | str_parser | dictionary_maker_runnable | RunnableParallel(
                    branches={
                        "Product Manager": Product_Manager_agent, 
                        "Architect": Architect_agent, 
                        "Developer": Developer_agent, 
                        "Tester": Tester_agent, 
                        "Reviewer": Reviewer_agent
                    }
                )
                
                # Dynamic terminal-like output indicator
                status_placeholder = st.empty()
                status_placeholder.info("⚡ Executing parallel workflows... (Inferencing via Ollama `mistral` model)")
                
                response = chain.invoke({"text": project_idea})
                res_dict = response['branches']
                
                status_placeholder.success("✅ **Team Pipeline Completed!** Collaboration successful.")
                
                # Dynamic Tabs for final output rendering
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📊 Product Manager", 
                    "🏗️ Architect", 
                    "💻 Developer", 
                    "🧪 Tester", 
                    "🧐 Reviewer"
                ])
                
                placeholder_error = "No output was generated."
                
                with tab1:
                    st.write(res_dict.get('Product Manager', placeholder_error))
                with tab2:
                    st.write(res_dict.get('Architect', placeholder_error))
                with tab3:
                    st.write(res_dict.get('Developer', placeholder_error))
                with tab4:
                    st.write(res_dict.get('Tester', placeholder_error))
                with tab5:
                    st.write(res_dict.get('Reviewer', placeholder_error))
                    
            except Exception as e:
                st.error(f"An error occurred during execution: {e}")
                st.info("Make sure Ollama is running locally and the 'mistral' model is installed!")
