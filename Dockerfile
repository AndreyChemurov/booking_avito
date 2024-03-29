FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN mkdir -p app
WORKDIR app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .