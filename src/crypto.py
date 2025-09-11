from pathlib import Path
import base64
import re


def load_pem_key(path: str | Path):
    """Загружает PEM-ключ и возвращает (exp, n)."""
    with open(path, "r", encoding="utf-8") as f:
        pem = f.read()

    match = re.search(r"-----BEGIN.*?-----(.*?)-----END.*?-----", pem, re.S)
    if not match:
        raise ValueError("Некорректный PEM-ключ")

    b64_data = match.group(1).strip()
    raw = base64.b64decode(b64_data)

    parts = raw.decode().split(",")
    if len(parts) != 2:
        raise ValueError("Некорректное содержимое PEM")

    exp = int(parts[0])
    n = int(parts[1])
    return exp, nпше


def encrypt_file(public_key_path: str | Path, input_file: str | Path, output_file: str | Path):
    """Шифрует файл блоками с использованием публичного ключа (PEM)."""
    e, n = load_pem_key(public_key_path)

    block_size = (n.bit_length() // 8) - 1
    encrypted_block_size = (n.bit_length() + 7) // 8

    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        while chunk := fin.read(block_size):
            m = int.from_bytes(chunk, byteorder="big")
            if m >= n:
                raise ValueError("Блок данных больше модуля n, увеличьте размер ключа")

            c = pow(m, e, n)
            fout.write(c.to_bytes(encrypted_block_size, byteorder="big"))


def decrypt_file(private_key_path: str | Path, encrypted_file: str | Path, output_file: str | Path):
    """Дешифрует файл блоками с использованием приватного ключа (PEM)."""
    d, n = load_pem_key(private_key_path)

    encrypted_block_size = (n.bit_length() + 7) // 8

    with open(encrypted_file, "rb") as fin, open(output_file, "wb") as fout:
        while chunk := fin.read(encrypted_block_size):
            c = int.from_bytes(chunk, byteorder="big")
            m = pow(c, d, n)
            data = m.to_bytes((m.bit_length() + 7) // 8, byteorder="big")
            fout.write(data)
