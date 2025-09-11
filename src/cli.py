import click
import os
from pathlib import Path


@click.group()
def cli():
    """RSA Key Generator and Encryption Tool"""
    pass


@cli.command()
@click.option("-p", "--path-dir", default="keys",
              type=click.Path(file_okay=False),
              help="Директория для сохранения ключей")
@click.option("-s", "--size", default=2048,
              type=int,
              help="Размер ключа в битах")
@click.option("-n", "--name", default="id_rsa",
              help="Базовое имя для ключей")
@click.option("-f", "--force", is_flag=True,
              help="Перезаписать существующие ключи")
def generate(path_dir, size, name, force):
    """Генерирует пару RSA ключей"""
    from src.rsa import generate_key_pair

    keys_dir = Path(path_dir)
    keys_dir.mkdir(parents=True, exist_ok=True)

    try:
        private_path, public_path = generate_key_pair(
            keys_dir, size, name, force
        )
        click.echo(f"Ключи созданы в: {keys_dir}")
        click.echo(f"Приватный: {private_path.name}")
        click.echo(f"Публичный: {public_path.name}")

    except FileExistsError as e:
        click.secho(f" {e}", fg="yellow")
        click.echo("Используйте --force для перезаписи")
        raise click.Abort()
    except Exception as e:
        click.secho(f"Ошибка: {e}", fg="red")
        raise click.Abort()


@cli.command()
@click.argument("public_key_path",
                type=click.Path(exists=True, dir_okay=False))
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", default=None,
              help="Имя выходного файла, default = encrypted/имя_файла.enc")
def encrypt(public_key_path, input_file, output):
    """Шифрует файл с помощью публичного ключа"""
    from src.crypto import encrypt_file

    if output is None:
        input_path = Path(input_file)
        output_file = Path("encrypted") / f"{input_path.name}.enc"
    else:
        output_file = Path(output)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        encrypt_file(public_key_path, input_file, output_file)
        click.echo(f"Файл зашифрован: {output_file}")
    except Exception as e:
        click.secho(f"Ошибка шифрования: {e}", fg="red")
        raise click.Abort()


@cli.command()
@click.argument("private_key_path",
                type=click.Path(exists=True, dir_okay=False))
@click.argument("encrypted_file", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", default=None,
              help="Имя выходного файла, default = decrypted/имя_файла.dec")
def decrypt(private_key_path, encrypted_file, output):
    """Дешифрует файл с помощью приватного ключа"""
    from src.crypto import decrypt_file

    if output is None:
        input_path = Path(encrypted_file)
        output_file = Path("decrypted") / f"{input_path.name}.dec"
    else:
        output_file = Path(output)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        decrypt_file(private_key_path, encrypted_file, output_file)
        click.echo(f"Файл дешифрован: {output_file}")
    except Exception as e:
        click.secho(f"Ошибка дешифрования: {e}", fg="red")
        raise click.Abort()


def main():
    cli()


if __name__ == "__main__":
    main()
