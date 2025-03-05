from library_api import create_app

# Створення додатку
app = create_app()

# Безпосередній запуск додатку, якщо скрипт виконується як основний
if __name__ == '__main__':
    # Режим налагодження
    app.run(debug=True, host='0.0.0.0', port=5000)