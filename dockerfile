FROM python:3.9.7 

WORKDIR /usr/src/app 

COPY requirements.txt ./ 

RUN apt-get update && apt-get install -y build-essential && pip install --no-cache-dir -r requirements.txt 

COPY . . 

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]