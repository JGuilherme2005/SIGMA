# servico-ia/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Comando para iniciar o consumidor quando o container rodar
CMD ["python", "consumer.py"]