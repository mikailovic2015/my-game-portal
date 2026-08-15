html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Спид-Дрифт</title>
    <style>
        body { background: #0d1117; color: #fff; font-family: Segoe UI, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { max-width: 450px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
        .back-link { display: block; text-align: left; color: #58a6ff; text-decoration: none; margin-bottom: 10px; font-size: 14px; font-weight: bold; }
        .stats-top { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
        .stat-card { background: #010409; padding: 10px; border-radius: 8px; border: 1px solid #30363d; font-size: 13px; font-weight: bold; }
        .status-box { background: #21262d; padding: 10px; border-radius: 8px; margin-bottom: 12px; text-align: left; font-size: 13px; border: 1px solid #30363d; }
        .bar-container { width: 100%; background: #30363d; height: 8px; border-radius: 4px; margin: 3px 0 8px 0; overflow: hidden; }
        .bar { height: 100%; transition: width 0.3s; }
        .game-box { background: #21262d; border: 2px solid #58a6ff; padding: 12px; border-radius: 10px; margin-bottom: 12px; text-align: center; }
        .alert { color: #58a6ff; font-weight: bold; font-size: 13px; margin-bottom: 8px; min-height: 18px; }
        .btn { width: 100%; padding: 12px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; margin-bottom: 8px; text-transform: uppercase; font-size: 14px; }
        .drift-btn { background: #58a6ff; color: #000; }
        .shop-box { background: #1f242c; padding: 10px; border-radius: 8px; border: 1px solid #30363d; text-align: left; margin-bottom: 5px; }
        .shop-title { font-weight: bold; margin-bottom: 8px; color: #d29922; font-size: 13px; text-transform: uppercase; }
        .shop-item { display: flex; justify-content: space-between; align-items: center; background: #2d333b; padding: 8px 10px; margin-bottom: 6px; border-radius: 6px; font-size: 13px; }
        .buy-btn { background: #238636; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-weight: bold; flex-shrink: 0; }
    </style>
</head>
<body>

<div class="container">
    <a href="/" class="back-link">← На главную</a>
    <h2>🏎️ Спид-Дрифт</h2>
    
    <div class="stats-top">
        <div class="stat-card">💨 Очки дрифта: <span id="drift_pts">0</span></div>
        <div class="stat-card">💰 Деньги: <span id="money">0</span> 🪙</div>
    </div>
    
    <div class="status-box">
        <div>Скорость: <span id="speed">60</span> км/ч</div>
        <div>Нитро-ускоритель: <span id="nitro_val">100</span>%</div>
        <div class="bar-container"><div class="bar" id="nitro_bar" style="width: 100%; background: #f85149;"></div></div>
    </div>

    <div class="game-box">
        <div class="alert" id="drift_alert">⚠️ Ручник наготове. Не переборщи со скоростью в повороте!</div>
        <div>🚗 Тачка: <span id="car_name">Стоковый Седан</span></div>
    </div>

    <button class="btn drift-btn" onclick="makeDrift()">🔥 Войти в крутой занос</button>

    <div class="shop-box">
        <div class="shop-title">🛒 Автомастерская:</div>
        <div class="shop-item"><span>Улучшить подвеску (+ множитель)</span> <button class="buy-btn" onclick="buy('mult', 50)">50 🪙</button></div>
        <div class="shop-item"><span>Спортивный турбо-наддув</span> <button class="buy-btn" onclick="buy('speed', 40)">40 🪙</button></div>
        <div class="shop-item"><span>Купить спорткар GT</span> <button class="buy-btn" onclick="buy('car', 150)">150 🪙</button></div>
    </div>
</div>

<script>
let g = { pts: 0, money: 0, speed: 60, nitro: 100, mult: 1, carLevel: 1 };

function update() {
    document.getElementById("drift_pts").innerText = g.pts;
    document.getElementById("money").innerText = g.money;
    document.getElementById("speed").innerText = g.speed;
    document.getElementById("nitro_val").innerText = g.nitro;
    document.getElementById("nitro_bar").style.width = g.nitro + "%";
    
    let car = "Стоковый Седан";
    if (g.carLevel === 2) car = "Заряженный Спринтер GT";
    if (g.carLevel >= 3) car = "Гиперкар Apex V8";
    document.getElementById("car_name").innerText = car;
}

function makeDrift() {
    if (g.nitro >= 20) {
        g.nitro -= 20;
        let roll = Math.random();
        
        if (roll < 0.3) {
            // Неудача: занос сорвался, вылет в кювет
            let penalty = Math.floor(15 * g.mult);
            g.pts = Math.max(0, g.pts - penalty);
            document.getElementById("drift_alert").innerText = "💥 Краш! Машину занесло в отбойник, минус очки дрифта (-" + penalty + ")!";
        } else if (roll < 0.45) {
            // Неудача: перегрев резины
            document.getElementById("drift_alert").innerText = "💨 Срыв сцепления! Резина задымилась, очки не засчитаны.";
        } else {
            // Удачный дрифт
            let gainedPts = Math.floor((Math.random() * 60 + 30) * g.mult);
            let gainedMoney = Math.floor(gainedPts / 4);
            g.pts += gainedPts;
            g.money += gainedMoney;
            document.getElementById("drift_alert").innerText = "🔥 Чистый дрифт! Очки: +" + gainedPts + " | Монеты: +" + gainedMoney;
        }
        update();
    } else {
        document.getElementById("drift_alert").innerText = "💨 Нитро на нуле! Охлаждаем турбину...";
        setTimeout(() => { g.nitro = 100; update(); document.getElementById("drift_alert").innerText = "⚡ Нитро в баке, погнали!"; }, 1200);
    }
}

function buy(type, cost) {
    if (g.money >= cost) {
        g.money -= cost;
        if (type === 'mult') g.mult += 1;
        else if (type === 'speed') g.speed += 40;
        else if (type === 'car') { g.carLevel++; g.mult += 2; g.speed += 80; }
        update();
        document.getElementById("drift_alert").innerText = "✅ Апгрейд успешно установлен!";
    } else {
        document.getElementById("drift_alert").innerText = "❌ Не хватает денег!";
    }
}

update();
</script>
</body>
</html>
"""
import os
os.makedirs("speed_drift", exist_ok=True)
with open("speed_drift/index.html", "w", encoding="utf-8") as f: f.write(html_content)
print("ДРИФТ ОБНОВЛЕН (УСПЕХИ И АВАРИИ ДОБАВЛЕНЫ)")
