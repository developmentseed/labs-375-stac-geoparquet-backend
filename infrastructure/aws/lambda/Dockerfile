ARG PYTHON_VERSION=3.12

FROM ghcr.io/astral-sh/uv:0.6.6 AS uv
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION} AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy
ENV PATH="/root/.cargo/bin:${PATH}"
ENV MATURIN_PEP517_ARGS="--features=duckdb-bundled"

# TODO Remove rustup, gcc, and g++ when we go back to using stacrs wheels
RUN dnf install -y findutils binutils git gcc g++ && \
  dnf clean all && \
  rm -rf /var/cache/dnf
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y 

RUN --mount=from=uv,source=/uv,target=/bin/uv \
  --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv export --frozen --no-emit-workspace --no-dev --no-editable --extra lambda -o requirements.txt && \
  uv pip install -r requirements.txt --target /asset
WORKDIR /asset
RUN python -c "from stacrs import DuckdbClient; DuckdbClient(use_s3_credential_chain=True, use_azure_credential_chain=False, install_extensions=True, extension_directory='/asset')"
RUN find . -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[0-9]*//'); cp $f $n; done;
RUN find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
RUN find . -type f -a -name '*.py' -print0 | xargs -0 rm -f
RUN find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf
RUN find . -type f -name '*.so*' -exec strip --strip-unneeded {} \;

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}
WORKDIR /asset
COPY --from=builder /asset /asset
COPY infrastructure/aws/lambda/handler.py /asset/handler.py
