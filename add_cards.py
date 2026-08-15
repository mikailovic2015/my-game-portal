with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Блок новых карточек в едином стиле интерфейса
new_cards_html = '''
    <!-- Новые игры -->
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
'''

if 'games/snake.html' not in content:
    # Ищем закрывающий тег сетки или хелпера перед концом файла
    if '</body>' in content:
        content = content.replace('</body>', new_cards_html + '\n</body>')
    else:
        content += new_cards_html

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Карточки игр успешно добавлены!")
else:
    print("Карточки уже добавлены ранее!")
