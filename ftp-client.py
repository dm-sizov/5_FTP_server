import socket

HOST = 'localhost'  # Адрес сервера
PORT = 6666  # Порт сервера

# Основной цикл клиента
while True:
    request = input('Введите команду (или "exit" для выхода): ')  # Ввод команды от пользователя
    if request.lower() == 'exit':
        break  # Выход из цикла, если команда "exit"

    sock = socket.socket()  # Создаем сокет
    sock.connect((HOST, PORT))  # Подключаемся к серверу

    sock.send(request.encode())  # Отправляем запрос на сервер

    response = sock.recv(1024).decode()  # Получаем ответ от сервера
    print("Ответ от сервера:", response)  # Выводим ответ

    sock.close()  # Закрываем соединение
