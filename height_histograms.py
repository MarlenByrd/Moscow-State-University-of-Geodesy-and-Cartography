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


def read_heights(filepath):
    """
    Надёжно извлекает колонку Height (5-е число в строке)
    из PPP / PPK файлов с плавающим форматом
    """
    heights = []

    with open(filepath) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 5:
                continue

            if not all(is_float(p) for p in parts[:5]):
                continue

            heights.append(float(parts[4]))

    return pd.Series(heights)


def main():
    # ===== файлы =====
    f_ppp_pride = Path("ppp_pride")
    f_ppp_rtklib = Path("ppp_rtklib.pos")
    f_ppk_rtklib = Path("ppk_rtklib.pos")

    for f in [f_ppp_pride, f_ppp_rtklib, f_ppk_rtklib]:
        if not f.exists():
            print(f"❌ Файл не найден: {f}")
            sys.exit(1)

    # ===== чтение =====
    h_ppp_pride = read_heights(f_ppp_pride)
    h_ppp_rtklib = read_heights(f_ppp_rtklib)
    h_ppk_rtklib = read_heights(f_ppk_rtklib)

    n = min(len(h_ppp_pride), len(h_ppp_rtklib), len(h_ppk_rtklib))

    h_ppp_pride = h_ppp_pride.iloc[:n]
    h_ppp_rtklib = h_ppp_rtklib.iloc[:n]
    h_ppk_rtklib = h_ppk_rtklib.iloc[:n]

    # ===== разности =====
    d_ppp = h_ppp_pride - h_ppp_rtklib
    d_ppp_ppk = h_ppp_rtklib - h_ppk_rtklib

    # ===== гистограммы =====
    plt.figure(figsize=(10, 6))
    plt.hist(d_ppp, bins=50, edgecolor="black")
    plt.xlabel("Δh, m")
    plt.ylabel("Count")
    plt.title("PPP(PRIDE) − PPP(RTKLIB)")
    plt.grid(True)
    plt.savefig("hist_ppp_pride_vs_rtklib.png", dpi=300, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.hist(d_ppp_ppk, bins=50, edgecolor="black")
    plt.xlabel("Δh, m")
    plt.ylabel("Count")
    plt.title("PPP(RTKLIB) − PPK(RTKLIB)")
    plt.grid(True)
    plt.savefig("hist_ppp_vs_ppk_rtklib.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Гистограммы построены:")
    print(" - hist_ppp_pride_vs_rtklib.png")
    print(" - hist_ppp_vs_ppk_rtklib.png")


if __name__ == "__main__":
    main()

