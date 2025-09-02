# Imagem base Python, adaptada para o Dash e Gunicorn
FROM python:3.9-slim-buster

# Configurações de usuário (boa prática de segurança)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner e instala as dependências
COPY --chown=user ./requirements.txt requirements.txt

# Upgrade pip para garantir que a versão mais recente do instalador seja usada
RUN pip install --upgrade pip

# Desinstala qualquer versão existente de dash (e seus componentes internos como dash-table)
# O '|| true' garante que o comando não falhe o build se o pacote não estiver instalado
RUN pip uninstall -y dash || true && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Copia o restante do código da aplicação para o contêiner
COPY --chown=user . /app

# Comando que será executado quando o contêiner for iniciado
# Inicia o Gunicorn servindo o aplicativo Dash na porta 7860
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:7860"]
