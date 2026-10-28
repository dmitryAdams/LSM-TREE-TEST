#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Шаблон построения графика из CSV: линии или группированные столбцы.

ФОРМАТ CSV («длинная таблица»): одна строка = одна точка графика.
Столбцы (имена задаются в разделе 1):
    X_COL      значение параметра по оси X (число или текстовая категория)
    Y_COL      измеряемая величина
    SERIES_COL название серии (вариант, конфигурация и т.п.);
               каждой серии соответствует своя линия / свой цвет столбцов
    ERR_COL    (необязательно) величина погрешности для планок

ЗАПУСК (например, из папки paper/figures/src/):
    python plot_template.py входной.csv выходной.pdf
Пути в командной строке можно не передавать, тогда берутся INPUT_CSV и OUTPUT_PDF.

ЗАВИСИМОСТИ: pip install matplotlib pandas

Всё, что можно и нужно подгонять под свой результат, собрано в разделах 1-5
и помечено словом «КРУТИ». Раздел 6 (само построение) править обычно не нужно.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # рисуем в файл, без окна
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, ScalarFormatter
import pandas as pd


# =============================================================================
# 1. ДАННЫЕ
# =============================================================================
INPUT_CSV = "../../../code/bench/results/example.csv"   # КРУТИ: путь к данным
OUTPUT_PDF = "../01-introduction/example.pdf"           # КРУТИ: куда сохранить
CSV_SEP = ","        # КРУТИ: разделитель; для CSV из русского Excel обычно ";"

X_COL = "x"          # КРУТИ: имена столбцов в твоём CSV
Y_COL = "y"
SERIES_COL = "series"
ERR_COL = None       # КРУТИ: имя столбца с погрешностью или None, если её нет


# =============================================================================
# 2. ТИП ГРАФИКА И ПОГРЕШНОСТИ
# =============================================================================
KIND = "line"        # КРУТИ: "line" (линии с маркерами) или "bar" (группированные столбцы)
ERR_STYLE = "bars"   # КРУТИ: "bars" (усы) или "band" (полоса); "band" только для KIND="line"
BAR_GROUP_WIDTH = 0.8   # КРУТИ: для "bar": какую долю расстояния между группами занимают столбцы (0..1)


# =============================================================================
# 3. ПОДПИСИ И ПОРЯДОК
# =============================================================================
X_LABEL = "Параметр, ед."      # КРУТИ: подпись оси X (с единицами измерения)
Y_LABEL = "Величина, ед."      # КРУТИ: подпись оси Y (с единицами измерения)
TITLE = None                   # КРУТИ: заголовок над графиком; в статье обычно None,
                               # потому что есть \caption под рисунком

SERIES_LABELS = {}             # КРУТИ: красивые имена серий в легенде,
                               # например {"имя_в_csv": "Имя в легенде"}
SERIES_ORDER = None            # КРУТИ: порядок серий списком, например ["A", "B"]; None = как в файле
X_ORDER = None                 # КРУТИ: порядок значений X, если они текстовые; None = как в файле


# =============================================================================
# 4. ОСИ
# =============================================================================
LOG_X = False        # КРУТИ: логарифмическая ось X (удобна для 1, 2, 4, 8, ... потоков); только для KIND="line"
LOG_Y = False        # КРУТИ: логарифмическая ось Y (удобна, если значения различаются на порядки)
LOG_X_BASE = 10      # КРУТИ: основание логарифма для X (2 удобно для степеней двойки)
LOG_Y_BASE = 10
X_LIM = None         # КРУТИ: пределы осей, например (0, 100); None = автоматически
Y_LIM = None
Y_FROM_ZERO = True   # КРУТИ: начинать ось Y с нуля (если Y_LIM не задан и нет лога)
X_TICKS_FROM_DATA = True   # КРУТИ: подписи по X ровно в точках измерений
                           # (для линий с числовым X; при логарифме выводит обычные числа)
GRID = True          # КРУТИ: сетка


# =============================================================================
# 5. ВНЕШНИЙ ВИД
# =============================================================================
# Размер рисунка. При полях 2,5 см ширина текста на A4 около 16 см,
# поэтому ширина 16 даёт «на всю строку», а 7.8 помещается в одну колонку из двух.
FIG_WIDTH_CM = 16.0     # КРУТИ
FIG_HEIGHT_CM = 8.0     # КРУТИ

# Шрифты. Размеры подгоняй к шрифту статьи (у нас 12 pt): подписи и цифры чуть мельче.
FONT_SIZE = 10          # КРУТИ: основной размер (подписи осей, цифры)
LEGEND_FONT_SIZE = 9    # КРУТИ
# По умолчанию DejaVu Serif: он входит в matplotlib, поддерживает кириллицу и работает везде.
# КРУТИ: хочешь шрифт ближе к LaTeX-тексту, поставь ["CMU Serif"] (Computer Modern Unicode,
# его нужно установить в систему) или ["Times New Roman"].
# Если вместо русских букв появились квадраты или предупреждение «Glyph ... missing»,
# выбранный шрифт не содержит кириллицу. Не используй "Latin Modern Roman": кириллицы в нём нет.
FONT_FAMILY = ["DejaVu Serif"]
PDF_FONTTYPE = 42    # КРУТИ: 42 = TrueType (текст в PDF выделяется). Если pdf-просмотрщик
                     # пишет «Mismatch between font type and embedded font file» (бывает с .otf-шрифтами),
                     # поставь 3.

# Цвета (палитра Окабэ-Ито, различима при нарушениях цветового зрения),
# маркеры и стили линий по кругу для серий. Можно менять и удлинять.
COLORS = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9", "#000000"]  # КРУТИ
MARKERS = ["o", "s", "^", "D", "v", "P", "X"]                                              # КРУТИ
LINESTYLES = ["-", "--", "-.", ":", "-", "--", "-."]                                       # КРУТИ
LINE_WIDTH = 1.4        # КРУТИ: толщина линий
MARKER_SIZE = 5         # КРУТИ: размер маркеров
ERR_CAPSIZE = 3         # КРУТИ: длина «шапочек» на усах
BAND_ALPHA = 0.2        # КРУТИ: прозрачность полосы погрешности (ERR_STYLE="band")

# Легенда
LEGEND = True           # КРУТИ: показывать легенду
LEGEND_LOC = "best"     # КРУТИ: "best", "upper left", "lower right", ...
LEGEND_NCOL = 1         # КРУТИ: число столбцов в легенде
LEGEND_FRAME = False    # КРУТИ: рамка вокруг легенды


# =============================================================================
# 6. ПОСТРОЕНИЕ (обычно править не нужно)
# =============================================================================
def apply_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": FONT_FAMILY,
        "mathtext.fontset": "cm",
        "font.size": FONT_SIZE,
        "axes.labelsize": FONT_SIZE,
        "xtick.labelsize": FONT_SIZE,
        "ytick.labelsize": FONT_SIZE,
        "legend.fontsize": LEGEND_FONT_SIZE,
        "pdf.fonttype": PDF_FONTTYPE,  # способ вшивания шрифтов в PDF (см. раздел 5)
        "axes.unicode_minus": False, # обычный дефис вместо длинного минуса в числах
    })


def load_data():
    df = pd.read_csv(INPUT_CSV, sep=CSV_SEP)
    needed = [X_COL, Y_COL, SERIES_COL] + ([ERR_COL] if ERR_COL else [])
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise SystemExit(f"В CSV нет столбцов: {missing}. Есть: {list(df.columns)}")
    return df


def series_names(df):
    names = list(dict.fromkeys(df[SERIES_COL]))  # порядок появления в файле
    if SERIES_ORDER is not None:
        names = [s for s in SERIES_ORDER if s in names]
    return names


def label_of(name):
    return SERIES_LABELS.get(name, str(name))


def style_axes(ax, df):
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)
    if TITLE:
        ax.set_title(TITLE)
    if GRID:
        ax.grid(True, linewidth=0.4, alpha=0.6)
        ax.set_axisbelow(True)
    if LOG_X and KIND == "line":   # лог. ось X имеет смысл только для линий
        ax.set_xscale("log", base=LOG_X_BASE)
    if LOG_Y:
        ax.set_yscale("log", base=LOG_Y_BASE)
    # Подписи по X в точках измерений (только линии с числовым X).
    # Делается после выбора масштаба, иначе он сбросил бы подписи.
    if KIND == "line" and X_TICKS_FROM_DATA and pd.api.types.is_numeric_dtype(df[X_COL]):
        ax.set_xticks(sorted(df[X_COL].unique()))
        if LOG_X:
            ax.xaxis.set_major_formatter(ScalarFormatter())  # «8», а не «2^3»
            ax.xaxis.set_minor_formatter(NullFormatter())
    if X_LIM:
        ax.set_xlim(*X_LIM)
    if Y_LIM:
        ax.set_ylim(*Y_LIM)
    elif Y_FROM_ZERO and not LOG_Y:
        ax.set_ylim(bottom=0)
    if LEGEND:
        ax.legend(loc=LEGEND_LOC, ncol=LEGEND_NCOL, frameon=LEGEND_FRAME)


def plot_lines(ax, df):
    numeric_x = pd.api.types.is_numeric_dtype(df[X_COL])
    if numeric_x:
        pos_of = None
    else:
        cats = X_ORDER if X_ORDER is not None else list(dict.fromkeys(df[X_COL]))
        pos_of = {c: i for i, c in enumerate(cats)}

    for i, name in enumerate(series_names(df)):
        sub = df[df[SERIES_COL] == name]
        x = sub[X_COL] if numeric_x else sub[X_COL].map(pos_of)
        sub = sub.assign(_x=x).sort_values("_x")
        kw = dict(color=COLORS[i % len(COLORS)], marker=MARKERS[i % len(MARKERS)],
                  linestyle=LINESTYLES[i % len(LINESTYLES)], linewidth=LINE_WIDTH,
                  markersize=MARKER_SIZE, label=label_of(name))
        if ERR_COL and ERR_STYLE == "bars":
            ax.errorbar(sub["_x"], sub[Y_COL], yerr=sub[ERR_COL], capsize=ERR_CAPSIZE, **kw)
        else:
            ax.plot(sub["_x"], sub[Y_COL], **kw)
            if ERR_COL and ERR_STYLE == "band":
                ax.fill_between(sub["_x"], sub[Y_COL] - sub[ERR_COL], sub[Y_COL] + sub[ERR_COL],
                                color=kw["color"], alpha=BAND_ALPHA, linewidth=0)

    if not numeric_x:
        ax.set_xticks(list(pos_of.values()))
        ax.set_xticklabels([str(c) for c in pos_of])


def plot_bars(ax, df):
    cats = X_ORDER if X_ORDER is not None else list(dict.fromkeys(df[X_COL]))
    names = series_names(df)
    width = BAR_GROUP_WIDTH / len(names)
    for i, name in enumerate(names):
        sub = df[df[SERIES_COL] == name].set_index(X_COL).reindex(cats)
        xs = [j - BAR_GROUP_WIDTH / 2 + width * (i + 0.5) for j in range(len(cats))]
        yerr = sub[ERR_COL] if ERR_COL else None
        ax.bar(xs, sub[Y_COL], width=width, color=COLORS[i % len(COLORS)],
               yerr=yerr, capsize=ERR_CAPSIZE, label=label_of(name),
               edgecolor="black", linewidth=0.4)
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels([str(c) for c in cats])


def main():
    global INPUT_CSV, OUTPUT_PDF
    if len(sys.argv) > 1:
        INPUT_CSV = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT_PDF = sys.argv[2]

    apply_style()
    df = load_data()
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_CM / 2.54, FIG_HEIGHT_CM / 2.54),
                           constrained_layout=True)
    if KIND == "line":
        plot_lines(ax, df)
    elif KIND == "bar":
        plot_bars(ax, df)
    else:
        raise SystemExit('KIND должен быть "line" или "bar"')
    style_axes(ax, df)

    out = Path(OUTPUT_PDF)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)  # формат берётся из расширения: .pdf, .svg или .png
    print(f"Сохранено: {out}")


if __name__ == "__main__":
    main()