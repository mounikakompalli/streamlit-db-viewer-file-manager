# ============================================================
# Dockerfile - Streamlit App Container
# Stage 3: Defines how Docker builds the Python app image
# ============================================================

# Step 1: Start from an official lightweight Python 3.11 image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
#         All subsequent commands run from /app
WORKDIR /app

# Step 3: Copy requirements.txt first (before app code)
#         This is a Docker best practice — if requirements don't change,
#         Docker reuses the cached layer and skips re-installing packages
COPY requirements.txt .

# Step 4: Install all Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the Streamlit app code into the container
COPY app.py .

# Step 6: Create directories for file import functionality
#         /app/uploads    = source directory (mounted from your Mac)
#         /app/imported_files = target directory (where files land after import)
RUN mkdir -p /app/uploads /app/imported_files

# Step 7: Tell Docker this container listens on port 8501
EXPOSE 8501

# Step 8: The command that runs when the container starts
#         --server.port=8501       = use port 8501
#         --server.address=0.0.0.0 = accept connections from outside the container
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
