with open("server.js", "r", encoding="utf-8") as f:
    srv = f.read()

# Выведем кусок кода, отвечающий за /api/login
import re
match = re.search(r"app\.post\('/api/login'.*?\});", srv, re.DOTALL)
if match:
    print("НАШЕЛ РОУТ ЛОГИНА НА СЕРВЕРЕ:")
    print(match.group(0))
else:
    print("Роут /api/login не найден в стандартном виде, ищем аппи...")
    for line in srv.splitlines():
        if "login" in line.lower():
            print(line)
