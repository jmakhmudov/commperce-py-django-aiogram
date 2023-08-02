FROM python:latest

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini.asc /tini.asc
RUN gpg --batch --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 595E85A6B1B4779EA4DAAEC70B588DFF0527A9B7 \
 && gpg --batch --verify /tini.asc /tini
RUN chmod +x /tini

WORKDIR /tgbot

COPY ./requirements.txt /tgbot/requirements.txt

RUN pip install -r /tgbot/requirements.txt

COPY ./entrypoint.sh /docker-entrypoint.sh
RUN chmod +x "/docker-entrypoint.sh"

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./tgbot.sh /tgbot.sh
RUN chmod +x /tgbot.sh

COPY . .

ENTRYPOINT ["/tini", "--", "/docker-entrypoint.sh"]
