from python:slim-bullseye

WORKDIR /usr/src/app

RUN apt update && apt install -y wkhtmltopdf

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./app.sh" ]
