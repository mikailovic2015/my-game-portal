import os

file_path = 'zombie_survival/index.html' 

if not os.path.exists(file_path):
    print(f"Файл {file_path} не найден! Проверь путь.")
else:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    html_code = """
        <div class="shop-box" style="margin-top: 15px;">
            <div class="shop-title">💾 Управление сейвом:</div>
            <div style="display: flex; gap: 8px;">
                <button class="buy-btn" style="flex: 1; background: #2196F3;" onclick="downloadBackup()">Скачать бэкап</button>
                <button class="buy-btn" style="flex: 1; background: #FF9800;" onclick="restoreBackup()">Загрузить бэкап</button>
            </div>
            <input type="file" id="backupFile" style="display: none;" accept=".json" onchange="processRestore(event)">
        </div>
    """

    js_code = """
    <script>
    function downloadBackup() {
        let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(g));
        let dlAnchorElem = document.createElement('a');
        dlAnchorElem.setAttribute("href", dataStr);
        dlAnchorElem.setAttribute("download", "zombie_save.json");
        document.body.appendChild(dlAnchorElem);
        dlAnchorElem.click();
        dlAnchorElem.remove();
    }
    function restoreBackup() {
        document.getElementById('backupFile').click();
    }
    function processRestore(event) {
        let fileReader = new FileReader();
        if (event.target.files[0]) {
            fileReader.readAsText(event.target.files[0], "UTF-8");
            fileReader.onload = function(e) {
                try {
                    let parsed = JSON.parse(e.target.result);
                    if (parsed && typeof parsed.hp !== 'undefined') {
                        g = parsed;
                        update();
                        alert("✅ Бэкап успешно восстановлен!");
                    } else { alert("❌ Ошибка формата!"); }
                } catch(ex) { alert("❌ Ошибка!"); }
            };
        }
    }
    </script>
    """

    if "downloadBackup" not in content:
        content = content.replace("</div>\n</body>", html_code + "\n</body>")
        content = content.replace("</script>", js_code)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Готово! Обнови страницу в браузере.")
    else:
        print("Уже добавлено.")
