#!/bin/bash

podman run \
        --detach \
        --restart=always \
        --publish=8501:8501 \
        --env=AZURE_OPENAI_SERVICE= \
        --env=AZURE_OPENAI_DEPLOYMENT= \
        --env=AZURE_OPENAI_API_VERSIONS= \
        --env=AZURE_OPENAI_API_KEY= \
        --env=AZURE_OPENAI_PROXY= \
        --name=openai-vision-ui \
        openai-vision-ui:20240101
