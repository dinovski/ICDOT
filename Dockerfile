# Build Stage
FROM python:3.10-slim-buster as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip wheel

COPY requirements.txt .
RUN pip install -r requirements.txt


# Final Stage
FROM python:3.10-slim-buster

COPY --from=builder /opt/venv /opt/venv
COPY . /app

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000

CMD ["gunicorn", "--reload", "-n", "BHOT-PROD", "-b", ":5010", "--access-logfile", "-", "--error-logfile", "-", "bhot_runner:app"]
