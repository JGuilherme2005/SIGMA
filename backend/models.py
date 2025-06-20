# models.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

# Modelo para o que o cidadão envia via PWA/WhatsApp
class CitizenReportInput(BaseModel):
    description: str = Field(..., example="Buraco perigoso na via em frente ao número 123.")
    latitude: float = Field(..., example=-23.550520)
    longitude: float = Field(..., example=-46.633308)
    media_url: Optional[str] = Field(None, example="https://storage.sig.ma/media/foto123.jpg")

# Modelo para a predição da IA
class IAPrediction(BaseModel):
    risk_level: Literal["baixo", "médio", "alto", "crítico"]
    category: Literal["desordem_urbana", "violencia", "acidente_transito", "saude", "desastre_natural"]
    suggested_action: str = Field(..., example="Acionar equipe de manutenção da prefeitura")

# Modelo completo de um Alerta, armazenado no nosso "banco de dados"
class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    status: Literal["novo", "em_atendimento", "resolvido", "fechado"] = "novo"
    report: CitizenReportInput
    prediction: IAPrediction
