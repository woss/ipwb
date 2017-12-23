# Use Python 2.7 as default, but facilitate change at build time
ARG     PYTHON_TAG=2.7
FROM    python:${PYTHON_TAG}

ARG     IPFS_VERSION=v0.4.13

# Add some metadata
LABEL   app.name="InterPlanetary Wayback (IPWB)" \
        app.description="A distributed and persistent archive replay system using IPFS" \
        app.license="MIT License" \
        app.license.url="https://github.com/oduwsdl/ipwb/blob/master/LICENSE" \
        app.repo.url="https://github.com/oduwsdl/ipwb" \
        app.authors="Mat Kelly <@machawk1> and Sawood Alam <@ibnesayeed>"

# Download and install IPFS
RUN     cd /tmp \
        && wget https://dist.ipfs.io/go-ipfs/v0.4.13/go-ipfs_${IPFS_VERSION}_linux-amd64.tar.gz \
        && tar xvfz go-ipfs*.tar.gz \
        && mv go-ipfs/ipfs /usr/local/bin/ipfs \
        && rm -rf go-ipfs* \
        && ipfs init

# Make necessary changes to prepare the environment for IPWB
RUN     apt update && apt install -y locales \
        && rm -rf /var/lib/apt/lists/* \
        && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
        && locale-gen

# Copy source files and install IPWB
WORKDIR /ipwb
COPY    requirements.txt ./
RUN     pip install -r requirements.txt
COPY    . ./
RUN     python setup.py install
RUN     mkdir /indexes

# Add an environment variable and populate it with the default sample
ENV     WARCS_PATH=ipwb/samples/warcs/salam-home.warc

# Run ipfs daemon in background
# Wait for the daemon to be ready
# Index WARCs from the WARCS_PATH environment variable
# Replay using the newly created index
CMD     ipfs daemon & \
        while ! curl -s localhost:5001 > /dev/null; do sleep 1; done \
        && ipwb index $WARCS_PATH > /indexes/index.cdxj \
        && ipwb replay /indexes/index.cdxj
