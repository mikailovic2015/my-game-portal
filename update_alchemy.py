html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Магическая Алхимия</title>
    <style>
        body { background: #0d1117; color: #fff; font-family: Segoe UI, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { max-width: 450px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
        .back-link { display: block; text-align: left; color: #58a6ff; text-decoration: none; margin-bottom: 10px; font-size: 14px; font-weight: bold; }
        .stats-top { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
        .stat-card { background: #010409; padding: 10px; border-radius: 8px; border: 1px solid #30363d; font-size: 13px; font-weight: bold; }
        .status-box { background: #21262d; padding: 10px; border-radius: 8px; margin-bottom: 12px; text-align: left; font-size: 13px; border: 1px solid #30363d; }
        .game-box { background: #21262d; border: 2px solid #bc8cff; padding: 12px; border-radius: 10px; margin-bottom: 12px; text-align: center; }
        .alert { color: #bc8cff; font-weight: bold; font-size: 13px; margin-bottom: 8px; min-height: 18px; }
        .btn { width: 100%; padding: 12px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; margin-bottom: 8px; text-transform: uppercase; font-size: 14px; }
        .craft-btn { background: #bc8cff; color: #000; }
        .elements-grid { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-top: 10px; }
        .element-badge { background: #30363d; padding: 6px 10px; border-radius: 6px; font-size: 12px; border: 1px solid #484f58; }
    </style>
</head>
<body>

<div class="container">
    <a href="/" class="back-link">← На главную</a>
    <h2>🧪 Магическая Алхимия</h2>
    
    <div class="stats-top">
        <div class="stat-card">✨ Открыто: <span id="elements_count">4</span>/12</div>
        <div class="stat-card">🔮 Мана: <span id="mana">100</span></div>
    </div>
    
    <div class="status-box">
        <div style="margin-bottom: 6px; font-weight: bold; color: #8b949e;">Инвентарь элементов:</div>
        <div class="elements-grid" id="inventory_list">
            <span class="element-badge">💧 Вода</span>
            <span class="element-badge">🔥 Огонь</span>
            <span class="element-badge">🌍 Земля</span>
            <span class="element-badge">💨 Воздух</span>
        </div>
    </div>

    <div class="game-box">
        <div class="alert" id="alchemy_alert">🧙‍♂️ Осторожно с пропорциями, возможен взрыв колбы!</div>
        <div style="margin-bottom: 8px;">
            <select id="elem1" style="background: #30363d; color: #fff; padding: 6px; border-radius: 6px; border: 1px solid #484f58;">
                <option value="Вода">💧 Вода</option>
                <option value="Огонь">🔥 Огонь</option>
                <option value="Земля">🌍 Земля</option>
                <option value="Воздух">💨 Воздух</option>
            </select>
            +
            <select id="elem2" style="background: #30363d; color: #fff; padding: 6px; border-radius: 6px; border: 1px solid #484f58;">
                <option value="Вода">💧 Вода</option>
                <option value="Огонь">🔥 Огонь</option>
                <option value="Земля">🌍 Земля</option>
                <option value="Воздух">💨 Воздух</option>
            </select>
        </div>
    </div>

    <button class="btn craft-btn" onclick="mixElements()">✨ Смешать ингредиенты</button>
</div>

<script>
let unlocked = ["Вода", "Огонь", "Земля", "Воздух"];
let mana = 100;
let recipes = {
    "Вода+Огонь": "💨 Пар",
    "Земля+Огонь": "🌋 Лава",
    "Земля+Вода": "🌱 Грязь",
    "Воздух+Земля": "🏜️ Пыль",
    "Огонь+Воздух": "⚡ Энергия",
    "Пар+Земля": "☁️ Облако",
    "Лава+Вода": "🪨 Камень",
    "Энергия+Грязь": "🧬 Жизнь"
};

function updateInventory() {
    let listHTML = "";
    unlocked.forEach(el => { listHTML += `<span class="element-badge">${el}</span>`; });
    document.getElementById("inventory_list").innerHTML = listHTML;
    document.getElementById("elements_count").innerText = unlocked.length;
    document.getElementById("mana").innerText = mana;
    
    let optionsHTML = "";
    unlocked.forEach(el => { optionsHTML += `<option value="${el}">${el}</option>`; });
    document.getElementById("elem1").innerHTML = optionsHTML;
    document.getElementById("elem2").innerHTML = optionsHTML;
}

function mixElements() {
    if (mana < 15) {
        document.getElementById("alchemy_alert").innerText = "⚠️ Недостаточно маны! Подожди восстановления...";
        setTimeout(() => { mana = 100; updateInventory(); document.getElementById("alchemy_alert").innerText = "🔮 Мана восстановлена!"; }, 1500);
        return;
    }
    
    mana -= 15;
    let e1 = document.getElementById("elem1").value;
    let e2 = document.getElementById("elem2").value;
    let key1 = e1 + "+" + e2;
    let key2 = e2 + "+" + e1;
    let result = recipes[key1] || recipes[key2];
    
    let failChance = Math.random();
    
    if (failChance < 0.25) {
        // Неудачный алхимический эксперимент (взрыв колбы)
        document.getElementById("alchemy_alert").innerText = "💥 БАБАХ! Колба взорвалась от нестабильной магии, ингредиенты сгорели!";
    } else if (result) {
        if (!unlocked.includes(result)) {
            unlocked.push(result);
            document.getElementById("alchemy_alert").innerText = "🎉 Успех! Создан новый элемент: " + result;
        } else {
            document.getElementById("alchemy_alert").innerText = "⚠️ Этот элемент (" + result + ") у тебя уже есть, ничего нового.";
        }
    } else {
        document.getElementById("alchemy_alert").innerText = "💨 Реакция не удалась... Получилась бесполезная жижа.";
    }
    updateInventory();
}
</script>
</body>
</html>
"""
import os
os.makedirs("magic_alchemy", exist_ok=True)
with open("magic_alchemy/index.html", "w", encoding="utf-8") as f: f.write(html_content)
print("АЛХИМИЯ ОБНОВЛЕНА (УСПЕХИ И ВЗРЫВЫ ДОБАВЛЕНЫ)")
