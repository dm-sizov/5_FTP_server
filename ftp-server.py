import socket
import os

# Определение рабочей директории
dirname = os.path.join(os.getcwd(), 'docs')


# Код обработки запросов от клиента
def process(req):
    global dirname
    command = req.split(' ', 1)  # Разделяем команду и оставшуюся часть (если есть)
    cmd = command[0].strip()

    if cmd == 'pwd':
        return dirname  # Возвращаем рабочую директорию
    elif cmd == 'ls':
        return '; '.join(os.listdir(dirname))  # Возвращаем содержимое директории
    elif cmd.startswith('cat '):  # Запрос на возврат содержимого файла
        filename = command[1].strip() if len(command) > 1 else ''
        return cat_file(filename)
    elif cmd.startswith('create '):  # Создание файла
        filename, contents = command[1].strip().split('|', 1)
        return create_file(filename, contents)
    elif cmd.startswith('delete '):  # Удаление файла
        filename = command[1].strip() if len(command) > 1 else ''
        return delete_file(filename)
    elif cmd.startswith('rename '):  # Переименовать файл
        oldname, newname = command[1].strip().split('|', 1)
        return rename_file(oldname, newname)
    elif cmd.startswith('mkdir '):  # Создание директории
        dirname = command[1].strip() if len(command) > 1 else ''
        return create_directory(dirname)
    elif cmd.startswith('rmdir '):  # Удаление директории
        dirname = command[1].strip() if len(command) > 1 else ''
        return remove_directory(dirname)
    else:
        return 'bad request'  # Если команда не распознана


# Функция для чтения содержимого файла
def cat_file(filename):
    filepath = os.path.join(dirname, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            return file.read()  # Возвращаем содержимое файла
    return 'File not found'


# Функция для создания файла
def create_file(filename, contents):
    filepath = os.path.join(dirname, filename)
    with open(filepath, 'w') as file:
        file.write(contents)  # Записываем содержимое в файл
    return 'File created'


# Функция для удаления файла
def delete_file(filename):
    filepath = os.path.join(dirname, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)  # Удаляем файл
        return 'File deleted'
    return 'File not found'


# Функция для переименования файла
def rename_file(oldname, newname):
    oldpath = os.path.join(dirname, oldname)
    newpath = os.path.join(dirname, newname)
    if os.path.isfile(oldpath):
        os.rename(oldpath, newpath)  # Переименуем файл
        return 'File renamed'
    return 'File not found'


# Функция для создания директории
def create_directory(dirname):
    path = os.path.join(dirname, dirname)
    try:
        os.makedirs(path)  # Создаем директорию
        return 'Directory created'
    except FileExistsError:
        return 'Directory already exists'


# Функция для удаления директории
def remove_directory(dirname):
    path = os.path.join(dirname, dirname)
    try:
        os.rmdir(path)  # Удаляем директорию
        return 'Directory deleted'
    except FileNotFoundError:
        return 'Directory not found'
    except OSError:
        return 'Directory is not empty'


# Определение порта
PORT = 6666
sock = socket.socket()
sock.bind(('', PORT))  # Привязываем сокет к порту
sock.listen()  # Начинаем слушать входящие соединения
print("Прослушиваем порт", PORT)

# Основной цикл сервера
while True:
    conn, addr = sock.accept()  # Принимаем входящее соединение
    print("Connected by", addr)

    request = conn.recv(1024).decode()  # Получаем запрос от клиента
    print("Request received:", request)

    response = process(request)  # Обрабатываем запрос
    conn.send(response.encode())  # Отправляем ответ клиенту
