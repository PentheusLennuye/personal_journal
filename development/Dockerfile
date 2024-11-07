ARG ALPINE_VER="3.20"
ARG PYTHON_VER="3.12"
FROM python:${PYTHON_VER}-alpine${ALPINE_VER}

RUN apk --update --no-progress --no-cache upgrade && \
    apk --no-progress --virtual .build-deps add pipx
RUN apk --update --no-progress add postgresql-client

# This application runs as non-root --------------------------------------
RUN addgroup -S appgroup && adduser -G appgroup -S appuser -u 1000
RUN [ -d /app ] || mkdir /app
RUN chown -R appuser:appgroup /app
USER appuser

# Install dependencies ----------------------------------------------------
WORKDIR /tmp
ENV PATH="/home/appuser/.local/bin:$PATH"
RUN pipx install --include-deps poetry poetry-plugin-export
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry config warnings.export false && \
    poetry export --with=dev --output=requirements.txt && \
    python -m pip install -r requirements.txt

# Clean up the build deps ------------------------------------------------
USER root
RUN apk del .build-deps

# Set the entrypoint -----------------------------------------------------
COPY development/entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

# Run the application as non-root -----------------------------------------
WORKDIR /app
USER appuser
CMD ["/opt/entrypoint.sh"]
