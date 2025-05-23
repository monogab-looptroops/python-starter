# Use a (minimal) python image, e.g. release 3.12
FROM python:3.12-slim AS base


RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /src

# Copy requirements
COPY ./requirements.txt /tmp/

# Define the build argument
ARG AZURE_ARTIFACTS_PYTHON_PAT

# Use the argument to set an environment variable
ENV AZURE_ARTIFACTS_PYTHON_PAT=${AZURE_ARTIFACTS_PYTHON_PAT}

# Install dependencies from the requirements files
# -r specifies the requirements file to install from
RUN pip install -U pip && \
    pip install keyring keyrings.google-artifactregistry-auth && \
    pip install --extra-index-url https://${AZURE_ARTIFACTS_PYTHON_PAT}@pkgs.dev.azure.com/clareboutpotatoes/e8f3797a-daa7-473a-aa9a-611e9ec8916b/_packaging/PlantApplicationsPythonPackages/pypi/simple/ -r /tmp/requirements.txt && \
    rm -rf /tmp/*


ARG IMAGE_TAG
ENV IMAGE_TAG=${IMAGE_TAG}

# Copy the source code into the image
COPY ./src ./src

# Set environment variables
# - PYTHONUNBUFFERED disables output buffering so logs are written immediately
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION python
ENV PYTHONUNBUFFERED 1


FROM base AS development

# Copying inside the certificates is mainly for testing. 
# It will be overwritten with the secrets mounted in the docker-compose file
#
RUN if [ -f ./certificates ]; then \
    cp -r ./certificates ./certificates; \
fi

# Install additional packages for development
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    nano \
    iputils-ping \
    curl \
    git \
    && curl -fsSL https://code-server.dev/install.sh | sh \
    && code-server --install-extension ms-python.python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp

CMD ["tail", "-f", "/dev/null"]

FROM base AS production

CMD ["python", "src/main.py"]