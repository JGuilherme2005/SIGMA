# backend/main.py
from .models import engine, Denuncia
import pika  # NOVO: Importa a biblioteca do RabbitMQ
import os    # NOVO: Para ler variáveis de ambiente
import json  # NOVO: Para formatar a mensagem
from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from .models import engine, Denuncia
from geoalchemy2.shape import to_shape

# --- Configuração do Banco de Dados (sem alterações) ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# --- NOVO: Função para Enviar Mensagem ao RabbitMQ ---
def enviar_para_fila(denuncia_id: int):
    # Pega o host do RabbitMQ do environment, com um fallback para localhost
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    
    try:
        # Conecta ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()

        # Declara a fila 'fila_denuncias'. Se não existir, ela será criada.
        # durable=True faz com que a fila sobreviva a reinicializações do RabbitMQ
        channel.queue_declare(queue='fila_denuncias', durable=True)

        # Prepara a mensagem (o ID da denúncia)
        mensagem = json.dumps({'denuncia_id': denuncia_id})

        # Publica a mensagem na fila
        channel.basic_publish(
            exchange='',
            routing_key='fila_denuncias',
            body=mensagem,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Torna a mensagem persistente
            ))
        
        print(f" [x] Enviado para a fila a denúncia com ID: {denuncia_id}")
        connection.close()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Erro ao conectar com o RabbitMQ: {e}")
        # Em um sistema de produção, você poderia ter uma lógica de fallback aqui
    
# --- Modelo Pydantic (sem alterações) ---
class DenunciaCreate(BaseModel):
    tipo: str
    descricao: str
    latitude: float
    longitude: float

# --- Endpoint de Criação de Denúncia (MODIFICADO) ---
@app.post("/denuncias/")
def criar_denuncia(denuncia_data: DenunciaCreate, db: Session = Depends(get_db)):
    ponto_wkt = f'POINT({denuncia_data.longitude} {denuncia_data.latitude})'
    
    nova_denuncia = Denuncia(
        tipo=denuncia_data.tipo,
        descricao=denuncia_data.descricao,
        localizacao=ponto_wkt,
        status='recebido' # Status inicial
    )
    db.add(nova_denuncia)
    db.commit()
    db.refresh(nova_denuncia) # Garante que o ID foi gerado

    # ---- NOVO: Envia o ID para a fila após salvar no banco ----
    enviar_para_fila(nova_denuncia.id)
    # -----------------------------------------------------------
    
    return {"id": nova_denuncia.id, "status": "Denúncia recebida e enviada para análise!"}

# --- Endpoint de Listagem (sem alterações) ---
@app.get("/denuncias/")
def listar_denuncias(db: Session = Depends(get_db)):
    denuncias = db.query(Denuncia).all()
    resultado = []
    for d in denuncias:
        ponto = to_shape(d.localizacao)
        resultado.append({
            "id": d.id,
            "tipo": d.tipo,
            "descricao": d.descricao,
            "status": d.status,
            "latitude": ponto.y,
            "longitude": ponto.x,
            "timestamp": d.timestamp
        })
    return resultado