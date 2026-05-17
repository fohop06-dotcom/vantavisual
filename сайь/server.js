require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 8081;
const path = require('path');

// Serve static files (frontend)
app.use((req, res, next) => {
  if (req.path !== '/' && !req.path.includes('.') && !req.path.startsWith('/api/')) {
    req.url = req.url + '.html';
  }
  next();
});
app.use(express.static(__dirname));

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || '*',
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// PostgreSQL pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

// Initialize database
const initDB = async () => {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        login VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        secret_2fa VARCHAR(255) DEFAULT NULL,
        recovery_token VARCHAR(255) DEFAULT NULL,
        recovery_expires TIMESTAMP DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('Database initialized');
  } catch (err) {
    console.error('Database init error:', err);
  }
};

initDB();

// Generate JWT token
const generateToken = (userId, login) => {
  return jwt.sign(
    { userId, login },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
};

// ===== REGISTRATION =====
app.post('/api/v1/auth/signup', async (req, res) => {
  try {
    const { login, email, password } = req.body;

    if (!login || !email || !password) {
      return res.status(400).json({ error: 'Все поля обязательны' });
    }

    if (password.length < 6) {
      return res.status(400).json({ error: 'Пароль должен быть минимум 6 символов' });
    }

    const existingUser = await pool.query(
      'SELECT id FROM users WHERE login = $1 OR email = $2',
      [login, email]
    );

    if (existingUser.rows.length > 0) {
      return res.status(409).json({ error: 'Логин или почта уже заняты' });
    }

    const saltRounds = 10;
    const passwordHash = await bcrypt.hash(password, saltRounds);

    const result = await pool.query(
      'INSERT INTO users (login, email, password_hash) VALUES ($1, $2, $3) RETURNING id, login, email',
      [login, email, passwordHash]
    );

    const user = result.rows[0];
    const token = generateToken(user.id, user.login);

    res.status(201).json({
      success: true,
      message: 'Регистрация успешна',
      token,
      data: {
        id: user.id,
        login: user.login,
        email: user.email
      }
    });
  } catch (err) {
    console.error('Signup error:', err);
    res.status(500).json({ error: 'Ошибка сервера при регистрации' });
  }
});

// ===== AUTHORIZATION =====
app.post('/api/v1/authorization', async (req, res) => {
  try {
    const { statement, password } = req.body;

    if (!statement || !password) {
      return res.status(400).json({ error: 'Введите логин/почту и пароль' });
    }

    const user = await pool.query(
      'SELECT * FROM users WHERE login = $1 OR email = $1',
      [statement]
    );

    if (user.rows.length === 0) {
      return res.status(401).json({
        success: false,
        reason: 'Неверный логин или пароль'
      });
    }

    const userData = user.rows[0];
    const validPassword = await bcrypt.compare(password, userData.password_hash);

    if (!validPassword) {
      return res.status(401).json({
        success: false,
        reason: 'Неверный логин или пароль'
      });
    }

    if (userData.secret_2fa) {
      return res.status(200).json({
        success: true,
        requires2fa: true,
        reason: 'Введите код из Google Authenticator'
      });
    }

    const token = generateToken(userData.id, userData.login);

    res.json({
      success: true,
      token,
      data: {
        id: userData.id,
        login: userData.login,
        email: userData.email
      }
    });
  } catch (err) {
    console.error('Authorization error:', err);
    res.status(500).json({ error: 'Ошибка сервера при авторизации' });
  }
});

// ===== 2FA VERIFICATION =====
app.post('/api/v1/verify-2fa', async (req, res) => {
  try {
    const { statement, code } = req.body;

    if (!statement || !code) {
      return res.status(400).json({ error: 'Введите логин/почту и код' });
    }

    const user = await pool.query(
      'SELECT * FROM users WHERE login = $1 OR email = $1',
      [statement]
    );

    if (user.rows.length === 0) {
      return res.status(401).json({ error: 'Пользователь не найден' });
    }

    const userData = user.rows[0];

    if (!userData.secret_2fa) {
      return res.status(400).json({ error: '2FA не включен' });
    }

    const { authenticator } = require('otplib');
    const isValid = authenticator.check(code, userData.secret_2fa);

    if (!isValid) {
      return res.status(401).json({ error: 'Неверный код 2FA' });
    }

    const token = generateToken(userData.id, userData.login);

    res.json({
      success: true,
      token,
      data: {
        id: userData.id,
        login: userData.login,
        email: userData.email
      }
    });
  } catch (err) {
    console.error('2FA verification error:', err);
    res.status(500).json({ error: 'Ошибка сервера при верификации 2FA' });
  }
});

// ===== PASSWORD RECOVERY =====
app.post('/api/v1/recovery/password', async (req, res) => {
  try {
    const { username } = req.body;

    if (!username) {
      return res.status(400).json({ error: 'Введите почту' });
    }

    const user = await pool.query(
      'SELECT id, email FROM users WHERE email = $1',
      [username]
    );

    if (user.rows.length === 0) {
      return res.status(404).json({ error: 'Пользователь с такой почтой не найден' });
    }

    const userData = user.rows[0];
    const recoveryToken = require('crypto').randomBytes(32).toString('hex');
    const expiresAt = new Date(Date.now() + 3600000);

    await pool.query(
      'UPDATE users SET recovery_token = $1, recovery_expires = $2 WHERE id = $3',
      [recoveryToken, expiresAt, userData.id]
    );

    const resetLink = `${process.env.FRONTEND_URL}/reset-password?token=${recoveryToken}`;

    const nodemailer = require('nodemailer');
    const transporter = nodemailer.createTransport({
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      secure: false,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
      }
    });

    await transporter.sendMail({
      from: process.env.EMAIL_USER,
      to: userData.email,
      subject: 'Восстановление пароля - Rockstar',
      html: `
        <h2>Восстановление пароля</h2>
        <p>Перейдите по ссылке для восстановления пароля:</p>
        <a href="${resetLink}">${resetLink}</a>
        <p>Ссылка действительна 1 час.</p>
      `
    });

    res.json({
      success: true,
      success: 'Письмо для восстановления отправлено на вашу почту'
    });
  } catch (err) {
    console.error('Password recovery error:', err);
    res.status(500).json({ error: 'Ошибка сервера при восстановлении пароля' });
  }
});

// ===== ACCOUNT DETAILS =====
app.get('/api/v1/account/details', async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Не авторизован' });
    }

    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    const user = await pool.query(
      'SELECT id, login, email, created_at FROM users WHERE id = $1',
      [decoded.userId]
    );

    if (user.rows.length === 0) {
      return res.status(404).json({ error: 'Пользователь не найден' });
    }

    res.json({
      success: true,
      data: user.rows[0]
    });
  } catch (err) {
    console.error('Account details error:', err);
    res.status(401).json({ error: 'Неверный или истекший токен' });
  }
});

// Health check
app.get('/api/v1/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
