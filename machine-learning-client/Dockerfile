FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

EXPOSE 5001

CMD ["python", "speech_to_text.py"]
