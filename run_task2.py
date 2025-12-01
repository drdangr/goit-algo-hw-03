#!/usr/bin/env python3
"""
Скрипт для перевірки та встановлення необхідних залежностей.
"""

import subprocess
import sys


def check_and_install_dependencies():
    """
    Перевіряє наявність потрібних пакетів та встановлює їх за необхідності.
    """
    try:
        import matplotlib
        print("✓ matplotlib вже встановлений")
    except ImportError:
        print("✗ matplotlib не знайдено. Встановлюю...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "matplotlib>=3.5.0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✓ matplotlib успішно встановлений")
        except subprocess.CalledProcessError:
            print("✗ Не вдалося встановити matplotlib")
            print("Спробуйте встановити вручну: pip install matplotlib")
            sys.exit(1)


if __name__ == "__main__":
    check_and_install_dependencies()
    print("\nВсі залежності готові! Запускаю програму...\n")
    
    # Імпортуємо та запускаємо основний скрипт
    from task_02_v03_1 import main
    main()
