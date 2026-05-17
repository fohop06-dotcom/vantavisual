# Rockstar API Backend

Бэкенд для Rockstar Client с регистрацией, авторизацией, 2FA и восстановлением пароля.

## Стек

- Node.js + Express
- PostgreSQL (Railway)
- JWT для аутентификации
- bcrypt для хеширования паролей
- otplib для 2FA (Google Authenticator)
- nodemailer для отправки писем

## Деплой на Railway

### 1. Создай PostgreSQL базу на Railway

1. Зайди на [railway.app](https://railway.app)
2. Нажми **New Project** → **Deploy from GitHub repo**
3. Подключи свой репозиторий
4. Нажми **+ New** → **Database** → **PostgreSQL**
5. Railway создаст базу и автоматически добавит переменную `DATABASE_URL`

### 2. Настрой переменные окружения

В панели Railway перейди в **Variables** и добавь:

| Переменная | Описание | Пример |
|---|---|---|
| `DATABASE_URL` | URL базы данных (Railway добавит автоматически) | `postgresql://...` |
| `JWT_SECRET` | Секретный ключ для JWT | `my-super-secret-key-123` |
| `FRONTEND_URL` | URL твоего фронтенда | `https://rockstar.pub` |
| `EMAIL_HOST` | SMTP сервер | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP порт | `587` |
| `EMAIL_USER` | Твоя почта | `you@gmail.com` |
| `EMAIL_PASS` | Пароль приложения | `xxxx xxxx xxxx xxxx` |

### 3. Получи URL API

Railway выдаст домен вида `https://your-project.up.railway.app`

### 4. Обнови фронтенд

В файле `js/auth.js` замени строку:

```js
// Было:
const expectedBaseUrl = `${origin}/api/v1`;

// Стало (подставь свой URL):
const expectedBaseUrl = `https://your-project.up.railway.app/api/v1`;
```

Или в `signin.html` / `signup.html` добавь перед подключением `auth.js`:

```html
<script>
  window.API_BASE_URL = 'https://your-project.up.railway.app/api/v1';
</script>
```

## API Endpoints

| Метод | Путь | Описание |
|---|---|---|
| POST | `/api/v1/auth/signup` | Регистрация |
| POST | `/api/v1/authorization` | Вход |
| POST | `/api/v1/verify-2fa` | Проверка 2FA |
| POST | `/api/v1/recovery/password` | Восстановление пароля |
| GET | `/api/v1/account/details` | Данные аккаунта (нужен JWT) |
| GET | `/api/v1/health` | Проверка работы сервера |

## Локальный запуск

```bash
cd api
npm install
cp .env.example .env
# Заполни .env своими данными
npm run dev
```

## Структура БД

Таблица `users`:
- `id` — уникальный ID
- `login` — логин (уникальный)
- `email` — почта (уникальная)
- `password_hash` — хеш пароля
- `secret_2fa` — секрет для 2FA (опционально)
- `recovery_token` — токен восстановления пароля
- `recovery_expires` — срок действия токена
- `created_at` / `updated_at` — timestamps
