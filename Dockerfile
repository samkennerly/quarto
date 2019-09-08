FROM python:3.7.4
LABEL description="Static website builder"
LABEL maintainer="samkennerly@gmail.com"

# Create project folder
ARG WORKDIR=/context
WORKDIR "${WORKDIR}"

# Install system packages
RUN apt-get -y update && \
    apt-get -y install gcc less tree vim zip

# Install Python packages
COPY ["requirements.txt","."]
RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

# Copy project files (use .dockerignore to exclude)
COPY [".","."]

CMD ["/bin/bash"]
