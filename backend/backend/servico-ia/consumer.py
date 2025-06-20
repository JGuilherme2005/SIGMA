# servico-ia/consumer.py
import pika
import os
import time
import json
from sqlalchemy import create_engine, Column, Integer, String, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# --- Configuração do Banco de Dados (igual ao outro serviço, mas lendo de seu próprio env) ---
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://sigma:sigma_password@localhost:5432/sigma_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definimos um modelo mínimo aqui para poder interagir com a tabela 'denuncias'
class Denuncia(Base):
    __tablename__ = 'denuncias'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))

# --- Lógica do Consumidor ---
def processar_denuncia(denuncia_id: int):
    """
    Esta função busca a denúncia no banco, simula o processamento da IA
    e atualiza o status.
    """
    db = SessionLocal()
    try:
        print(f"Processando denúncia ID: {denuncia_id}...")
        
        # Simula o trabalho da IA (análise de risco, etc.)
        time.sleep(5)  # Simula uma tarefa que leva 5 segundos

        # Atualiza o status da denúncia no banco de dados para 'analisado'
        stmt = (
            update(Denuncia).
            where(Denuncia.id == denuncia_id).
            values(status='analisado_pela_ia')
        )
        db.execute(stmt)
        db.commit()
        
        print(f"Denúncia ID: {denuncia_id} processada e status atualizado para 'analisado_pela_ia'.")
        
    finally:
        db.close()

def callback(ch, method, properties, body):
    """
    Função chamada toda vez que uma mensagem é recebida da fila.
    """
    print(f" [x] Recebido: {body}")
    
    try:
        dados = json.loads(body)
        denuncia_id = dados['denuncia_id']
        processar_denuncia(denuncia_id)
        
        # Confirma ao RabbitMQ que a mensagem foi processada com sucesso
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Mensagem processada e confirmada (ack).")
        
    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")
        # Aqui você poderia implementar uma lógica para reenviar a mensagem (nack)

def main():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    
    # Loop para tentar conectar ao RabbitMQ (útil em ambientes Docker)
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            channel = connection.channel()
            
            channel.queue_declare(queue='fila_denuncias', durable=True)
            print(' [*] Aguardando por denúncias. Para sair, pressione CTRL+C')

            # Define que este consumidor só pegará uma nova mensagem após terminar a atual
            channel.basic_qos(prefetch_count=1)
            
            channel.basic_consume(queue='fila_denuncias', on_message_callback=callback)
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Conexão com RabbitMQ falhou. Tentando novamente em 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print('Interrompido.')
            break

if __name__ == '__main__':
    main() 

    