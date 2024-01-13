# Use a imagem oficial do Python 3.11.4
FROM python:3.11.4

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos necessários para o aplicativo
COPY api.py /app/api.py
COPY requirements.txt /app/requirements.txt

# Instale as dependências usando o pip
RUN pip install -r requirements.txt

# Defina a porta a ser usada pelo aplicativo
ENV PORT=8000

# Exponha a porta
EXPOSE 8000

# Comando para executar o aplicativo
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]