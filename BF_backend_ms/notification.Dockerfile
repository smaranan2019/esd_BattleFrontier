FROM python:3.8-slim
WORKDIR /usr/src/app
COPY amqp.reqs.txt tele.reqs.txt ./
RUN pip install --no-cache-dir -r amqp.reqs.txt -r tele.reqs.txt
COPY ./notification.py ./amqp_setup.py ./
CMD [ "python", "./notification.py" ]