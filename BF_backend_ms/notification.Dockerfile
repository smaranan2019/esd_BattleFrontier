FROM python:3.8-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN pip install --no-cache-dir -r amqp.reqs.txt -r http.reqs.txt
COPY ./notification.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./notification.py" ]