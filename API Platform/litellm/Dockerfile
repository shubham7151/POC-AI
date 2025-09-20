FROM ghcr.io/berriai/litellm:main-v1.72.2-stable

WORKDIR /app

COPY config.yaml .

RUN chmod +x ./docker/entrypoint.sh

EXPOSE 4000/tcp

# CMD ["--port", "4000", "--config", "config.yaml", "--detailed_debug"]
CMD ["litellm", "--port", "4000", "--config", "config.yaml", "--detailed_debug"]
