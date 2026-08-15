import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Убираем старую кривую вставку, если она осталась
html = re.sub(r'<!-- Новые игры -->.*?(?=</body>|</html>|$)', '', html, flags=re.DOTALL)

# Ищем любую существующую карточку на странице (например, catcher или stone), чтобы понять окружение
match = re.search(r'(<a[^>]*href=["\'][^"\']*catcher/?["\'][^>]*>.*?</a>)', html, re.DOTALL | re.IGNORECASE)
if not match:
    # Если catcher не найден, ищем любую другую ссылку-карточку
    match = re.search(r'(<a[^>]*class=["\'][^"\']*card[^"\']*["\'][^>]*>.*?</a>)', html, re.DOTALL | re.IGNORECASE)

if match:
    template_card = match.group(1)

    new_games = [
        ("games/snake.html", "Неоновая Змейка", "🐍"),
        ("games/space.html", "Космический Тир", "🚀"),
        ("games/pong.html", "Кибер Понг", "🏓"),
        ("games/memory.html", "Матрица Памяти", "🧩"),
        ("games/game2048.html", "Мини 2048", "📦"),
        ("games/math.html", "Мат. Блиц", "➕"),
        ("games/coin.html", "Орел или Решка", "🪙"),
        ("games/picker.html", "Генератор Цветов", "🎨"),
        ("games/tapspeed.html", "Скорость Тапа", "⚡"),
    ]

    cards_html = "\n    <!-- Новые игры -->\n"
    for href, title, icon in new_games:
        card_html = f'''    <a href="{href}" class="card">
        <div class="icon">{icon}</div>
        <div class="title">{title}</div>
    </a>\n'''
        cards_html += card_html

    # Вставляем новые карточки сразу после последней найденной карточки на странице
    last_card_pos = html.rfind(template_card)
    insert_pos = last_card_pos + len(template_card)
    html = html[:insert_pos] + "\n" + cards_html + html[insert_pos:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Карточки успешно встроены в сетку игр!")
else:
    print("Ошибка: не удалось найти структуру карточек в index.html")
