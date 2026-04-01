#!/bin/bash

# Exit on error
set -e

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install streamlit pandas matplotlib

echo "Starting Streamlit app..."
streamlit run app.py \
    --server.port 6368 \
    --server.baseUrlPath /wicktheory \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false
