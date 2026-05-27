FROM python:3.11.9-slim-bookworm

WORKDIR /app

COPY . .

RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

CMD ["python", "-m", "devops_toolkit.cli", "--root", ".", "--strict"]
