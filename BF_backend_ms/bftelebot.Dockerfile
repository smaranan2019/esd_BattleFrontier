FROM python:3.8-slim
WORKDIR /usr/src/app
COPY tele.reqs.txt ./
RUN pip install --no-cache-dir -r tele.reqs.txt
COPY ./BFTeleBot.py ./
CMD [ "python", "./BFTeleBot.py" ]