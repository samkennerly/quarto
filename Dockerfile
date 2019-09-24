FROM python:3.7.4
LABEL description="Python development sandbox"
LABEL maintainer="samkennerly@gmail.com"

# Create project folder
ARG WORKDIR=/context
WORKDIR "${WORKDIR}"

# Install system packages
RUN apt-get -y update && apt-get -y install \
    less tree

# Install Python packages
RUN pip install --upgrade pip && pip install \
    black

CMD ["/bin/bash"]
