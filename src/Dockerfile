FROM python:3.11.4-slim

ENV HY_API_PORT=80
EXPOSE $HY_API_PORT

WORKDIR /api
COPY speer-notes/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY speer-notes .

CMD ["python", "run.py"]
