FROM python:3.12-bookworm
RUN apt-get update
RUN apt-get install -y \
    git \
    python3-guestfs \
    libguestfs-tools
RUN pip install pipx
RUN pipx install poetry
RUN ln -s /root/.local/bin/poetry /usr/local/bin/poetry





