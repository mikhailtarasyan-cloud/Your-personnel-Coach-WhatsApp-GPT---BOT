import os, json, time, requests
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# --- Config ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# URL RAW du programme sur GitHub
PROGRAM_URL = "https://raw.githubusercontent.com/mikhailtarasyan-cloud/Your-personnel-Coach-WhatsApp-GPT---BOT/main/program.md"

# --- Charger le programme ---
text = requests.get(PROGRAM_URL).text
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
fragments = splitter.split_text(text)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(fragments, embeddings)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
qa = RetrievalQA.from_chain_type(
    llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff"
)

# --- Mémoire simple JSON ---
MEM_DIR = "user_memory"
os.makedirs(MEM_DIR, exist_ok=True)

def mem_path(user_id): 
    return os.path.join(MEM_DIR, f"{user_id}.json")

def load_mem(user_id):
    p = mem_path(user_id)
    if os.path.exists(p):
        return json.load(open(p, "r", encoding="utf-8"))
    return {
        "user_id": user_id,
        "name": None,
        "language": "fr",
        "stage": 1,
        "completed": [],
        "last_seen": int(time.time())
    }

def save_mem(user_id, data):
    json.dump(data, open(mem_path(user_id), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# --- System Prompt ---
SYSTEM_PROMPT = """
Tu es un mentor IA basé sur le programme «100% CASH».
- Utilise uniquement la base de connaissances (program.md).
- Reste concentré sur l’étape actuelle de l’utilisateur.
- Si la question ne concerne pas le programme → «Je suis ton mentor pour 100% CASH. Restons concentrés sur ton parcours.»
- Termine chaque réponse par une mini-question ou un micro-exercice.
"""

# --- FastAPI ---
app = FastAPI()

# Vérification Render
@app.get("/")
async def root():
    return {"message": "Ton mentor 100% CASH est prêt 🚀"}

# Endpoint WhatsApp (Twilio)
@app.post("/whatsapp")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    user_id = From
    user_text = Body.strip()

    mem = load_mem(user_id)

    # --- Contexte utilisateur ---
    system_ctx = f"""
    Utilisateur: {mem['name'] or 'inconnu'}
    Étape actuelle: {mem['stage']}
    Exercices terminés: {', '.join(mem['completed']) or 'aucun'}
    """

    # --- Réponse IA ---
    answer = qa.run(user_text)

    # --- Reconnaissance du nom ---
    name_triggers = ["je m'appelle", "mon nom est", "je suis", "moi c'est"]
    for trig in name_triggers:
        if trig in user_text.lower():
            mem["name"] = user_text.lower().split(trig)[-1].strip().split()[0].capitalize()
            break

    # --- Validation d'étape (terminé, fini, fais, fait) ---
    stage_triggers = ["terminé", "fini", "fais", "fait"]
    if any(word in user_text.lower() for word in stage_triggers):
        old_stage = mem["stage"]
        mem["completed"].append(f"etape{old_stage}_exo")
        if mem["stage"] < 5:
            mem["stage"] += 1
            answer = f"Bravo {mem['name'] or 'ami'} 🎉 tu as fini l’étape {old_stage}, on passe à l’étape {mem['stage']} 🚀"
        else:
            answer = f"Bravo {mem['name'] or 'ami'} 🎉 tu as complété toutes les étapes du programme ! 🔥"

    # --- Sauvegarde mémoire ---
    mem["last_seen"] = int(time.time())
    save_mem(user_id, mem)

    # --- Réponse Twilio ---
    resp = MessagingResponse()
    resp.message(answer)
    return PlainTextResponse(str(resp))
