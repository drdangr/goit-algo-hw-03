import sys
from pathlib import Path # Для роботи з файловими шляхами
import shutil # Для копіювання файлів

# я виррішив викорустати бібліотеку pathlib замість os для зручнішої роботи з шляхами 
# та shutil для копіювання файлів з збереженням метаданих.

# У цьому скрипті ми використовуємо клас Path з модуля pathlib.
# Основні методи та властивості, які мені потрібні:
# - Path(...)            — створюємо об’єкт шляху до файлу або теки.
# - iterdir()            — перебираємо всі елементи всередині теки.
# - is_dir() / is_file() — перевіряємо, чи є елемент текою або файлом.
# - suffix               — отримуємо розширення файлу (наприклад, ".txt").
# - name                  — отримуємо повну назву файлу з розширенням.
# - exists()             — перевіряємо, чи існує шлях.
# - mkdir()              — створюємо теку (за потреби з проміжними батьківськими).


def copy_file_to_extension_folder(file_path: Path, dest_root: Path) -> None:
    """
    Копіює один файл у піддиректорію за його розширенням.
    """
    # Визначаємо розширення файлу (без крапки)
    if file_path.suffix:
        ext_name = file_path.suffix[1:].lower()
    else:
        ext_name = "без_розширення"

    target_dir = dest_root / ext_name

    try:
        # Створюємо піддиректорію для цього розширення, якщо вона ще не існує
        target_dir.mkdir(parents=True, exist_ok=True)

        # Копіюємо файл, зберігаючи метадані (час зміни тощо)
        shutil.copy2(file_path, target_dir / file_path.name)
    #обробка можливих помилок доступу та інших помилок ОС    
    except PermissionError:
        print(f"Помилка доступу під час копіювання файлу: {file_path}")
    except OSError as error:
        print(f"Помилка копіювання файлу '{file_path}': {error}")


def copy_and_sort_files(src_dir: Path, dest_dir: Path) -> None:
    """
    Рекурсивно обходить теку src_dir і копіює всі файли
    до teки dest_dir, сортує їх за розширенням.
    """
    try:
        for item in src_dir.iterdir():
            if item.is_dir():
                # Якщо це тека — рекурсивно обходимо її
                copy_and_sort_files(item, dest_dir)
            elif item.is_file():
                # Якщо це файл — копіюємо його у відповідну піддиректорію
                copy_file_to_extension_folder(item, dest_dir)
    #обробка можливих помилок доступу та інших помилок ОС            
    except PermissionError:
        print(f"Помилка доступу до теки: {src_dir}")
    except OSError as error:
        print(f"Помилка роботи з файловою системою для '{src_dir}': {error}")


def main() -> None:
    """
    Точка входу в програму.
    Читає аргументи командного рядка та запускає рекурсивне копіювання.
    """
    if len(sys.argv) < 2:
        print("Будь ласка, вкажіть шлях до вихідної теки.")
        print("Використання: python task_01_v01.py <шлях_до_вихідної_теки> [шлях_до_теки_призначення]")
        sys.exit(1)

    src = Path(sys.argv[1])

    # Якщо друга тека не передана — використовуємо 'dist' за замовчуванням
    if len(sys.argv) >= 3:
        dest = Path(sys.argv[2])
    else:
        dest = Path("dist")

    if not src.exists() or not src.is_dir():
        print(f"Вихідна тека не існує або не є текою: {src}")
        sys.exit(1)

    try:
        # Створюємо теку призначення, якщо її немає
        dest.mkdir(parents=True, exist_ok=True)
    #обробка можливих помилок доступу та інших помилок ОС    
    except PermissionError:
        print(f"Неможливо створити теку призначення: {dest}")
        sys.exit(1)
    except OSError as error:
        print(f"Помилка під час створення теки призначення '{dest}': {error}")
        sys.exit(1)

    print(f"Копіюємо файли з '{src}' до '{dest}'...")
    copy_and_sort_files(src, dest)
    print("Готово. Файли скопійовано та відсортовано за розширенням.")


if __name__ == "__main__":
    main()