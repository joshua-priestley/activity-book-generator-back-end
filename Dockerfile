from python:slim-bullseye

WORKDIR /usr/src/app

RUN apt update \
  && apt install --no-install-recommends -y wget \
  && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
  && apt install --no-install-recommends -y ./wkhtmltox_0.12.6-1.buster_amd64.deb

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./app.sh" ]
