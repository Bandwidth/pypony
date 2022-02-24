# Action will be run in a python3 container
FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt setup.py ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy setup.py and our module
COPY  ./api_validator ./api_validator

RUN pip install -e .

# Run the python code
CMD ["python", "-m", "api_validator"]
