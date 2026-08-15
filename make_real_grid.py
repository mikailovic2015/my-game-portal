with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Блок красивых карточек в точном стиле сайта
grid_cards = """
    <a href="games/snake.html" class="card">
        <div class="icon">🐍</div>
        <div class="title">Неоновая Змейка</div>
    </a>
    <a href="games/space.html" class="card">
        <div class="icon">🚀</div>
        <div class="title">Космический Тир</div>
    </a>
    <a href="games/pong.html" class="card">
        <div class="icon">🏓</div>
        <div class="title">Кибер Понг</div>
    </a>
    <a href="games/memory.html" class="card">
        <div class="icon">🧩</div>
        <div class="title">Матрица Памяти</div>
    </a>
    <a href="games/game2048.html" class="card">
        <div class="icon">📦</div>
        <div class="title">Мини 2048</div>
    </a>
    <a href="games/math.html" class="card">
        <div class="icon">➕</div>
        <div class="title">Мат. Блиц</div>
    </a>
    <a href="games/coin.html" class="card">
        <div class="icon">🪙</div>
        <div class="title">Орел или Решка</div>
    </a>
    <a href="games/picker.html" class="card">
        <div class="icon">🎨</div>
        <div class="title">Генератор Цветов</div>
    </a>
    <a href="games/tapspeed.html" class="card">
        <div class="icon">⚡</div>
        <div class="title">Скорость Тапа</div>
    </a>
"""

# Вставляем перед закрывающим тегом контейнера игр или перед body
if '</body>' in content:
    # Найдем, где заканчиваются остальные карточки, и вставим туда
    if 'Catcher' in content:
        # Вставим сразу после карточки Catcher для теста или перед закрытием body
        content = content.replace('</body>', grid_cards + '\n</body>')
    else:
        content = content.replace('</body>', grid_cards + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Готово!")
