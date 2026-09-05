# ============================================================================
# Multi-stage Dockerfile for Ren'Py Web Build
# Builds the "Чистый берег" visual novel as a browser-playable WASM app
#
# Usage:
#   docker compose up --build        # Build & run on http://localhost:8080
#   docker compose up --build -d     # Detached mode
# ============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Build the Ren'Py web version
# ---------------------------------------------------------------------------
FROM --platform=linux/amd64 python:3.12-slim AS builder

ARG RENPY_VERSION=8.5.3
ARG RENPY_DL=https://www.renpy.org/dl/${RENPY_VERSION}

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl bzip2 xz-utils libgl1 libglib2.0-0 p7zip-full \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# Download and extract Ren'Py SDK
RUN curl -fSL "${RENPY_DL}/renpy-${RENPY_VERSION}-sdk.tar.bz2" \
        -o renpy-sdk.tar.bz2 \
    && tar xjf renpy-sdk.tar.bz2 \
    && rm renpy-sdk.tar.bz2 \
    && mv renpy-${RENPY_VERSION}-sdk renpy

# Download and install Web (WASM) support into the SDK
RUN curl -fSL "${RENPY_DL}/renpy-${RENPY_VERSION}-web.zip" \
        -o renpy-web.zip \
    && cd /opt/renpy && 7z x /opt/renpy-web.zip -y \
    && rm /opt/renpy-web.zip

# Copy the game project
COPY . /project

# Remove compiled caches, saves, and duplicate images
RUN rm -rf /project/game/cache /project/game/saves /project/images

# Build the web version
RUN cd /opt/renpy \
    && ./renpy.sh launcher web_build /project --destination /output

# ---------------------------------------------------------------------------
# Stage 2: Patch the generated HTML — remove hamburger menu, customize loading
# ---------------------------------------------------------------------------
FROM --platform=linux/amd64 python:3.12-slim AS patcher

COPY --from=builder /output /output
COPY patch_html.py /patch_html.py

RUN python3 /patch_html.py /output

# ---------------------------------------------------------------------------
# Stage 3: Serve with Nginx
# ---------------------------------------------------------------------------
FROM nginx:alpine AS runtime

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built and patched web files
COPY --from=patcher /output /tmp/output

# Move web build files to nginx html root
RUN BUILD_DIR=$(find /tmp/output -name "index.html" -exec dirname {} \; | head -1) \
    && if [ -z "$BUILD_DIR" ]; then echo "ERROR: No index.html found in build output" && exit 1; fi \
    && cp -r "${BUILD_DIR}"/* /usr/share/nginx/html/ \
    && rm -rf /tmp/output

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
