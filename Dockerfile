FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /build

# Create an isolated virtual environment
RUN python -m venv "$VIRTUAL_ENV"

COPY requirements.txt .

# Install dependencies into the virtual environment
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

    RUN pip install --no-cache-dir -r requirements.txt

# pip is only needed during the build.
RUN rm -rf \
    "$VIRTUAL_ENV/lib/python3.12/site-packages/pip" \
    "$VIRTUAL_ENV/lib/python3.12/site-packages/pip-"*.dist-info \
    "$VIRTUAL_ENV/bin/pip" \
    "$VIRTUAL_ENV/bin/pip3" \
    "$VIRTUAL_ENV/bin/pip3.12"

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /myapp

# Create a dedicated non-root user
RUN groupadd --system --gid 10001 app \
    && useradd --system \
       --uid 10001 \
       --gid 10001 \
       --home-dir /myapp \
       --no-create-home \
       app

# Copy only the runtime dependencies from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application
COPY --chown=app:app src/ ./src/

# Make sure the application directory belongs to the app user
RUN chown -R app:app /myapp

USER 10001:10001

EXPOSE 5004

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5004"]
