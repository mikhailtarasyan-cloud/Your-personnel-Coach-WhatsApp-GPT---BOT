import os, json, time, requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# --- Config ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# URL de ton programme GitHub (RAW)
PROGRAM_URL = "https://github.com/mikhailtarasyan-cloud/Your-personnel-Coach-WhatsApp-GPT---BOT/blob/main/program.md"

# --- Charger programme ---
text = requests.get(PROGRAM_URL).text
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
fragments = splitter.split_text(text)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(fragments, embeddings)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(), chain_type="stuff")

# --- Mémoire simple JSON ---
MEM_DIR = "user_memory"
os.makedirs(MEM_DIR, exist_ok=True)

def mem_path(user_id): return os.path.join(MEM_DIR, f"{user_id}.json")

def load_mem(user_id):
    p = mem_path(user_id)
    if os.path.exists(p):
        return json.load(open(p, "r", encoding="utf-8"))
    return {"user_id": user_id, "name": None, "language": "fr", "stage": 1, "completed": [], "last_seen": int(time.time())}

def save_mem(user_id, data):
    json.dump(data, open(mem_path(user_id), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# --- System Prompt ---
SYSTEM_PROMPT = """
Tu es un mentor IA basé sur le programme «100% CASH».
- Utilise uniquement la base program.md.
- Reste concentré sur l’étape actuelle de l’utilisateur.
- Si question hors programme → «Je suis ton mentor pour 100% CASH. Restons concentrés sur ton parcours.»
- Termine chaque réponse par une mini-question ou micro-exercice.
"""

# --- FastAPI ---
app = FastAPI()

@app.post("/whatsapp")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    user_id = From
    user_text = Body.strip()

    mem = load_mem(user_id)

    # contexte mémoire
    system_ctx = f"""
    Utilisateur: {mem['name'] or 'inconnu'}
    Étape actuelle: {mem['stage']}
    Exercices terminés: {', '.join(mem['completed']) or 'aucun'}
    """

    # réponse IA
    answer = qa.run(user_text)

    # mise à jour mémoire
    if "terminé" in user_text.lower():
        mem["completed"].append(f"etape{mem['stage']}_exo")
        if mem["stage"] < 5:
            mem["stage"] += 1
    mem["last_seen"] = int(time.time())
    save_mem(user_id, mem)

    # Twilio response
    resp = MessagingResponse()
    resp.message(answer)
    return PlainTextResponse(str(resp))
