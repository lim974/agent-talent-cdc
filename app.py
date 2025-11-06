import streamlit as st
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # Pour OpenAI
# from langchain_huggingface import HuggingFaceEndpoint  # Pour HuggingFace, décommentez si besoin

# Récupération du token depuis les secrets Streamlit
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]  # Pour OpenAI
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]  # Pour HuggingFace

# Initialisation du modèle
llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])  # Pour OpenAI
# llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"])  # Pour HuggingFace

templates = {
    "Semaine 1": "Tu es un facilitateur. Aide à cadrer le besoin : {context}",
    "Semaine 2": "Propose des idées et benchmarks pour : {context}",
    "Semaine 3": "Donne des conseils pour prototyper et tester : {context}",
    "Semaine 4": "Synthétise les livrables en rapport structuré : {context}"
}

st.title("Assistant Sprint – MVP (LangChain nouvelle version)")
step = st.selectbox("Choisir l'étape du sprint :", list(templates.keys()))
context = st.text_area("Décris le contexte ou l'irritant :")

if st.button("Générer recommandations"):
    prompt = PromptTemplate(template=templates[step], input_variables=["context"])
    # Nouvelle façon d'exécuter le prompt avec le LLM
    result = llm.invoke(prompt.format(context=context))
    st.write("### Recommandations :")
    st.write(result)

st.subheader("Checklist")
tasks = ["Cadrage terminé", "Benchmark réalisé", "Prototype créé", "Tests effectués", "Rapport rédigé"]
for task in tasks:
    st.checkbox(task)
st.file_uploader("Uploader livrables (Word, PDF)", accept_multiple_files=True)