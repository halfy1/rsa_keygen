RSA Key Generator

Учебный проект: реализация генерации RSA-ключей, шифрования и дешифрования файлов **своими руками**, без использования готовых криптографических библиотек.

### Возможности

- Генерация пары RSA-ключей (public, private) в PEM-подобном формате
- Шифрование файлов с помощью публичного ключа
- Дешифрование файлов с помощью приватного ключа
- Управление через CLI на базе Click

### Установка

```bash
git clone https://github.com/halfy1/rsa_keygen
cd rsa_keygen
python -m venv venv

#Linux/Mac
source venv/bin/activate
#Windows
venv\Scripts\activate

pip install -r requirements.txt

#Проверка работоспособности
python -m src.cli --help
```

### Генерация ключей
```bash
python -m src.cli generate -s 1024 -n demo
``` 
#### Создаст файлы:
- `keys/demo_private.pem`
- `keys/demo_public.pem`
#### Флаги:
- `-f, --force` - перезаписать ключи
- `-p, --path-dir` - Директория сохранения ключей. `default=keys/`
- `-s, -size` - размер ключа в битах. `default=2048`
- `-n, --name` - название ключей, `default=it_rsa`

### Шифрование
```bash
python -m src.cli encrypt keys/demo_public.pem message.txt -o encrypted.bin`
```
#### Создаст файл
- `encrypted.bin`
#### Параметры
- `public_key_path` -  путь до публичного ключа
- `input_file` - путь до файла для шифрования
#### Флаги
- `-o, --output` - имя выходного файла. `default = encrypted/inpit_file.enc`

### Дешифрование
```bash
python -m src.cli decrypt keys/demo_private.pem encrypted.bin -o decrypted.txt
```
### Создаст файл
- `decrypted.txt`
### Параметры
- `private_key_path` - путь до приватного ключа
- `encrypted_file` - путь до файла для дешифрования
### Флаги
- `-o, --output` - имя выходного файла. `default = decrypted/input_file.dec`
- 
### Тестовый пример 
```bash
# 1. Сгенерировать ключи
python -m src.cli generate -s 512 -n test

# 2. Создать тестовый файл
echo "hello rsa" > msg.txt

# 3. Зашифровать
python -m src.cli encrypt keys/test_public.pem msg.txt -o enc.bin

# 4. Расшифровать
python -m src.cli decrypt keys/test_private.pem enc.bin -o dec.txt
```

### Структура проекта
```text
src/
  cli.py
  rsa.py
  crypto.py
requirements.txt
```
