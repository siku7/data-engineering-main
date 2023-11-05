FROM python:3.10


EXPOSE 8000

# Define environment variable
ENV DATABASE_URL=postgresql://codetest:password@database/codetest 

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY data ./data 
COPY main.py ./
