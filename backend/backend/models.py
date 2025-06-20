# backend/models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
import datetime

# Substitua com as suas variáveis de ambiente do docker-compose.yml
DATABASE_URL = "postgresql://sigma:sigma_password@localhost:5432/sigma_db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Denuncia(Base):
    __tablename__ = 'denuncias'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    tipo = Column(String(50)) # ex: 'buraco_na_via', 'iluminacao_falha', 'aglomeracao'
    descricao = Column(Text, nullable=True)
    status = Column(String(50), default='recebido')
    
    # O campo mais importante para PostGIS: armazena latitude e longitude
    # O 'srid=4326' é o sistema de coordenadas padrão (WGS 84)
    localizacao = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

# Para criar a tabela no banco de dados na primeira vez que rodar
Base.metadata.create_all(bind=engine)