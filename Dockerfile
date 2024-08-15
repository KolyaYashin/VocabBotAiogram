FROM python:slim

WORKDIR /home

RUN apt-get update && apt-get install -y git


RUN git clone https://github.com/KolyaYashin/VocabBotAiogram.git

WORKDIR /home/VocabBotAiogram

RUN pip install -r requirements.txt

COPY run.sh run.sh

RUN chmod +x /home/VocabBotAiogram/run.sh


ENTRYPOINT ["/home/VocabBotAiogram/run.sh"]

#ENTRYPOINT ["python3", "main.py"]