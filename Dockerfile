FROM python:3.9

WORKDIR .

RUN python -m venv ./venvap

ENV PATH="/venvap/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY app ./app
#COPY createdb.sql ./
EXPOSE 80
EXPOSE 443
EXPOSE 4000

ENV UVICORN_HOST=0.0.0.0 UVICORN_PORT=[80,4000]
ENTRYPOINT ["python", "main.py"]

