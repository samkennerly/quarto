FROM python:3.6.9
LABEL description="Python development sandbox"
LABEL maintainer="samkennerly@gmail.com"

# Create project folder
ARG WORKDIR=/context
WORKDIR "${WORKDIR}"

# Install system packages
RUN apt-get -y update && apt-get -y install \
    tidy=2:5.6.0-10

# Install Python packages
RUN pip install --upgrade pip && pip install \
    black==19.3b0 \
    Cython==0.29.13 \
    mistune==0.8.4

CMD ["/bin/bash"]
