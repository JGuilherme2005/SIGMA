# main.py
from fastapi import FastAPI, APIRouter, HTTPException, Body
from typing import List
import time

# Importa os modelos de dados que criamos
from models import CitizenReportInput, Alert, IAPrediction

# --- Bloco de Simulação (Mocks) ---
# Em um sistema real, isso seria substituído por bancos de dados, modelos de IA e APIs reais.

# "Banco de Dados" em memória (uma simples lista Python)
ALERTS_DB: List[Alert] = []

# MOCK: Núcleo de IA Preditiva
def mock_predictive_ai(report: CitizenReportInput) -> IAPrediction:
    """Simula a IA analisando a descrição e retornando uma predição."""
    desc = report.description.lower()
    if any(keyword in desc for keyword in ["tiro", "assalto", "briga", "violência"]):
        return IAPrediction(risk_level="crítico", category="violencia", suggested_action="Despachar Polícia Militar (190)")
    elif any(keyword in desc for keyword in ["acidente", "batida", "atropelamento"]):
        return IAPrediction(risk_level="alto", category="acidente_transito", suggested_action="Despachar SAMU (192) e PM de Trânsito")
    elif any(keyword in desc for keyword in ["doente", "passando mal", "infarto"]):
        return IAPrediction(risk_level="alto", category="saude", suggested_action="Despachar SAMU (192)")
    elif any(keyword in desc for keyword in ["buraco", "lixo", "poste apagado", "iluminação"]):
        return IAPrediction(risk_level="baixo", category="desordem_urbana", suggested_action="Acionar Secretaria de Obras da Prefeitura")
    else:
        return IAPrediction(risk_level="médio", category="desordem_urbana", suggested_action="Análise manual requerida pelo painel de comando")

# MOCK: Núcleo de Integração Institucional (NII)
def mock_dispatch_resource(action: str, alert_id: str):
    """Simula o envio de um comando para a instituição correta."""
    print(f"\n[NII-LOG] Disparando Ação: '{action}' para o Alerta ID: {alert_id}")
    print(f"[NII-LOG] Conectando com a API da instituição correspondente...")
    time.sleep(1) # Simula latência da rede
    print(f"[NII-LOG] Ordem enviada com sucesso!")

# MOCK: Serviço de Auditoria em Blockchain
def mock_log_to_blockchain(alert_id: str, event_description: str):
    """Simula o registro de um evento imutável na blockchain."""
    print(f"\n[BLOCKCHAIN-LOG] Registrando evento para Alerta ID: {alert_id}")
    print(f"  -> Evento: '{event_description}'")
    print(f"  -> Hash da Transação: 0x{hash(f'{alert_id}{event_description}{time.time()}'):x}")


# --- Configuração do FastAPI ---

app = FastAPI(
    title="🛡️ SIGMA - Backend API",
    description="Plataforma nacional de IA preditiva para segurança pública urbana.",
    version="1.0.0",
)

# Roteadores para organizar os endpoints por funcionalidade
citizen_router = APIRouter(prefix="/cidadao", tags=["Módulo Cidadão Ativo"])
dashboard_router = APIRouter(prefix="/painel", tags=["Painel de Comando Integrado"])


# --- Lógica de Orquestração ---

def process_and_dispatch_alert(alert: Alert):
    """
    Esta é a função central do "Protocolo de Resposta Automatizado".
    Ela é chamada assim que um novo alerta é criado.
    """
    print(f"\n--- INICIANDO PROTOCOLO DE RESPOSTA AUTOMATIZADO PARA ALERTA {alert.id} ---")
    
    # 1. Loga a criação do alerta na Blockchain
    mock_log_to_blockchain(alert.id, "Alerta Criado e Validado pela IA")
    
    # 2. Executa a ação sugerida pela IA
    action = alert.prediction.suggested_action
    mock_dispatch_resource(action, alert.id)
    
    # 3. Atualiza o status do alerta no banco de dados
    alert.status = "em_atendimento"
    
    # 4. Loga o despacho na Blockchain
    mock_log_to_blockchain(alert.id, f"Recurso Despachado: {action}")
    print("--- FIM DO PROTOCOLO ---")


# --- Endpoints da API ---

@citizen_router.post("/denuncia", response_model=Alert, status_code=201)
def create_citizen_report(report: CitizenReportInput = Body(...)):
    """
    Recebe uma nova denúncia de um cidadão (via PWA ou WhatsApp).
    """
    # 1. IA Preditiva analisa a denúncia
    prediction = mock_predictive_ai(report)
    
    # 2. Cria o objeto de Alerta completo
    new_alert = Alert(report=report, prediction=prediction)
    
    # 3. "Salva" o alerta no nosso banco de dados em memória
    ALERTS_DB.append(new_alert)
    
    # 4. Inicia o fluxo de resposta automática
    process_and_dispatch_alert(new_alert)
    
    # 5. Retorna o alerta criado para o cliente
    return new_alert

@dashboard_router.get("/alertas", response_model=List[Alert])
def get_all_alerts():
    """
    Fornece todos os alertas para o Painel de Comando Integrado.
    """
    # Retorna a lista em ordem decrescente (mais novos primeiro)
    return sorted(ALERTS_DB, key=lambda x: x.timestamp, reverse=True)

@dashboard_router.get("/alertas/{alert_id}", response_model=Alert)
def get_alert_by_id(alert_id: str):
    """
    Busca um alerta específico pelo seu ID.
    """
    for alert in ALERTS_DB:
        if alert.id == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alerta não encontrado")

# Inclui os roteadores na aplicação principal
app.include_router(citizen_router)
app.include_router(dashboard_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do SIGMA. Acesse /docs para ver a documentação."}