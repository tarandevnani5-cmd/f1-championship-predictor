# 1. Use an official lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (optimizes Docker caching)
COPY requirements.txt .

# 4. Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your project folders into the container
# This copies app/, src/, templates/, data/, and models/
COPY . .

# 6. Generate mock data and Pre-train the model inside the container 
# This makes the build self-sufficient even if data/ is ignored by Git
RUN python generate_mock_data.py && python src/train_no_mlflow.py

# 7. Expose the port FastAPI will run on
EXPOSE 8000

# 8. Command to start the FastAPI server
# Note: we use 0.0.0.0 so it's accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]