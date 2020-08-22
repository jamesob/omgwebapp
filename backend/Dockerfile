FROM python:3.8

WORKDIR /app
COPY docker_entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && mkdir /pycache
COPY . .
RUN pip install -r requirements.txt && pip install -e .
ENTRYPOINT ["/entrypoint.sh"]
