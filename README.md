# VocabBotAiogram

Ссылка - t.me/VocabTrainingBot

• Телеграм бота для помощи при изучении новых слов английского языка. При создании использовал
Telegram API и возможности библиотеки Aiogram. Для сохранения словаря
пользователя я использовал базу данных SQLite. А чтобы бот был активен, я
задеплоил его на виртуальный сервер
от RuVDS.
Возможности бота:
- Пользователь может вводить слова на
английском и их перевод, и они сохра
няться в его словаре
- Можно проводить тесты по своим
словам, чтобы лучше их запомнить
(учитывается насколько давно пользователь вспоминал конкретное слово)


• Стэк технологий - Aiogram3, SQLite

Для запуска у вас должны быть заданы переменные окружения MY_TG_ID и TOKEN_VOCAB

Инструкция по запуску:

Сначала скачайте docker: sudo apt install docker

Скачайте образ через команду: docker pull kolya364/ai_vocab_bot:1

Создайте место для хранения данных на хосте: docker volume create vocab_data

Задайте переменные окружения командами:
export MY_TG_ID="your telegram id"
export TOKEN_VOCAB="API token of your bot"

Запуск контейнера: docker run -d -e TOKEN_VOCAB=$TOKEN_VOCAB -e MY_TG_ID=$MY_TG_ID -v vocab_data:/home/VocabBotAiogram/data --name bot kolya364/ai_vocab_bot:1
