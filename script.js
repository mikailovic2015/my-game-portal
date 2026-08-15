
const mathExamples = [
    { q: "5 + 7 =", a: 12 }, { q: "12 - 4 =", a: 8 }, { q: "6 * 3 =", a: 18 }, { q: "20 / 5 =", a: 4 }, { q: "9 + 9 =", a: 18 },
    { q: "15 - 6 =", a: 9 }, { q: "7 * 7 =", a: 49 }, { q: "32 / 8 =", a: 4 }, { q: "11 + 8 =", a: 19 }, { q: "14 - 9 =", a: 5 },
    { q: "4 * 6 =", a: 24 }, { q: "81 / 9 =", a: 9 }, { q: "13 + 7 =", a: 20 }, { q: "25 - 10 =", a: 15 }, { q: "5 * 5 =", a: 25 },
    { q: "36 / 6 =", a: 6 }, { q: "18 + 2 =", a: 20 }, { q: "30 - 12 =", a: 18 }, { q: "3 * 9 =", a: 27 }, { q: "45 / 5 =", a: 9 },
    { q: "16 + 16 =", a: 32 }, { q: "50 - 25 =", a: 25 }, { q: "8 * 8 =", a: 64 }, { q: "64 / 8 =", a: 8 }, { q: "19 + 11 =", a: 30 },
    { q: "22 - 7 =", a: 15 }, { q: "9 * 6 =", a: 54 }, { q: "40 / 4 =", a: 10 }, { q: "14 + 14 =", a: 28 }, { q: "60 - 20 =", a: 40 },
    { q: "7 * 8 =", a: 56 }, { q: "72 / 9 =", a: 8 }, { q: "25 + 25 =", a: 50 }, { q: "33 - 13 =", a: 20 }, { q: "4 * 9 =", a: 36 },
    { q: "54 / 6 =", a: 9 }, { q: "17 + 13 =", a: 30 }, { q: "44 - 11 =", a: 33 }, { q: "6 * 6 =", a: 36 }, { q: "48 / 6 =", a: 8 },
    { q: "21 + 9 =", a: 30 }, { q: "99 - 33 =", a: 66 }, { q: "9 * 9 =", a: 81 }, { q: "56 / 7 =", a: 8 }, { q: "12 + 18 =", a: 30 },
    { q: "75 - 25 =", a: 50 }, { q: "3 * 8 =", a: 24 }, { q: "28 / 4 =", a: 7 }, { q: "10 + 90 =", a: 100 }, { q: "100 - 50 =", a: 50 }
];

let currentCorrectAnswer = 0;

function generateCaptcha() {
    const randomIndex = Math.floor(Math.random() * mathExamples.length);
    const selected = mathExamples[randomIndex];
    currentCorrectAnswer = selected.a;
    const qEl = document.getElementById("captcha-question");
    if (qEl) qEl.innerText = selected.q;
}

function verifyAndGetLink() {
    const userAnswer = parseInt(document.getElementById("captcha-input").value);
    const userEmail = document.getElementById("reset-email").value;
    
    if (userAnswer !== currentCorrectAnswer) {
        alert("Ошибка! Неверный ответ на пример. Попробуй еще раз.");
        generateCaptcha();
        return;
    }

    if (!userEmail) {
        alert("Введи почту!");
        return;
    }

    const uniqueToken = Math.random().toString(36).substring(2) + Date.now().toString(36);
    const resetLink = `${window.location.origin}/reset-password.html?token=${uniqueToken}&email=${encodeURIComponent(userEmail)}`;

    const resultBox = document.getElementById("reset-result-box");
    if (resultBox) {
        resultBox.style.display = "block";
        resultBox.innerHTML = `Капча пройдена! Вот твоя персональная ссылка для смены пароля:<br><br><a href="${resetLink}" target="_blank" style="color: #58a6ff; word-break: break-all;">${resetLink}</a>`;
    }
}
