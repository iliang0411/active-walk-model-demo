FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY assets ./assets
COPY demo_data ./demo_data
COPY .streamlit ./.streamlit

EXPOSE 8501

CMD ["streamlit", "run", "app/demo_ui.py", "--server.address=0.0.0.0", "--server.port=8501"]