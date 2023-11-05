FROM python:3.10

# Define environment variable
ENV DATABASE_URL=postgresql://codetest:password@database/codetest 
ENV HOST=database
ENV DB=codetest
ENV USER=codetest
ENV PASSWORD=password

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
# COPY data ./data 
COPY main.py ./
# CMD ["python", "./main.py"]