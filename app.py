import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

# 🔑 Récupération de la clé OpenAI depuis les secrets Streamlit
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialisation du modèle OpenAI via LangChain
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Templates pour chaque étape du sprint
templates = {
    "Semaine 1": "Tu es un facilitateur. Aide à cadrer le besoin : {context}",
    "Semaine 2": "Propose des idées et benchmarks pour : {context}",
    "Semaine 3": "Donne des conseils pour prototyper et tester : {context}",
    "Semaine 4": "Synthétise les livrables en rapport structuré : {context}"
}

# Sauvegarde état du sprint
STATE_FILE = "sprint_state.json"

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

# Interface Streamlit
st.title("Assistant Sprint – MVP")
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

# Checklist interactive
st.subheader("Checklist")
tasks = ["Cadrage terminé", "Benchmark réalisé", "Prototype créé", "Tests effectués", "Rapport rédigé"]
for task in tasks:
    checked = st.checkbox(task, value=state.get(task, False))
    state[task] = checked
save_state(state)

# Upload livrables
uploaded_files = st.file_uploader("Uploader livrables (Word, PDF)", accept_multiple_files=True)
if uploaded_files:
    st.write(f"{len(uploaded_files)} fichiers uploadés.")