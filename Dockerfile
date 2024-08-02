FROM python:slim

WORKDIR /home

RUN apt-get update && apt-get install -y git sqlite3


RUN git clone https://github.com/KolyaYashin/VocabBotAiogram.git

WORKDIR /home/VocabBotAiogram

RUN pip install -r requirements.txt


ENTRYPOINT ["python3", "main.py"]