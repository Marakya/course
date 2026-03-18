# 🚀 Telegram Bot 

## 📘 Описание проекта

Telegram‑бот, поддерживающий два режима работы:

* **main.py** — интеграция с Яндекс‑агентом
* **app.py** — интеграция с Langflow

Проект полностью контейнеризован и запускается в один шаг через Docker.

---

## 📦 Требования

### 🔧 Обязательные

* **Docker** — основной инструмент для запуска проекта.
  Скачать можно здесь:
  [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

### 🖥️ Опциональные

* **VS Code** — удобный редактор для работы с репозиторием.
  Можно использовать любой терминал.

---

## ⚙️ Установка и запуск локально

### **1. Клонируйте репозиторий**

```bash
git clone https://github.com/Marakya/course
```

### **2. Перейдите в директорию проекта**

```bash
cd course
```

### **3. Создайте файл `.env`**

```bash
cp .env.example .env
```

Заполните все параметры: токен Telegram‑бота, ключи сервисов и другие настройки.

---

## 🐳 Запуск через Docker

### 🔄 Выбор режима работы

В проекте доступно два скрипта:

* `main.py` — Яндекс‑агент
* `app.py` — Langflow

В файле **Dockerfile** в самом конце выберите нужный вариант запуска — раскомментируйте одну строку с `CMD`.

---

### **4. Соберите Docker‑контейнер**

```bash
docker build -t telegram-bot .
```

### **5. Запустите контейнер**

```bash
docker run --name telegram-bot --rm -p 8000:8000 telegram-bot
```

Бот запустится автоматически. Теперь можно открыть Telegram и начать с ним диалог.

---

## Отправить образ на DockerHub

Авторизоваться в DockerHub:
```bash
docker login
```

Ввести данные:
```bash
Username: user
Password: <пароль или access token>
```

Создать в DockerHub репозиторий, например с именем mybot и запустить сборку (user - ваше имя пользователя на DockerHub):
```bash
docker build -t user/mybot .
```

Отправить образ в DockerHub:
```bash
docker push user/mybot:latest
```

Если же необходимо взять готовый образ/или ваш:
```bash
docker pull user/mybot:latest
```

Запуск контейнера:
```bash
docker run user/mybot:latest
```

## ☁️ Развёртывание на виртуальной машине (например, Яндекс Облако)

Чтобы запустить бота на сервере:

1. Арендуйте виртуальную машину (VPS/VM) — например яндекс облако 
Инстуркция по подключению к Яндекс - https://yandex.cloud/ru/docs/tutorials/infrastructure-management/run-docker-on-vm/console#create-vm
2. Повторите те же шаги, что и для локальной установки:

   * Установите Docker
   * Клонируйте репозиторий
   * Создайте `.env`
   * Соберите контейнер
   * Запустите командой:

     ```bash
     docker run --name telegram-bot --rm -p 8000:8000 telegram-bot
     ```

После запуска бот будет работать постоянно, пока запущен контейнер.




