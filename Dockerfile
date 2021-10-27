from surnet/alpine-wkhtmltopdf:3.13.5-0.12.6-small

RUN apk add --update --no-cache python3 py3-pip \
    && ln -sf python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ./app.sh
