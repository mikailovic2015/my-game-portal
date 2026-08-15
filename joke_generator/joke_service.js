const fs = require('fs');
const path = require('path');
const https = require('https');

const JOKES_FILE = path.join(__dirname, 'jokes.json');

const initialJokes = [
    { cat: "it", text: "Программист перед сном ставит два стакана: один с водой, второй пустой." },
    { cat: "it", text: "Фича — это баг, который оформил подписку и пробрался в релиз." },
    { cat: "life", text: "Я не откладываю дела на потом, я даю им время настояться." },
    { cat: "short", text: "Настоящая свобода — это когда выключены все уведомления." }
];

function loadJokes() {
    if (!fs.existsSync(JOKES_FILE)) {
        fs.writeFileSync(JOKES_FILE, JSON.stringify(initialJokes, null, 2), 'utf-8');
        return initialJokes;
    }
    try {
        return JSON.parse(fs.readFileSync(JOKES_FILE, 'utf-8'));
    } catch (e) {
        return initialJokes;
    }
}

function saveJokes(jokes) {
    fs.writeFileSync(JOKES_FILE, JSON.stringify(jokes, null, 2), 'utf-8');
}

function fetchJokeOnline() {
    https.get('https://v2.jokeapi.dev/joke/Any?type=single&safe-mode', (res) => {
        let raw = '';
        res.on('data', chunk => raw += chunk);
        res.on('end', () => {
            try {
                const data = JSON.parse(raw);
                if (data && data.joke) {
                    const list = loadJokes();
                    const exists = list.some(j => (j.text || j) === data.joke);
                    if (!exists) {
                        list.push({ cat: data.category ? data.category.toLowerCase() : "life", text: data.joke });
                        saveJokes(list);
                        console.log(`[JOKE SERVICE] Добавлена новая шутка из сети! Всего: ${list.length}`);
                    }
                }
            } catch (err) {}
        });
    }).on('error', () => {});
}

function startBackgroundFetcher(intervalMinutes = 5) {
    fetchJokeOnline();
    setInterval(fetchJokeOnline, intervalMinutes * 60 * 1000);
}

module.exports = { loadJokes, startBackgroundFetcher };
