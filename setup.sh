#!/bin/bash

# Create required directories
mkdir -p uploads logs

# Set permissions
chmod 755 uploads logs

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
flask db init
flask db migrate
flask db upgrade

echo "Setup complete! Run 'flask run' to start the development server."
