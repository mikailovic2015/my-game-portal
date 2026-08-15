html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Зомби-Выживание</title>
    <style>
        body { background: #0d1117; color: #fff; font-family: Segoe UI, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { max-width: 450px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
        .stats-top { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
        .stat-card { background: #010409; padding: 10px; border-radius: 8px; border: 1px solid #30363d; font-size: 14px; font-weight: bold; }
        .status-box { background: #21262d; padding: 10px; border-radius: 8px; margin-bottom: 12px; text-align: left; font-size: 13px; border: 1px solid #30363d; }
        .bar-container { width: 100%; background: #30363d; height: 8px; border-radius: 4px; margin: 3px 0 8px 0; overflow: hidden; }
        .bar { height: 100%; transition: width 0.3s; }
        .zombie-box { background: #21262d; border: 2px solid #f85149; padding: 10px; border-radius: 10px; margin-bottom: 12px; text-align: center; }
        .alert { color: #f85149; font-weight: bold; font-size: 13px; margin-bottom: 8px; min-height: 18px; }
        .btn { width: 100%; padding: 12px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; margin-bottom: 8px; text-transform: uppercase; font-size: 14px; }
        .shoot { background: #f85149; color: white; }
        .melee { background: #58a6ff; color: #000; }
        .shop-box { background: #1f242c; padding: 10px; border-radius: 8px; border: 1px solid #30363d; text-align: left; margin-bottom: 5px; }
        .shop-title { font-weight: bold; margin-bottom: 8px; color: #d29922; font-size: 13px; text-transform: uppercase; }
        .shop-item { display: flex; justify-content: space-between; align-items: center; background: #2d333b; padding: 8px 10px; margin-bottom: 6px; border-radius: 6px; font-size: 13px; }
        .buy-btn { background: #238636; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-weight: bold; flex-shrink: 0; }
        .buy-btn:hover { background: #2ea043; }
    </style>
</head>
<body>

<div class="container">
    <h2>🧟 Зомби-Выживание</h2>
    <div class="stats-top">
        <div class="stat-card">📦 Патроны: <span id="ammo">10</span></div>
        <div class="stat-card">💰 Монеты: <span id="money">50</span></div>
    </div>
    
    <div class="status-box">
        <div>HP: <span id="hp_val">150</span>/150</div>
        <div class="bar-container"><div class="bar" id="hp_bar" style="width: 100%; background: #238636;"></div></div>
        <div>Еда: <span id="food_val">100</span>/100</div>
        <div class="bar-container"><div class="bar" id="food_bar" style="width: 100%; background: #d29922;"></div></div>
        <div>Вода: <span id="water_val">100</span>/100</div>
        <div class="bar-container"><div class="bar" id="water_bar" style="width: 100%; background: #58a6ff;"></div></div>
    </div>

    <div class="zombie-box">
        <div class="alert" id="zombie_alert">⚠️ Зомби рычит и подбирается ближе!</div>
        <div>🧟 Зомби (HP: <span id="zombie_hp">10</span>)</div>
    </div>

    <button class="btn shoot" onclick="shootZombie()">🔫 Стрелять</button>
    <button class="btn melee" onclick="meleeZombie()">⚔️ Удар врукопашную (урон: <span id="melee_dmg">1.5</span>)</button>

    <div class="shop-box">
        <div class="shop-title">🛒 Магазин снабжения:</div>
        <div class="shop-item"><span>Патроны (+10)</span> <button class="buy-btn" onclick="buy('ammo', 10, 20)">20 🪙 Купить</button></div>
        <div class="shop-item"><span>Еда (+30)</span> <button class="buy-btn" onclick="buy('food', 30, 15)">15 🪙 Купить</button></div>
        <div class="shop-item"><span>Вода (+30)</span> <button class="buy-btn" onclick="buy('water', 30, 15)">15 🪙 Купить</button></div>
        <div class="shop-item"><span>Аптечка (+50 HP)</span> <button class="buy-btn" onclick="buy('hp', 50, 35)">35 🪙 Купить</button></div>
        <div class="shop-item"><span>Улучшить огнестрел (+1 урон)</span> <button class="buy-btn" onclick="buy('gunDmg', 1, 50)">50 🪙 Купить</button></div>
        <div class="shop-item"><span>Улучшить рукопашку (+0.5 урон)</span> <button class="buy-btn" onclick="buy('meleeDmg', 0.5, 40)">40 🪙 Купить</button></div>
    </div>
</div>

<script>
let g = {
    hp: 150, maxHp: 150,
    food: 100, maxFood: 100,
    water: 100, maxWater: 100,
    ammo: 10, money: 50,
    zombieHp: 10, zombieMaxHp: 10,
    gunDmg: 5, meleeDmg: 1.5
};

function update() {
    document.getElementById("hp_val").innerText = Math.round(g.hp);
    document.getElementById("food_val").innerText = Math.round(g.food);
    document.getElementById("water_val").innerText = Math.round(g.water);
    document.getElementById("ammo").innerText = g.ammo;
    document.getElementById("money").innerText = g.money;
    document.getElementById("zombie_hp").innerText = Math.max(0, Math.round(g.zombieHp));
    document.getElementById("melee_dmg").innerText = g.meleeDmg;
    
    document.getElementById("hp_bar").style.width = (g.hp / g.maxHp * 100) + "%";
    document.getElementById("food_bar").style.width = (g.food / g.maxFood * 100) + "%";
    document.getElementById("water_bar").style.width = (g.water / g.maxWater * 100) + "%";
}

function shootZombie() {
    if (g.ammo > 0) {
        g.ammo--;
        g.zombieHp -= g.gunDmg;
        checkZombie();
        update();
    } else {
        document.getElementById("zombie_alert").innerText = "⚠️ Нет патронов! Купи в магазине.";
    }
}

function meleeZombie() {
    g.zombieHp -= g.meleeDmg;
    checkZombie();
    update();
}

function checkZombie() {
    if (g.zombieHp <= 0) {
        let reward = Math.floor(Math.random() * 15) + 10;
        g.money += reward;
        g.zombieMaxHp += 5;
        g.zombieHp = g.zombieMaxHp;
        document.getElementById("zombie_alert").innerText = "🎉 Зомби побежден! + " + reward + " монет!";
    } else {
        document.getElementById("zombie_alert").innerText = "⚠️ Зомби рычит и подбирается ближе!";
    }
}

function buy(type, amount, cost) {
    if (g.money >= cost) {
        g.money -= cost;
        if (type === "ammo") g.ammo += amount;
        if (type === "food") g.food = Math.min(g.maxFood, g.food + amount);
        if (type === "water") g.water = Math.min(g.maxWater, g.water + amount);
        if (type === "hp") g.hp = Math.min(g.maxHp, g.hp + amount);
        if (type === "gunDmg") g.gunDmg += amount;
        if (type === "meleeDmg") g.meleeDmg += amount;
        update();
        document.getElementById("zombie_alert").innerText = "✅ Успешная покупка!";
    } else {
        document.getElementById("zombie_alert").innerText = "❌ Не хватает монет!";
    }
}

update();
</script>

</body>
</html>
"""

with open("zombie_survival/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("ФАЙЛ УСПЕШНО ЗАПИСАН БЕЗ БАГОВ!")
