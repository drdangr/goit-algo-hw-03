import math
import sys
import subprocess
import os
from typing import List, Tuple

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Помилка: matplotlib не встановлений.")
    print("Встановлюю matplotlib...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "matplotlib>=3.5.0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        import matplotlib.pyplot as plt
        print("✓ matplotlib успішно встановлений\n")
    except Exception as e:
        print(f"✗ Не вдалося встановити matplotlib: {e}")
        print("Спробуйте встановити вручну: pip install matplotlib")
        sys.exit(1)

Line = Tuple[float, float, float, float]
OUTPUT_DIR = "task_02_koch_snowflake"


def koch_segment(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    level: int,
    lines: List[Line],
) -> None:
    """
    Рекурсивно будує один відрізок кривої Коха.
    Якщо level == 0 — просто додаємо відрізок (x1, y1) → (x2, y2).
    """
    if level == 0:
        lines.append((x1, y1, x2, y2))
        return

    dx = (x2 - x1) / 3
    dy = (y2 - y1) / 3

    # Точки A, B, D, E на прямій
    xA, yA = x1, y1
    xB, yB = x1 + dx, y1 + dy
    xD, yD = x1 + 2 * dx, y1 + 2 * dy
    xE, yE = x2, y2

    # Обчислюємо вершину "зубця" C (поворот на -60° назовні)
    cos60 = 0.5
    sin60 = math.sqrt(3) / 2

    xC = xB + dx * cos60 + dy * sin60
    yC = yB - dx * sin60 + dy * cos60

    # Рекурсивно опрацьовуємо 4 частини
    koch_segment(xA, yA, xB, yB, level - 1, lines)
    koch_segment(xB, yB, xC, yC, level - 1, lines)
    koch_segment(xC, yC, xD, yD, level - 1, lines)
    koch_segment(xD, yD, xE, yE, level - 1, lines)


def draw_koch_snowflake(level: int, save_to_file: bool = True) -> None:
    """
    Будує сніжинку Коха для заданого рівня рекурсії.
    """
    lines: List[Line] = []

    # Початковий рівносторонній трикутник
    size = 300.0
    xA, yA = 0.0, 0.0
    xB, yB = size, 0.0
    xC, yC = size / 2, size * math.sqrt(3) / 2

    koch_segment(xA, yA, xB, yB, level, lines)
    koch_segment(xB, yB, xC, yC, level, lines)
    koch_segment(xC, yC, xA, yA, level, lines)

    xs = []
    ys = []
    for x1, y1, x2, y2 in lines:
        xs.extend([x1, x2])
        ys.extend([y1, y2])

    plt.figure(figsize=(8, 8))

    # Лінії
    for x1, y1, x2, y2 in lines:
        plt.plot([x1, x2], [y1, y2], color="b")

    # Заливка (опціонально, щоб було красиво)
    plt.fill(xs, ys, color="c", alpha=0.2)

    plt.axis("equal")
    plt.title(f"Сніжинка Коха (рівень рекурсії: {level})")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.2)

    plt.show()

    if save_to_file:
        # Створюємо папку, якщо вона не існує
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = os.path.join(OUTPUT_DIR, f"koch_snowflake_level_{level}.png")
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Графік збережено в файл: {filename}")
        plt.close()
    else:
        try:
            plt.show()
        except Exception as e:
            print(f"Не можу відобразити графічне вікно: {e}")
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            filename = os.path.join(OUTPUT_DIR, f"koch_snowflake_level_{level}.png")
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            print(f"Графік збережено в файл: {filename}")


def main() -> None:
    """
    Запитує у користувача рівень рекурсії та малює сніжинку Коха.
    Працює в циклі, поки користувач не натисне Enter без введення числа.
    """
    while True:
        level_str = input(
            "Введіть рівень рекурсії (ціле число від 0 до 7)\n"
            "Або натисніть Enter без введення, щоб вийти: "
        )

        # Порожній рядок — вихід з програми
        if level_str.strip() == "":
            print("Вихід з програми.")
            break

        try:
            level = int(level_str)
        except ValueError:
            print("Потрібно ввести ціле число. Спробуйте ще раз.\n")
            continue

        if level < 0 or level > 7:
            print("Рівень рекурсії має бути від 0 до 7. Спробуйте ще раз.\n")
            continue

        print(f"Генерую сніжинку Коха з рівнем рекурсії {level}...")
        draw_koch_snowflake(level, save_to_file=True)
        print()  # Порожній рядок для зручності виводу

if __name__ == "__main__":
    main()