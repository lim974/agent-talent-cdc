import streamlit as st
import os
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

# 🔑 Récupération du token Hugging Face depuis les secrets Streamlit
os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

# Initialisation du modèle Hugging Face (exemple : mistralai/Mistral-7B-Instruct-v0.2)
llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    model_kwargs={"temperature": 0.3, "max_new_tokens": 512}
)

templates = {
    "Semaine 1": "Tu es un facilitateur. Aide à cadrer le besoin : {context}",
    "Semaine 2": "Propose des idées et benchmarks pour : {context}",
    "Semaine 3": "Donne des conseils pour prototyper et tester : {context}",
    "Semaine 4": "Synthétise les livrables en rapport structuré : {context}"
}

STATE_FILE = "sprint_state.json"

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

st.title("Assistant Sprint – MVP (Hugging Face)")
state = load_state()

step = st.selectbox("Choisir l'étape du sprint :", list(templates.keys()))
context = st.text_area("Décris le contexte ou l'irritant :", state.get("context", ""))

if st.button("Générer recommandations"):
    prompt = PromptTemplate(template=templates[step], input_variables=["context"])
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(context=context)
    st.write("### Recommandations :")
    st.write(result)
    state["context"] = context
    state["last_result"] = result
    save_state(state)

st.subheader("Checklist")
tasks = ["Cadrage terminé", "Benchmark réalisé", "Prototype créé", "Tests effectués", "Rapport rédigé"]
for task in tasks:
    checked = st.checkbox(task, value=state.get(task, False))
    state[task] = checked
save_state(state)

uploaded_files = st.file_uploader("Uploader livrables (Word, PDF)", accept_multiple_files=True)
if uploaded_files:
    st.write(f"{len(uploaded_files)} fichiers uploadés.")