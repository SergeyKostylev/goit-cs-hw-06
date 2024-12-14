# Вебдодаток без вебфреймворку

Цей проект реалізує простий вебдодаток, що включає дві HTML-сторінки (index.html та message.html), обробку статичних ресурсів, а також роботу з формою на сторінці `message.html`. Вебдодаток також містить обробку помилок 404 та інтеграцію з Socket-сервером для збереження даних у базу даних MongoDB.

## Технічні вимоги

### Вебдодаток:
1. **Маршрутизація**:
   - `index.html`: головна сторінка.
   - `message.html`: сторінка з формою для вводу даних.
   - Якщо сторінка не знайдена, має бути повернута сторінка `error.html` (помилка 404).

2. **Статичні ресурси**:
   - `style.css` — файл стилів.
   - `logo.png` — логотип.

3. **HTTP-сервер**:
   - Сервер працює на порту 3000.
   - Обробка запитів за допомогою звичайного HTTP без використання вебфреймворків.

### Socket-сервер:
1. **Порт 5099**: Використовуємо для з'єднання з клієнтом.
2. Клієнт надсилає дані форми, через сокет для обробки.
3. **Обробка даних**:
   - Дані перевіряються на сервері та зберігаються у MongoDB.
   - Формат збереження даних у MongoDB: словник.

### Формат документа MongoDB:
```json
{
  "name": "Дмитро",
  "message": "Привіт чат",
  "time": "2024-12-14 20:21:53.690215"
}