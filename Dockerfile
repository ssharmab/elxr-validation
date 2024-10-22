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
    python-is-python3 \
    bc
RUN pip install pipx
RUN pip install --upgrade pip
RUN pipx install poetry
RUN git config --global --add safe.directory /workspaces/elxr-validation/.git/modules/elxr_validator/inline
RUN ln -s /root/.local/bin/poetry /usr/local/bin/poetry
WORKDIR /workspaces/elxr-validation
COPY dist/elxr_validator-0.1.0-py3-none-any.whl /workspaces/elxr-validation
RUN bash -c "pip install elxr_validator-0.1.0-py3-none-any.whl"
