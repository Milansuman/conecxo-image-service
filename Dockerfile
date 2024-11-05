FROM python:3

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["fastapi", "run", "server.py"]

EXPOSE 8000