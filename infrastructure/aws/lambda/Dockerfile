ARG PYTHON_VERSION=3.12
ARG BUILDPLATFORM=x86_64

FROM --platform=${BUILDPLATFORM} ghcr.io/astral-sh/uv:0.6.6 AS uv
FROM --platform=${BUILDPLATFORM} public.ecr.aws/lambda/python:${PYTHON_VERSION} AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

RUN dnf install -y findutils git && \
  dnf clean all && \
  rm -rf /var/cache/dnf

RUN --mount=from=uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv export --frozen --no-emit-workspace --no-dev --no-editable --extra lambda -o requirements.txt && \
  uv pip install -r requirements.txt --target /asset
WORKDIR /asset
RUN python -c "from rustac import DuckdbClient; client = DuckdbClient(install_extensions=True, extension_directory='/asset/duckdb-extensions'); client.execute('CREATE SECRET (TYPE S3, PROVIDER CREDENTIAL_CHAIN)')"
RUN find . -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[0-9]*//'); cp $f $n; done;
RUN find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
RUN find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf
RUN find . -type f -name '*.so*' -exec strip --strip-unneeded {} \;

FROM --platform=${BUILDPLATFORM} public.ecr.aws/lambda/python:${PYTHON_VERSION}
ENV TZ=UTC
WORKDIR ${LAMBDA_TASK_ROOT}
COPY --from=builder /asset ${LAMBDA_TASK_ROOT}
COPY infrastructure/aws/lambda/handler.py ${LAMBDA_TASK_ROOT}
CMD [ "handler.handler" ]
