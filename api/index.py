from flask import Flask
import requests
import os

app = Flask(__name__)

# Pega o token do ambiente
# Certifique-se que na Vercel a Key seja exatamente "GH_TOKEN"
TOKEN = os.getenv("GH_TOKEN_30min")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Lista de workflows a serem acionados
WORKFLOWS = [
    {"repo": "contagem_piso_out_sp5", "workflow": "piso_exp.yaml"},
    #{"repo": "FIFO_INBOUND_SP5", "workflow": "fifo_in_sp5.yaml"},
]

# Rota principal para verificar se o app está no ar
@app.route('/')
def home():
    return "Servidor do agendador de workflows do GitHub está no ar."

# Rota que será chamada pelo Cron Job da Vercel
@app.route('/api/trigger')
def trigger_workflows():
    # Loop que executa a lógica UMA VEZ por chamada
    for wf in WORKFLOWS:
        # ALTERAÇÃO: Atualizado de Murilosantana7 para joaopavanelo-lang
        url = f"https://api.github.com/repos/joaopavanelo-lang/{wf['repo']}/actions/workflows/{wf['workflow']}/dispatches"
        data = {"ref": "main"}
        try:
            res = requests.post(url, headers=HEADERS, json=data)
            print(f"[OK] {wf['workflow']} -> {res.status_code}")
        except Exception as e:
            print(f"[ERRO] {wf['workflow']} -> {e}")
    
    return "Workflows acionados com sucesso!", 200
