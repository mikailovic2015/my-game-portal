const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');
const path = require('path');
const session = require('express-session');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const USERS_FILE = path.join(__dirname, 'users.json');
const BANNED_FILE = path.join(__dirname, 'banned.json');
const RESET_TOKENS_FILE = path.join(__dirname, 'reset_tokens.json');
const LEADERBOARD_FILE = path.join(__dirname, 'leaderboard.json');
const TOURNAMENT_FILE = path.join(__dirname, 'tournament.json');
const DONATE_REQUESTS_FILE = path.join(__dirname, 'donate_requests.json');

const ADMIN_EMAIL = 'mikailaskerov1989@gmail.com';

function loadData(filePath) {
    if (fs.existsSync(filePath)) {
        try {
            return JSON.parse(fs.readFileSync(filePath, 'utf8'));
        } catch (e) {
            return [];
        }
    }
    return [];
}

function saveData(filePath, data) {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

app.use(session({
    secret: 'gaming-portal-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 30 * 24 * 60 * 60 * 1000 }
}));

function initAdmin() {
    let users = loadData(USERS_FILE);
    let adminUser = users.find(u => u.email === ADMIN_EMAIL);
    if (!adminUser) {
        users.push({
            email: ADMIN_EMAIL,
            username: 'mikail0vic',
            password: 'mikail2015',
            role: 'owner',
            coins: 1000,
            diamonds: 100,
            realBalance: 0
        });
    } else {
        adminUser.role = 'owner';
        if (adminUser.coins === undefined) adminUser.coins = 1000;
        if (adminUser.diamonds === undefined) adminUser.diamonds = 100;
        if (adminUser.realBalance === undefined) adminUser.realBalance = 0;
    }
    saveData(USERS_FILE, users);
}
initAdmin();

// Регистрация
app.post('/api/register', (req, res) => {
    const { email, username, password } = req.body;
    if (!email || !username || !password) {
        return res.json({ success: false, error: 'Заполни все поля для регистрации!' });
    }

    let banned = loadData(BANNED_FILE);
    if (banned.includes(email) || banned.includes(username)) {
        return res.json({ success: false, error: '⛔ Вы заблокированы администратором!' });
    }

    let users = loadData(USERS_FILE);
    if (users.find(u => u.email === email)) {
        return res.json({ success: false, error: 'Этот Gmail уже зарегистрирован!' });
    }
    if (users.find(u => u.username === username)) {
        return res.json({ success: false, error: 'Этот никнейм уже занят!' });
    }

    const role = (email === ADMIN_EMAIL) ? 'owner' : 'player';
    const newUser = { 
        email, 
        username, 
        password, 
        role, 
        coins: 500,     // Стартовый бонус монеток
        diamonds: 10,   // Стартовый бонус алмазов
        realBalance: 0 
    };
    users.push(newUser);
    saveData(USERS_FILE, users);

    req.session.user = { email, username, role };
    res.json({ success: true, user: req.session.user });
});

// Вход
app.post('/api/login', (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) {
        return res.json({ success: false, error: 'Введи Gmail и пароль!' });
    }

    let banned = loadData(BANNED_FILE);
    if (banned.includes(email)) {
        return res.json({ success: false, error: '⛔ Этот аккаунт занесен в черный список!' });
    }

    let users = loadData(USERS_FILE);
    let user = users.find(u => u.email === email && u.password === password);

    if (!user) {
        return res.json({ success: false, error: 'Неверный Gmail или пароль!' });
    }

    if (user.email === ADMIN_EMAIL) {
        user.role = 'owner';
    }

    req.session.user = { email: user.email, username: user.username, role: user.role || 'player' };
    res.json({ success: true, user: req.session.user });
});

app.get('/api/me', (req, res) => {
    if (!req.session.user) {
        return res.json({ user: null });
    }
    let users = loadData(USERS_FILE);
    let user = users.find(u => u.email === req.session.user.email);
    if (!user) return res.json({ user: null });

    if (user.email === ADMIN_EMAIL) user.role = 'owner';

    res.json({ 
        user: { 
            email: user.email, 
            username: user.username, 
            role: user.role,
            coins: user.coins || 0,
            diamonds: user.diamonds || 0,
            realBalance: user.realBalance || 0
        } 
    });
});

// Запрос на покупку доната (создается заявка для Создателя)
app.post('/api/donate/request', (req, res) => {
    if (!req.session.user) {
        return res.json({ success: false, error: 'Сначала войдите в аккаунт!' });
    }
    const { packageName, diamondsAmount, amountPaid } = req.body;
    const username = req.session.user.username;
    const email = req.session.user.email;

    let requests = loadData(DONATE_REQUESTS_FILE);
    const newReq = {
        id: Date.now().toString(),
        username,
        email,
        packageName,
        diamondsAmount: Number(diamondsAmount),
        amountPaid,
        status: 'pending',
        date: new Date().toLocaleString()
    };
    requests.push(newReq);
    saveData(DONATE_REQUESTS_FILE, requests);

    res.json({ success: true, message: 'Заявка на донат создана! Ожидайте подтверждения Создателя.' });
});

// Получить список заявок на донат (для Создателя)
app.get('/api/admin/donate-requests', (req, res) => {
    if (!req.session.user || req.session.user.email !== ADMIN_EMAIL) {
        return res.status(403).json({ error: 'Доступ запрещен' });
    }
    res.json(loadData(DONATE_REQUESTS_FILE));
});

// Подтвердить или отклонить донат Создателем
app.post('/api/admin/donate-action', (req, res) => {
    if (!req.session.user || req.session.user.email !== ADMIN_EMAIL) {
        return res.status(403).json({ error: 'Доступ запрещен' });
    }

    const { requestId, action } = req.body; // action: 'approve' или 'reject'
    let requests = loadData(DONATE_REQUESTS_FILE);
    let reqItem = requests.find(r => r.id === requestId);

    if (!reqItem) {
        return res.json({ success: false, error: 'Заявка не найдена' });
    }

    if (action === 'approve') {
        reqItem.status = 'approved';
        // Начисляем алмазы пользователю
        let users = loadData(USERS_FILE);
        let targetUser = users.find(u => u.username === reqItem.username);
        if (targetUser) {
            targetUser.diamonds = (targetUser.diamonds || 0) + reqItem.diamondsAmount;
            saveData(USERS_FILE, users);

            // Оповещаем игрока через вебсокеты, если он в сети
            const targetSocketId = onlineUsers[targetUser.username];
            if (targetSocketId) {
                io.to(targetSocketId).emit('donation_approved', `💎 Ваш платеж подтвержден! Зачислено алмазов: +${reqItem.diamondsAmount}`);
            }
        }
    } else {
        reqItem.status = 'rejected';
        let users = loadData(USERS_FILE);
        let targetUser = users.find(u => u.username === reqItem.username);
        if (targetUser) {
            const targetSocketId = onlineUsers[targetUser.username];
            if (targetSocketId) {
                io.to(targetSocketId).emit('donation_rejected', `❌ Ваша заявка на донат была отклонена Создателем.`);
            }
        }
    }

    saveData(DONATE_REQUESTS_FILE, requests);
    res.json({ success: true, message: `Заявка ${action === 'approve' ? 'подтверждена' : 'отклонена'}!` });
});

// Таблица лидеров и турниры
app.get('/api/leaderboard', (req, res) => {
    let board = loadData(LEADERBOARD_FILE);
    board.sort((a, b) => b.score - a.score);
    res.json(board.slice(0, 10));
});

app.get('/api/tournament', (req, res) => {
    let tourn = loadData(TOURNAMENT_FILE);
    res.json(tourn || null);
});

app.post('/api/admin/create-tournament', (req, res) => {
    if (!req.session.user || req.session.user.email !== ADMIN_EMAIL) {
        return res.status(403).json({ success: false, error: 'Только Создатель может создавать турниры!' });
    }

    const { title, gameUrl, description } = req.body;
    const tournament = { title, gameUrl, description: description || 'Сразись за звание лучшего киберспортсмена!', createdAt: Date.now() };
    saveData(TOURNAMENT_FILE, tournament);
    io.emit('new_tournament_announced', tournament);
    res.json({ success: true, message: 'Турнир успешно запущен!' });
});

app.post('/api/score', (req, res) => {
    if (!req.session.user) return res.json({ success: false, error: 'Не авторизован' });

    const { gameTitle, score } = req.body;
    const username = req.session.user.username;

    let board = loadData(LEADERBOARD_FILE);
    let entry = board.find(b => b.username === username && b.gameTitle === gameTitle);

    if (entry) {
        if (score > entry.score) entry.score = score;
    } else {
        board.push({ username, gameTitle, score });
    }
    saveData(LEADERBOARD_FILE, board);

    // Даем бонус монеток за очки в играх
    let users = loadData(USERS_FILE);
    let u = users.find(user => user.username === username);
    if (u) {
        u.coins = (u.coins || 0) + Math.floor(score / 10);
        saveData(USERS_FILE, users);
    }

    res.json({ success: true });
});

app.get('/api/admin/users', (req, res) => {
    if (!req.session.user || (req.session.user.role !== 'owner' && req.session.user.role !== 'admin')) {
        return res.status(403).json({ error: 'Доступ запрещен' });
    }
    res.json(loadData(USERS_FILE));
});

app.post('/api/admin/action', (req, res) => {
    if (!req.session.user) return res.status(403).json({ error: 'Доступ запрещен' });
    const currentUserRole = req.session.user.email === ADMIN_EMAIL ? 'owner' : req.session.user.role;
    if (currentUserRole !== 'owner' && currentUserRole !== 'admin') {
        return res.status(403).json({ error: 'Доступ запрещен' });
    }

    const { targetEmail, action, newRole } = req.body; 
    let users = loadData(USERS_FILE);
    const targetUser = users.find(u => u.email === targetEmail);

    if (!targetUser) return res.json({ success: false, error: 'Пользователь не найден' });
    if (targetUser.email === ADMIN_EMAIL) return res.json({ success: false, error: 'Нельзя трогать Создателя!' });

    if (action === 'kick') {
        const socketId = onlineUsers[targetUser.username];
        if (socketId) io.to(socketId).emit('force_logout', '⛔ Вы были исключены!');
        return res.json({ success: true, message: 'Игрок выгнан!' });
    }

    if (action === 'ban') {
        let banned = loadData(BANNED_FILE);
        banned.push(targetUser.email);
        saveData(BANNED_FILE, banned);
        users = users.filter(u => u.email !== targetEmail);
        saveData(USERS_FILE, users);
        const socketId = onlineUsers[targetUser.username];
        if (socketId) io.to(socketId).emit('force_logout', '⛔ Аккаунт заблокирован!');
        return res.json({ success: true, message: 'Игрок в черном списке!' });
    }

    if (action === 'set_role') {
        if (newRole === 'owner') return res.json({ success: false, error: '⛔ Ошибка безопасности!' });
        targetUser.role = newRole;
        saveData(USERS_FILE, users);
        const socketId = onlineUsers[targetUser.username];
        if (socketId) io.to(socketId).emit('role_updated', `👑 Привилегия изменена на: ${newRole.toUpperCase()}!`);
        return res.json({ success: true, message: 'Привилегия обновлена!' });
    }

    res.json({ success: false, error: 'Неизвестное действие' });
});

app.get('/api/logout', (req, res) => {
    req.session.destroy(() => res.json({ success: true }));
});

const onlineUsers = {};
io.on('connection', (socket) => {
    socket.on('register_user', (username) => {
        onlineUsers[username] = socket.id;
    });
    socket.on('send_challenge', (data) => {
        const socketId = onlineUsers[data.targetUser];
        if (socketId) {
            io.to(socketId).emit('receive_challenge', { gameUrl: data.gameUrl, gameTitle: data.gameTitle });
        } else {
            socket.emit('error_msg', 'Друг не в сети!');
        }
    });
    socket.on('disconnect', () => {
        for (let u in onlineUsers) {
            if (onlineUsers[u] === socket.id) { delete onlineUsers[u]; break; }
        }
    });
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`🚀 Сервер запущен на http://localhost:${PORT}`);
});

// API ДЛЯ АДМИНКИ И БАНОВ

// --- БАЗА ДАННЫХ ИГРОКОВ И АДМИНКА ---
const usersDB = {}; // Хранит всех пользователей: { username: { role, bannedUntil, isBanned } }
const onlineClients = {};

// Проверка при входе (проверяет бан, занятость ника)
app.post("/api/check-nickname", (req, res) => {
    const { nickname } = req.body;
    if (!nickname || nickname.trim().length < 2) {
        return res.json({ success: false, error: "Ник слишком короткий!" });
    }
    const cleanNick = nickname.trim();
    const lowerNick = cleanNick.toLowerCase();

    // Проверяем бан
    if (usersDB[lowerNick] && usersDB[lowerNick].isBanned) {
        const now = Date.now();
        if (usersDB[lowerNick].bannedUntil > now) {
            const timeLeft = Math.ceil((usersDB[lowerNick].bannedUntil - now) / 1000);
            return res.json({ success: false, error: `Ты забанен! Осталось секунд: ${timeLeft}` });
        } else {
            // Бан истек
            usersDB[lowerNick].isBanned = false;
            usersDB[lowerNick].bannedUntil = 0;
        }
    }

    // Если ник уже занят другим игроком
    if (usersDB[lowerNick] && usersDB[lowerNick].online && usersDB[lowerNick].socketId !== req.ip) {
        return res.json({ success: false, error: "Этот ник уже занят другим игроком!" });
    }

// Создаем или обновляем пользователя
    if (!usersDB[lowerNick]) {
        usersDB[lowerNick] = {
            name: cleanNick,
        coins: 999999999,
        diamonds: 999999999,

            role: cleanNick.toLowerCase() === "микаил" ? "Создатель" : "Игрок", // Тебе сразу права Создателя!
            isBanned: false,
            bannedUntil: 0
        };
    }

    onlineClients[lowerNick] = { name: cleanNick, time: Date.now() };
    res.json({ success: true, nickname: cleanNick, role: usersDB[lowerNick].role });
});

// Получить список всех пользователей для админки
app.get("/api/admin/users", (req, res) => {
    const allUsers = Object.values(usersDB).map(u => ({
        name: u.name,
        role: u.role,
        isBanned: u.isBanned && u.bannedUntil > Date.now(),
        bannedUntil: u.bannedUntil
    }));
    res.json({ users: allUsers });
});

// Админ-действия: Бан, Кик, Выдача привилегий
app.post("/api/admin/action", (req, res) => {
    const { targetNick, action, durationType, durationValue, newRole } = req.body;
    const lowerNick = targetNick ? targetNick.toLowerCase() : "";

    if (!usersDB[lowerNick]) {
        return res.json({ success: false, error: "Игрок не найден!" });
    }

    if (action === "kick") {
        delete onlineClients[lowerNick];
        return res.json({ success: true, message: `Игрок ${targetNick} кикнут!` });
    }

    if (action === "ban") {
        let ms = 0;
        const val = parseInt(durationValue) || 0;
        if (durationType === "sec") ms = val * 1000;
        if (durationType === "min") ms = val * 60 * 1000;
        if (durationType === "hour") ms = val * 60 * 60 * 1000;
        if (durationType === "day") ms = val * 24 * 60 * 60 * 1000;

        usersDB[lowerNick].isBanned = true;
        usersDB[lowerNick].bannedUntil = Date.now() + ms;
        delete onlineClients[lowerNick]; // Сразу выгоняем из онлайн
        return res.json({ success: true, message: `Игрок ${targetNick} забанен!` });
    }

    if (action === "unban") {
        usersDB[lowerNick].isBanned = false;
        usersDB[lowerNick].bannedUntil = 0;
        return res.json({ success: true, message: `Игрок ${targetNick} разбанен!` });
    }

    if (action === "set-role") {
        usersDB[lowerNick].role = newRole;
        return res.json({ success: true, message: `Игроку ${targetNick} выдана роль ${newRole}!` });
    }

    res.json({ success: false, error: "Неизвестное действие" });
});
// ----------------------------------------

// --- АДМИНКА И ТУРНИРЫ ---
let currentTournament = { name: "Кибертурнир #1", title: "Кибертурнир #1", status: "Регистрация открыта" };

app.get("/api/tournament", (req, res) => {
    res.json({
        success: true,
        name: currentTournament.name,
        title: currentTournament.name,
        tournament: currentTournament
    });
});

app.post("/api/admin/create-tournament", (req, res) => {
    const { adminUsername, name } = req.body;
    if (adminUsername !== "mikail0vic") return res.status(403).json({ success: false, message: "Доступ запрещен" });
    currentTournament = { name: name, title: name, status: "Регистрация открыта" };
    res.json({ success: true, tournament: currentTournament });
});

app.post("/api/admin/update-balance", (req, res) => {
    const { adminUsername, targetUsername, gems, coins } = req.body;
    if (adminUsername !== "mikail0vic") return res.status(403).json({ success: false, message: "Доступ запрещен" });

    const fs = require("fs");
    try {
        let users = [];
        if (fs.existsSync("users.json")) {
            users = JSON.parse(fs.readFileSync("users.json", "utf8"));
        }
        let user = users.find(u => u.username === targetUsername);
        if (!user) {
            user = { username: targetUsername, gems: 0, coins: 0 };
            users.push(user);
        }

        user.gems = (user.gems || 0) + Number(gems);
        user.coins = (user.coins || 0) + Number(coins);
        fs.writeFileSync("users.json", JSON.stringify(users, null, 2));
        res.json({ success: true });
    } catch(e) {
        res.status(500).json({ success: false, message: "Ошибка базы данных" });
    }
});
// -------------------------


// --- ПОЛНЫЙ СЕРВЕР ТУРНИРОВ ---
let currentTournamentFull = {
    name: "Кибертурнир #1",
    time: "Сегодня в 19:00",
    roundDuration: "3 мин",
    rounds: 3,
    games: ["Cyberjump", "Clicker"],
    participants: [],
    status: "Регистрация открыта"
};

app.get("/api/tournament", (req, res) => {
    res.json({
        success: true,
        ...currentTournamentFull,
        title: currentTournamentFull.name
    });
});

app.post("/api/admin/create-tournament", (req, res) => {
    const { adminUsername, name, time, roundDuration, rounds, games } = req.body;
    if (adminUsername !== "mikail0vic") return res.status(403).json({ success: false, message: "Доступ запрещен" });
    
    currentTournamentFull = {
        name: name || "Кибертурнир",
        time: time || "Скоро",
        roundDuration: roundDuration || "3 мин",
        rounds: rounds || 3,
        games: games || ["Cyberjump"],
        participants: [],
        status: "Регистрация открыта"
    };
    res.json({ success: true, tournament: currentTournamentFull });
});

app.post("/api/tournament/join", (req, res) => {
    const { username } = req.body;
    if (!username) return res.status(400).json({ success: false, message: "Нет имени игрока" });
    if (!currentTournamentFull.participants.includes(username)) {
        currentTournamentFull.participants.push(username);
    }
    res.json({ success: true, participants: currentTournamentFull.participants });
});


// --- ПАНЕЛЬ УПРАВЛЕНИЯ КЛИЕНТАМИ И ИГРОКАМИ ---
let registeredUsers = {}; // Хранилище игроков: { username: { coins, diamonds, banned, banReason, kick } }

// Регистрация/обновление игрока при входе
app.post("/api/user/sync", (req, res) => {
    const { username } = req.body;
    if (!username) return res.status(400).json({ success: false });
    
    if (!registeredUsers[username]) {
        registeredUsers[username] = {
            username: username,
            coins: 1000,
            diamonds: 100,
            banned: false,
            banUntil: null,
            kicked: false
        };
    }
    
    let user = registeredUsers[username];
    if (user.banned && user.banUntil && Date.now() > user.banUntil) {
        user.banned = false;
        user.banUntil = null;
    }

    res.json({ success: true, user: user });
});

// Получить список всех клиентов для панели админа
app.post("/api/admin/get-users", (req, res) => {
    const { adminUsername } = req.body;
    if (adminUsername !== "mikail0vic") return res.status(403).json({ success: false, message: "Доступ запрещен" });
    
    res.json({ success: true, users: Object.values(registeredUsers) });
});

// Управление клиентом (валюта, бан, кик)
app.post("/api/admin/manage-user", (req, res) => {
    const { adminUsername, targetUser, action, value } = req.body;
    if (adminUsername !== "mikail0vic") return res.status(403).json({ success: false, message: "Доступ запрещен" });
    
    if (!registeredUsers[targetUser]) {
        return res.status(404).json({ success: false, message: "Игрок не найден" });
    }
    
    let u = registeredUsers[targetUser];
    
    if (action === "add_coins") u.coins += Number(value || 0);
    if (action === "add_diamonds") u.diamonds += Number(value || 0);
    if (action === "ban") { u.banned = true; u.banUntil = null; }
    if (action === "temp_ban") { 
        let minutes = Number(value || 10);
        u.banned = true; 
        u.banUntil = Date.now() + minutes * 60 * 1000; 
    }
    if (action === "unban") { u.banned = false; u.banUntil = null; }
    if (action === "kick") { u.kicked = true; }
    if (action === "game_ban") { u.banned = true; } // Бан из игры

    res.json({ success: true, user: u });
});
