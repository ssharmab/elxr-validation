FROM python:3.11-bookworm AS elxr-container
RUN apt update
RUN apt install -y \ 
    git \
    python3-guestfs \
    libguestfs-tools \
    libguestfs-dev \
    vim \
    pipenv \
    curl wget net-tools \
    python-is-python3
RUN pip install pipx
RUN pip install --upgrade pip
RUN pipx install poetry
RUN ln -s /root/.local/bin/poetry /usr/local/bin/poetry
WORKDIR /workspaces/elxr-validation