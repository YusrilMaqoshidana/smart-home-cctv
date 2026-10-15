FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY services /app/services

EXPOSE 8000

CMD ["python3", "-m", "services.web_dashboard.app"]
