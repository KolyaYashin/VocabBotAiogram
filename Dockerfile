FROM python:slim

WORKDIR /home

RUN apt-get update && apt-get install -y git


RUN git clone https://github.com/KolyaYashin/ai_vocab_bot.git

WORKDIR /home/ai_vocab_bot

RUN pip install -r requirements.txt

COPY run.sh run.sh

RUN chmod +x /home/ai_vocab_bot/run.sh


ENTRYPOINT ["/home/ai_vocab_bot/run.sh"]

#ENTRYPOINT ["python3", "main.py"]