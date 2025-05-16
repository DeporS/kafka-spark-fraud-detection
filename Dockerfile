FROM python:3.13-slim

# Complete the packages needed to compile libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    libblas-dev \
    liblapack-dev \
    libpq-dev \
    build-essential \
    cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
