ARG PYTHON_VERSION=3.12

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install required utilities
RUN dnf install -y findutils binutils git && \
  dnf clean all && \
  rm -rf /var/cache/dnf

WORKDIR /tmp
COPY uv.lock uv.lock
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY src/ src/

RUN uv export --frozen --extra lambda > requirements.txt && \
  uv pip install --compile-bytecode --target ${LAMBDA_TASK_ROOT} -r requirements.txt

# Reduce package size and remove useless files
WORKDIR ${LAMBDA_TASK_ROOT}
RUN find . -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[0-9]*//'); cp $f $n; done;
RUN find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
RUN find . -type f -a -name '*.py' -print0 | xargs -0 rm -f
RUN find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf

# Strip debug symbols from compiled C/C++ code
RUN find . -type f -name '*.so*' -exec strip --strip-unneeded {} \;

COPY infrastructure/aws/lambda/handler.py ${LAMBDA_TASK_ROOT}/handler.py
