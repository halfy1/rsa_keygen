import random
import math
import base64
from pathlib import Path


def is_prime(n, k=40):
    """Тест Миллера-Рабина"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = mod_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = mod_pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def mod_pow(base, exp, mod):
    """Возведение в степень по модулю"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:  # если бит = 1
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


def gen_prime(bit_length=1024):
    """Генерация простого числа заданной битовой длины"""
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1))
        candidate |= 1
        if is_prime(candidate):
            return candidate


def egcd(a, b):
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def modinv(a, m):
    """Обратное по модулю"""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('Нет обратного элемента')
    return x % m


def generate_keys(bit_length=1024):
    """Генерация пары ключей RSA"""
    p = gen_prime(bit_length // 2)
    q = gen_prime(bit_length // 2)
    while p == q:
        q = gen_prime(bit_length // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2

    d = modinv(e, phi)
    return (e, n), (d, n)


def to_pem(key_type, numbers: tuple) -> str:
    """Сериализация ключа в PEM-подобный формат"""
    key_bytes = f"{numbers[0]},{numbers[1]}".encode()
    b64 = base64.encodebytes(key_bytes).decode().replace("\n", "")
    return f"-----BEGIN {key_type} KEY-----\n{b64}\n-----END {key_type} KEY-----\n"


def save_key(path: Path, key_type: str, numbers: tuple):
    pem = to_pem(key_type, numbers)
    with open(path, "w") as f:
        f.write(pem)


def generate_key_pair(keys_dir: str, bit_length=1024, name="rsa", force=False):
    """Генерация и сохранение ключей в файлы"""
    keys_dir = Path(keys_dir)
    keys_dir.mkdir(parents=True, exist_ok=True)

    public, private = generate_keys(bit_length)

    private_path = keys_dir / f"{name}_private.pem"
    public_path = keys_dir / f"{name}_public.pem"

    if not force and (private_path.exists() or public_path.exists()):
        raise FileExistsError(
            "Файлы ключей уже существуют, используйте --force для перезаписи")

    save_key(private_path, "RSA PRIVATE", private)
    save_key(public_path, "RSA PUBLIC", public)

    return private_path, public_path
