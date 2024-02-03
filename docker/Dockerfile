FROM condaforge/mambaforge:latest

ENV DEBIAN_FRONTEND=noninteractive 

SHELL ["bash", "-c"]

RUN apt-get update -q && apt-get install -q -y --no-install-recommends \
    libgl1-mesa-dev libglu1 libxinerama1 libxft-dev libxcursor1  node-less \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN ./install_onelab_prebuilt.sh Linux /opt/onelab/bin stable

ENV PATH /opt/onelab/bin:$PATH

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
