FROM python:3.8-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./shipping.py ./
CMD [ "python", "./shipping.py" ]