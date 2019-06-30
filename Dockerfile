FROM python:3.7.3-alpine3.10

WORKDIR /usr/src/geocoding-proxy

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "./server.py" ]