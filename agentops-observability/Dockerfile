# ---- build stage ----
FROM python:3.11-slim AS builder

WORKDIR /app
COPY pyproject.toml ./
RUN pip install --upgrade pip \
 && pip install --no-cache-dir ".[dev]"

# ---- runtime stage ----
FROM python:3.11-slim AS runtime

# Run as non-root user
RUN useradd --no-create-home --shell /bin/false appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY api ./api
COPY database ./database
COPY domain ./domain
COPY adapters ./adapters
COPY workers ./workers
COPY migrations ./migrations
COPY alembic.ini ./

USER appuser

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
