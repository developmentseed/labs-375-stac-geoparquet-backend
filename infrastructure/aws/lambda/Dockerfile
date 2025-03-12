ARG PYTHON_VERSION=3.12

FROM ghcr.io/astral-sh/uv:0.6.6 AS uv
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

RUN dnf install -y git && \
  dnf clean all && \
  rm -rf /var/cache/dnf

RUN --mount=from=uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
  uv pip install -r requirements.txt --target /asset

WORKDIR /asset
COPY infrastructure/aws/lambda/handler.py /asset/handler.py
