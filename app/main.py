from fastapi import FastAPI
from app.router import authenication, users, publications


app = FastAPI()
app.include_router(authenication.router)
app.include_router(users.router)
app.include_router(publications.router)

# Совместим ли класс юзера с аунтефикацией

# Проблема с получением пользователя
# Регистрация и вход
# Должны ли создаваться теги при создании публикаций

# Тест для crud публикаций
# crud для тегов
# тест crud тегов

# нужна ли ветка crud
# Обновить ли ветку database
