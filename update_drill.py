html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Космический Бур</title>
    <style>
        body { background: #0d1117; color: #fff; font-family: Segoe UI, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { max-width: 450px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
        .back-link { display: block; text-align: left; color: #58a6ff; text-decoration: none; margin-bottom: 10px; font-size: 14px; font-weight: bold; }
        .stats-top { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
        .stat-card { background: #010409; padding: 10px; border-radius: 8px; border: 1px solid #30363d; font-size: 13px; font-weight: bold; }
        .status-box { background: #21262d; padding: 10px; border-radius: 8px; margin-bottom: 12px; text-align: left; font-size: 13px; border: 1px solid #30363d; }
        .bar-container { width: 100%; background: #30363d; height: 8px; border-radius: 4px; margin: 3px 0 8px 0; overflow: hidden; }
        .bar { height: 100%; transition: width 0.3s; }
        .drill-box { background: #21262d; border: 2px solid #d29922; padding: 12px; border-radius: 10px; margin-bottom: 12px; text-align: center; }
        .alert { color: #d29922; font-weight: bold; font-size: 13px; margin-bottom: 8px; min-height: 18px; }
        .btn { width: 100%; padding: 12px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; margin-bottom: 8px; text-transform: uppercase; font-size: 14px; }
        .drill-btn { background: #d29922; color: #000; }
        .shop-box { background: #1f242c; padding: 10px; border-radius: 8px; border: 1px solid #30363d; text-align: left; margin-bottom: 5px; }
        .shop-title { font-weight: bold; margin-bottom: 8px; color: #58a6ff; font-size: 13px; text-transform: uppercase; }
        .shop-item { display: flex; justify-content: space-between; align-items: center; background: #2d333b; padding: 8px 10px; margin-bottom: 6px; border-radius: 6px; font-size: 13px; }
        .buy-btn { background: #238636; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-weight: bold; flex-shrink: 0; }
    </style>
</head>
<body>

<div class="container">
    <a href="/" class="back-link">← На главную</a>
    <h2>🚀 Космический Бур</h2>
    
    <div class="stats-top">
        <div class="stat-card">⛏️ Глубина: <span id="depth">0</span> м</div>
        <div class="stat-card">💎 Руда: <span id="ore">0</span></div>
    </div>
    
    <div class="status-box">
        <div>Энергия бура: <span id="energy_val">100</span>/100</div>
        <div class="bar-container"><div class="bar" id="energy_bar" style="width: 100%; background: #58a6ff;"></div></div>
        <div>Кредиты: <span id="money">0</span> 🪙</div>
    </div>

    <div class="drill-box">
        <div class="alert" id="drill_alert">⚠️ Бур готов к погружению. Остерегайся аномалий!</div>
        <div>🌍 Слой: <span id="layer_name">Верхний грунт</span></div>
    </div>

    <button class="btn drill-btn" onclick="drillRock()">⚡ Бурить породу</button>

    <div class="shop-box">
        <div class="shop-title">🛒 Ангар модернизации:</div>
        <div class="shop-item"><span>Охладитель (+25 макс. энергии)</span> <button class="buy-btn" onclick="buy('energy', 25, 30)">30 🪙</button></div>
        <div class="shop-item"><span>Улучшить бур (+1 сила)</span> <button class="buy-btn" onclick="buy('power', 1, 40)">40 🪙</button></div>
        <div class="shop-item"><span>Продать всю руду (1 руда = 5 🪙)</span> <button class="buy-btn" style="background:#1f6feb;" onclick="sellOre()">Продать</button></div>
    </div>
</div>

<script>
let g = { depth: 0, ore: 0, money: 0, energy: 100, maxEnergy: 100, power: 1 };

function update() {
    document.getElementById("depth").innerText = g.depth;
    document.getElementById("ore").innerText = g.ore;
    document.getElementById("money").innerText = g.money;
    document.getElementById("energy_val").innerText = Math.round(g.energy);
    document.getElementById("energy_bar").style.width = (g.energy / g.maxEnergy * 100) + "%";
    
    let layer = "Верхний грунт";
    if (g.depth > 50) layer = "Твердая скала";
    if (g.depth > 150) layer = "Магматический слой";
    if (g.depth > 300) layer = "Ядро планеты";
    document.getElementById("layer_name").innerText = layer;
}

function drillRock() {
    if (g.energy >= 10) {
        g.energy -= 10;
        let roll = Math.random();
        
        if (roll < 0.25) {
            // Неудачный исход: провал / аномалия
            document.getElementById("drill_alert").innerText = "💥 Провал! Бур наткнулся на твердую породу и заклинил. Руды нет!";
        } else if (roll < 0.45) {
            // Еще одна неудача: газовый карман (урон энергии)
            g.energy = Math.max(0, g.energy - 15);
            document.getElementById("drill_alert").innerText = "⚠️ Упс! Газовый карман повредил систему охлаждения (-15 энергии)!";
        } else {
            // Удачный исход
            g.depth += g.power * 5;
            let foundOre = g.power * (Math.floor(Math.random() * 3) + 1);
            g.ore += foundOre;
            document.getElementById("drill_alert").innerText = "⛏️ Успех! Добыто руды: +" + foundOre;
        }
        update();
    } else {
        document.getElementById("drill_alert").innerText = "🔋 Батарея разряжена! Ждем перезарядки...";
        setTimeout(() => { g.energy = g.maxEnergy; update(); document.getElementById("drill_alert").innerText = "⚡ Энергия восстановлена!"; }, 1500);
    }
}

function sellOre() {
    if (g.ore > 0) {
        let earned = g.ore * 5;
        g.money += earned;
        let sold = g.ore;
        g.ore = 0;
        update();
        document.getElementById("drill_alert").innerText = "💰 Продано руды (" + sold + ") за " + earned + " кредитов!";
    } else {
        document.getElementById("drill_alert").innerText = "⚠️ У тебя нет руды для продажи!";
    }
}

function buy(type, amount, cost) {
    if (g.money >= cost) {
        g.money -= cost;
        if (type === 'energy') { g.maxEnergy += amount; g.energy = g.maxEnergy; }
        if (type === 'power') { g.power += amount; }
        update();
        document.getElementById("drill_alert").innerText = "✅ Улучшение успешно установлено!";
    } else {
        document.getElementById("drill_alert").innerText = "❌ Не хватает кредитов!";
    }
}

update();
</script>
</body>
</html>
"""
import os
os.makedirs("space_drill", exist_ok=True)
with open("space_drill/index.html", "w", encoding="utf-8") as f: f.write(html_content)
print("БУР ОБНОВЛЕН (УСПЕХИ И ПРОВАЛЫ ДОБАВЛЕНЫ)")
