from python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add --no-cache wkhtmltopdf
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./app.sh" ]
