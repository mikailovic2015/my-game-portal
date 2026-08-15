import os

html_code = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Кибер-Генератор Паролей</title>
    <style>
        * { box-sizing: border-box; }
        body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; padding: 15px 10px; margin: 0; min-height: 100vh; }
        .container { max-width: 460px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 16px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .back-link { display: block; text-align: left; color: #58a6ff; text-decoration: none; margin-bottom: 15px; font-size: 14px; font-weight: bold; }
        .title { font-size: 22px; font-weight: 800; color: #58a6ff; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 8px; }
        
        /* Display Box */
        .pass-box { position: relative; background: #010409; border: 2px solid #30363d; border-radius: 12px; padding: 14px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; gap: 10px; transition: border-color 0.3s; }
        .pass-box:focus-within, .pass-box:hover { border-color: #58a6ff; }
        .pass-text { font-family: "Courier New", Courier, monospace; font-size: 20px; font-weight: bold; color: #3fb950; letter-spacing: 2px; overflow-x: auto; white-space: nowrap; width: 100%; text-align: left; scrollbar-width: none; }
        .pass-text::-webkit-scrollbar { display: none; }
        .copy-btn { background: #238636; color: white; border: none; padding: 10px 14px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; flex-shrink: 0; display: flex; align-items: center; gap: 5px; font-size: 13px; }
        .copy-btn:hover { background: #2ea043; transform: scale(1.03); }
        
        /* Strength Bar */
        .strength-container { margin-bottom: 20px; text-align: left; }
        .strength-header { display: flex; justify-content: space-between; font-size: 12px; color: #8b949e; margin-bottom: 6px; font-weight: bold; }
        .strength-bar-bg { width: 100%; height: 8px; background: #21262d; border-radius: 4px; overflow: hidden; }
        .strength-bar-fill { height: 100%; width: 0%; transition: width 0.4s ease, background-color 0.4s ease; border-radius: 4px; }
        
        /* Controls */
        .controls-group { background: #010409; border: 1px solid #21262d; border-radius: 12px; padding: 15px; margin-bottom: 15px; text-align: left; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 14px; font-weight: bold; }
        .slider-val { color: #58a6ff; font-size: 16px; font-weight: 800; }
        input[type=range] { width: 100%; accent-color: #58a6ff; cursor: pointer; height: 6px; }
        
        .options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .option-item { display: flex; align-items: center; gap: 8px; font-size: 13px; background: #161b22; padding: 8px 10px; border-radius: 8px; border: 1px solid #30363d; cursor: pointer; user-select: none; }
        .option-item input[type=checkbox] { accent-color: #58a6ff; width: 16px; height: 16px; cursor: pointer; }
        
        .mode-selector { display: flex; gap: 6px; margin-top: 12px; }
        .mode-btn { flex: 1; padding: 8px; font-size: 12px; font-weight: bold; background: #161b22; color: #8b949e; border: 1px solid #30363d; border-radius: 6px; cursor: pointer; }
        .mode-btn.active { background: #1f6feb; color: white; border-color: #58a6ff; }
        
        /* Generate Button */
        .gen-btn { width: 100%; background: linear-gradient(135deg, #1f6feb, #238636); color: white; border: none; padding: 14px; font-size: 16px; font-weight: 800; border-radius: 10px; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; transition: 0.2s; box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4); }
        .gen-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(31, 111, 235, 0.6); }
        .gen-btn:active { transform: translateY(0); }

        /* History */
        .history-box { margin-top: 20px; text-align: left; background: #010409; border: 1px solid #21262d; border-radius: 12px; padding: 12px; }
        .history-title { font-size: 12px; font-weight: bold; color: #8b949e; margin-bottom: 8px; text-transform: uppercase; }
        .history-item { display: flex; justify-content: space-between; align-items: center; font-family: monospace; font-size: 13px; padding: 6px 8px; background: #161b22; border-radius: 6px; margin-bottom: 4px; border: 1px solid #30363d; }
        .history-item span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 80%; }
        .history-copy { color: #58a6ff; cursor: pointer; font-size: 12px; font-weight: bold; }
        
        /* Toast */
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(100px); background: #238636; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 14px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); opacity: 0; transition: all 0.3s ease; pointer-events: none; }
        .toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
    </style>
</head>
<body>

<div class="container">
    <a href="/" class="back-link">← На главную</a>
    <div class="title">🔐 Кибер-Пароль</div>

    <div class="pass-box">
        <div class="pass-text" id="password_display">Пароль...</div>
        <button class="copy-btn" onclick="copyPassword()">📋 Копировать</button>
    </div>

    <div class="strength-container">
        <div class="strength-header">
            <span>Надежность: <strong id="strength_text" style="color:#f85149;">—</strong></span>
            <span id="crack_time">Время на взлом: —</span>
        </div>
        <div class="strength-bar-bg">
            <div class="strength-bar-fill" id="strength_bar"></div>
        </div>
    </div>

    <div class="controls-group">
        <div class="slider-header">
            <span>Длина пароля</span>
            <span class="slider-val" id="length_val">16</span>
        </div>
        <input type="range" id="length_slider" min="6" max="64" value="16" oninput="updateLength(this.value)">

        <div class="mode-selector">
            <button class="mode-btn active" id="mode_random" onclick="setMode('random')">Случайный</button>
            <button class="mode-btn" id="mode_easy" onclick="setMode('easy')">Произносимый</button>
            <button class="mode-btn" id="mode_phrase" onclick="setMode('phrase')">Фраза</button>
        </div>

        <div class="options-grid" id="options_container">
            <label class="option-item"><input type="checkbox" id="opt_upper" checked onchange="generate()"> A-Z (Заглавные)</label>
            <label class="option-item"><input type="checkbox" id="opt_lower" checked onchange="generate()"> a-z (Строчные)</label>
            <label class="option-item"><input type="checkbox" id="opt_digits" checked onchange="generate()"> 0-9 (Цифры)</label>
            <label class="option-item"><input type="checkbox" id="opt_symbols" checked onchange="generate()"> !@#$% (Спецсимволы)</label>
            <label class="option-item" style="grid-column: span 2;"><input type="checkbox" id="opt_avoid" onchange="generate()"> Исключить похожие (l, 1, I, O, 0)</label>
        </div>
    </div>

    <button class="gen-btn" onclick="generateWithAnim()">⚡ Сгенерировать пароль</button>

    <div class="history-box">
        <div class="history-title">📜 История паролей (последние 5)</div>
        <div id="history_list"></div>
    </div>
</div>

<div class="toast" id="toast">✅ Скопировано в буфер!</div>

<script>
let currentMode = "random";
let history = [];

const wordsList = ["Cyber", "Matrix", "Shield", "Rocket", "Storm", "Phoenix", "Titan", "Vortex", "Falcon", "Quantum", "Hyper", "Shadow", "Neon", "Signal", "Orbit"];

function setMode(mode) {
    currentMode = mode;
    document.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("active"));
    document.getElementById("mode_" + mode).classList.add("active");
    
    let optContainer = document.getElementById("options_container");
    if (mode === "phrase" || mode === "easy") {
        optContainer.style.opacity = "0.4";
        optContainer.style.pointerEvents = "none";
    } else {
        optContainer.style.opacity = "1";
        optContainer.style.pointerEvents = "all";
    }
    generate();
}

function updateLength(val) {
    document.getElementById("length_val").innerText = val;
    generate();
}

function generate() {
    let len = parseInt(document.getElementById("length_slider").value);
    let pass = "";
    
    if (currentMode === "phrase") {
        let count = Math.max(2, Math.floor(len / 6));
        let selected = [];
        for (let i = 0; i < count; i++) {
            selected.push(wordsList[Math.floor(Math.random() * wordsList.length)]);
        }
        pass = selected.join("-") + Math.floor(Math.random() * 99 + 10);
    } else if (currentMode === "easy") {
        let vowels = "aeiouy";
        let consonants = "bcdfghjklmnpqrstvwxz";
        for (let i = 0; i < len; i++) {
            pass += (i % 2 === 0) ? consonants[Math.floor(Math.random() * consonants.length)] : vowels[Math.floor(Math.random() * vowels.length)];
        }
    } else {
        let chars = "";
        if (document.getElementById("opt_upper").checked) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        if (document.getElementById("opt_lower").checked) chars += "abcdefghijklmnopqrstuvwxyz";
        if (document.getElementById("opt_digits").checked) chars += "0123456789";
        if (document.getElementById("opt_symbols").checked) chars += "!@#$%^&*()_+-=[]{}|;:,.<>?";
        
        if (document.getElementById("opt_avoid").checked) {
            chars = chars.replace(/[l1IO0]/g, "");
        }
        
        if (!chars) chars = "abcdefghijklmnopqrstuvwxyz";

        for (let i = 0; i < len; i++) {
            pass += chars[Math.floor(Math.random() * chars.length)];
        }
    }

    document.getElementById("password_display").innerText = pass;
    evaluateStrength(pass);
    return pass;
}

function generateWithAnim() {
    let textElem = document.getElementById("password_display");
    let glitchChars = "!@#$%^&*()_+-=[]{}|;:,.<>?ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let iterations = 0;
    
    let interval = setInterval(() => {
        let randomStr = "";
        let len = parseInt(document.getElementById("length_slider").value);
        for(let i=0; i<len; i++) {
            randomStr += glitchChars[Math.floor(Math.random() * glitchChars.length)];
        }
        textElem.innerText = randomStr;
        iterations++;
        if (iterations > 6) {
            clearInterval(interval);
            let finalPass = generate();
            addToHistory(finalPass);
        }
    }, 40);
}

function evaluateStrength(pass) {
    let score = 0;
    if (pass.length >= 8) score += 1;
    if (pass.length >= 14) score += 1;
    if (/[A-Z]/.test(pass)) score += 1;
    if (/[0-9]/.test(pass)) score += 1;
    if (/[^A-Za-z0-9]/.test(pass)) score += 1;

    let bar = document.getElementById("strength_bar");
    let text = document.getElementById("strength_text");
    let crack = document.getElementById("crack_time");

    if (pass.length < 8) {
        bar.style.width = "20%";
        bar.style.backgroundColor = "#f85149";
        text.innerText = "Слабенький ⚠️";
        text.style.color = "#f85149";
        crack.innerText = "Время на взлом: несколько секунд";
    } else if (score <= 3) {
        bar.style.width = "50%";
        bar.style.backgroundColor = "#d29922";
        text.innerText = "Средний 🟡";
        text.style.color = "#d29922";
        crack.innerText = "Время на взлом: пару дней";
    } else if (score === 4) {
        bar.style.width = "80%";
        bar.style.backgroundColor = "#3fb950";
        text.innerText = "Надежный 🟢";
        text.style.color = "#3fb950";
        crack.innerText = "Время на взлом: несколько лет";
    } else {
        bar.style.width = "100%";
        bar.style.backgroundColor = "#a371f7";
        text.innerText = "Кибер-Щит 🛡️";
        text.style.color = "#a371f7";
        crack.innerText = "Время на взлом: миллиарды лет";
    }
}

function copyPassword() {
    let pass = document.getElementById("password_display").innerText;
    if (!pass || pass === "Пароль...") return;
    
    navigator.clipboard.writeText(pass).then(() => {
        showToast();
    }).catch(() => {
        let input = document.createElement("input");
        input.value = pass;
        document.body.appendChild(input);
        input.select();
        document.execCommand("copy");
        document.body.removeChild(input);
        showToast();
    });
}

function showToast() {
    let toast = document.getElementById("toast");
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2000);
}

function addToHistory(pass) {
    if (history.includes(pass)) return;
    history.unshift(pass);
    if (history.length > 5) history.pop();
    
    let html = "";
    history.forEach(p => {
        html += `<div class="history-item">
            <span>${p}</span>
            <span class="history-copy" onclick="copyCustom('${p}')">Копировать</span>
        </div>`;
    });
    document.getElementById("history_list").innerHTML = html;
}

function copyCustom(str) {
    navigator.clipboard.writeText(str);
    showToast();
}

generate();
</script>

</body>
</html>
"""

try:
    target_dir = "password_gen"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        
    target_file = os.path.join(target_dir, "index.html")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(html_code)
        
    # Реальная проверка создания файла перед выводом успеха
    if os.path.exists(target_file) and os.path.getsize(target_file) > 100:
        print("\033[92m[УСПЕХ] Файл password_gen/index.html создан и записан успешно!\033[0m")
    else:
        print("\033[91m[ОШИБКА] Файл не удалось записать.\033[0m")
except Exception as e:
    print(f"\033[91m[ОШИБКА SYSTEM]: {e}\033[0m")
