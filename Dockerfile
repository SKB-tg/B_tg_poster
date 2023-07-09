FROM python:3.9

WORKDIR .

RUN python -m venv ./venvap

ENV PATH="/venvap/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY app ./app
#COPY createdb.sql ./

ENTRYPOINT ["python", "main.py"]

