import streamlit as st
import os
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

# Récupération du token Hugging Face depuis les secrets Streamlit
os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

# Initialisation du modèle SmolLM3-3B

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceTB/SmolLM3-3B",
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    task="text-generation"
)


templates = {
    "Semaine 1": "Tu es un facilitateur. Aide à cadrer le besoin : {context}",
    "Semaine 2": "Propose des idées et benchmarks pour : {context}",
    "Semaine 3": "Donne des conseils pour prototyper et tester : {context}",
    "Semaine 4": "Synthétise les livrables en rapport structuré : {context}"
}

st.title("Assistant Sprint – MVP (SmolLM3-3B Hugging Face)")
step = st.selectbox("Choisir l'étape du sprint :", list(templates.keys()))
context = st.text_area("Décris le contexte ou l'irritant :")

if st.button("Générer recommandations"):
    prompt = PromptTemplate(template=templates[step], input_variables=["context"])
    result = llm.invoke(prompt.format(context=context))
    st.write("### Recommandations :")
    st.write(result)

st.subheader("Checklist")
tasks = ["Cadrage terminé", "Benchmark réalisé", "Prototype créé", "Tests effectués", "Rapport rédigé"]
for task in tasks:
    st.checkbox(task)
st.file_uploader("Uploader livrables (Word, PDF)", accept_multiple_files=True)