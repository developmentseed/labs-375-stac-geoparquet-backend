ARG PYTHON_VERSION=3.12

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install required utilities
RUN dnf install -y findutils binutils && \
  dnf clean all && \
  rm -rf /var/cache/dnf

WORKDIR /tmp
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY src/stac_fastapi/ src/stac_fastapi/

RUN uv pip install --compile-bytecode .[lambda] --target /asset --no-binary pydantic

# Reduce package size and remove useless files
WORKDIR /asset
RUN find . -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[0-9]*//'); cp $f $n; done;
RUN find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
RUN find . -type f -a -name '*.py' -print0 | xargs -0 rm -f
RUN find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf
RUN rm -rdf /asset/numpy/doc/ /asset/boto3* /asset/botocore* /asset/bin /asset/geos_license /asset/Misc

# Strip debug symbols from compiled C/C++ code (except for numpy.libs!)
RUN find . -type f -name '*.so*' \
  -not -path "./numpy.libs/*" \
  -exec strip --strip-unneeded {} \;

COPY infrastructure/aws/lambda/handler.py /asset/handler.py

CMD ["echo", "hello world"]

