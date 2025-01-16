# Use a Python image with UV pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Enable caching for performance optimization
ENV UV_LINK_MODE=copy

# Install the project dependencies using UV
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the project files
ADD . /app

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Set the environment PATH to include the virtual environment executables
ENV PATH="/app/.venv/bin:$PATH"

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Expose the Django development server port
EXPOSE 8000

# Reset the entrypoint (do not invoke `uv` automatically)
ENTRYPOINT []

# Run Django's development server with ASGI for Channels (instead of WSGI)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "myproject.asgi:application"]
