FROM python:3.14-slim
ARG APPLICATION_SERVER_PORT=8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/ \
    VIRTUAL_ENVIRONMENT_PATH="/src/.venv" \
    APPLICATION_SERVER_PORT=$APPLICATION_SERVER_PORT

ENV PATH="$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

WORKDIR ${PYTHONPATH}

COPY ./requirements/prod.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./src /src
EXPOSE ${APPLICATION_SERVER_PORT}
CMD ["uvicorn", "--workers", "1", "--host", "0.0.0.0", "--port", "8000", "src.main:app"]
