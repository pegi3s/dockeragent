FROM pegi3s/docker:29.0.1

# 1. Install System Tools, GitHub CLI & Python
RUN apt-get update && apt-get install -y curl git jq procps python3 wget zip tar\
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# 2. Install OpenCode
RUN curl -fsSL https://opencode.ai/install | bash

ENV PATH="/root/.opencode/bin:/usr/local/bin:${PATH}"

# 3. Setup Config
RUN mkdir -p /root/.config/opencode
COPY opencode.json /root/.config/opencode/opencode.json
COPY instructions.md /root/.config/opencode/instructions.md
COPY instructions_r.md /root/.config/opencode/instructions_r.md
COPY instructions_nextflow.md /root/.config/opencode/instructions_nextflow.md
COPY instructions_jupyter.md /root/.config/opencode/instructions_jupyter.md
COPY instructions_form.md /root/.config/opencode/instructions_form.md
COPY setup_config.py /setup_config.py
COPY entrypoint.sh /entrypoint.sh

# 4. Entrypoint — fills in opencode.json at runtime from /data/config.json and /usr/.apikey
RUN chmod +x /entrypoint.sh

WORKDIR /data
ENTRYPOINT ["/entrypoint.sh"]
