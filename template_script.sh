#!/bin/bash

export AZURE_OPENAI_SERVICE=
export AZURE_OPENAI_DEPLOYMENT=
export AZURE_OPENAI_API_VERSION=2024-02-15-preview
export AZURE_OPENAI_API_KEY=
export AZURE_OPENAI_PROXY=

streamlit run src/vision-ui.py \
    --browser.gatherUsageStats=false \
    --server.maxUploadSize 20
