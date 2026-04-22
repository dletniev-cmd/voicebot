# 🎙 Voice Transcription Bot

Telegram-бот, который автоматически расшифровывает голосовые сообщения и видео-кружки
в группах и личных чатах. Использует Whisper large-v3 через Groq API — бесплатно и точно.

## Возможности

- 🎙 Расшифровка голосовых сообщений
- 🎥 Расшифровка видео-кружков
- 🌍 ~100 языков (автоматическое определение)
- ✍️ Пунктуация и форматирование
- 👥 Работает в группах и личных чатах
- ⚡ Ответ в виде reply на оригинальное сообщение

## Быстрый старт

### 1. Получи токены

**Telegram Bot Token:**
1. Открой [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot` и следуй инструкциям
3. Скопируй токен вида `123456789:AAF...`

> **Важно для групп:** в BotFather отправь `/mybots` → выбери бота →
> `Bot Settings` → `Group Privacy` → **отключи** (Disabled).
> Без этого бот не будет видеть сообщения в группах.

**Groq API Key (бесплатно):**
1. Зарегистрируйся на [console.groq.com](https://console.groq.com)
2. Перейди в API Keys → Create API Key
3. Скопируй ключ

### 2. Установка

```bash
git clone <repo>
cd voice_bot

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Конфигурация

```bash
cp .env.example .env
# Отредактируй .env — вставь свои токены
```

### 4. Запуск

```bash
python bot.py
```

## Добавление в группу

1. Добавь бота в группу как обычного участника
2. **Обязательно:** отключи Group Privacy (см. шаг выше)
3. Бот сразу начнёт расшифровывать голосовые и кружки

## Лимиты Groq (бесплатный тир)

| Ограничение | Значение |
|-------------|----------|
| Минут аудио в день | 2,000 мин (33+ часа) |
| Запросов в минуту | 20 |
| Файл | до 25 МБ |

Для среднестатистической группы этого более чем достаточно.

## Деплой на сервер

```bash
# systemd сервис
sudo nano /etc/systemd/system/voice-bot.service
```

```ini
[Unit]
Description=Voice Transcription Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/voice_bot
ExecStart=/home/ubuntu/voice_bot/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable voice-bot
sudo systemctl start voice-bot
```
