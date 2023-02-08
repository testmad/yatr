FROM python:3.8-slim

# Expose a port
EXPOSE 8787

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV YATR_MODULE_PATH=/terraform/modules

WORKDIR /app
COPY . /app

RUN python -m pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8787", "--timeout", "600", "app.app:app"]
