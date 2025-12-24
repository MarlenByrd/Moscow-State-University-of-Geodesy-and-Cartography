#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def main():
    input_file = Path("ppp_pride")

    if not input_file.exists():
        print(f"❌ Файл не найден: {input_file.resolve()}")
        sys.exit(1)

    heights = []

    with input_file.open() as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            # берём только строки, где есть минимум 5 чисел
            if len(parts) < 5:
                continue

            if not all(is_float(p) for p in parts[:5]):
                continue

            # parts[4] — Height по твоему формату
            heights.append(float(parts[4]))

    if not heights:
        print("❌ Не удалось извлечь значения Height")
        sys.exit(1)

    heights = pd.Series(heights)

    print(f"✔ Прочитано значений Height: {len(heights)}")

    print("\n📊 Height statistics:")
    print(heights.describe())

    # ===== гистограмма =====
    plt.figure(figsize=(10, 6))
    plt.hist(heights, bins=50, edgecolor="black")
    plt.xlabel("Height, m")
    plt.ylabel("Count")
    plt.title("PPP Height distribution")
    plt.grid(True)

    output = Path("ppp_pride_height.png")
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\n✅ Готово: {output.resolve()}")


if __name__ == "__main__":
    main()
