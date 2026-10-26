"""
Проект 1: как подглядывание (peeking) раздувает долю ложноположительных результатов в A/B-тесте.

Идея: моделируем A/A-тесты (эффекта НЕТ) и смотрим, как часто тест "находит" значимость.
Всё векторизовано через numpy: никаких циклов по симуляциям.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(42)

# ---------- Параметры ----------
N_SIM = 10_000      # число симулированных тестов
DAYS = 14           # длительность теста, дней (= число "подглядываний")
DAILY_N = 360       # новых пользователей в день на группу (~5000 за 14 дней)
P = 0.10            # базовая конверсия (в A/A у обеих групп одинаковая)
ALPHA = 0.05


# ---------- Шаг 1. Симуляция (готово) ----------
def simulate(n_sim, days, daily_n, p_a, p_b, rng):
    """Возвращает накопленные успехи по дням для групп A и B и накопленный размер группы."""
    a = rng.binomial(daily_n, p_a, size=(n_sim, days)).cumsum(axis=1)
    b = rng.binomial(daily_n, p_b, size=(n_sim, days)).cumsum(axis=1)
    n = daily_n * np.arange(1, days + 1)  # накопленное n на группу, shape (days,)
    return a, b, n


def z_stats(a, b, n):
    """Двухвыборочный z-тест для долей на каждый день. Shape (n_sim, days)."""
    p_a, p_b = a / n, b / n
    pooled = (a + b) / (2 * n)
    se = np.sqrt(pooled * (1 - pooled) * 2 / n)
    return (p_b - p_a) / se


# ---------- Шаг 2. Наивное подглядывание (TODO) ----------
def naive_fpr(z, alpha):
    """
    TODO: посчитайте две величины:
      1) fpr_final: доля симуляций, где |z| значим ТОЛЬКО в последний день (должно быть ~alpha)
      2) fpr_peeking: доля симуляций, где |z| значим ХОТЯ БЫ В ОДИН из дней
    Подсказка: критическое значение z_crit = stats.norm.ppf(1 - alpha / 2);
    "хотя бы один день" = np.any(..., axis=1).
    """
    raise NotImplementedError


def fpr_by_number_of_looks(z, alpha):
    """
    TODO: для k = 1..DAYS посчитайте долю симуляций, где значимость была
    хотя бы раз в первые k дней. Верните массив длины DAYS (для графика).
    Подсказка: np.any(np.abs(z[:, :k]) > z_crit, axis=1).mean()
    """
    raise NotImplementedError


# ---------- Шаг 3. Корректные границы (TODO) ----------
def calibrate_constant(z, boundary_shape, alpha):
    """
    Подбор константы c так, чтобы общая доля ложных срабатываний при DAYS проверках была ровно alpha.
      Pocock:            граница на каждом дне = c (константа)         -> boundary_shape = np.ones(DAYS)
      O'Brien-Fleming:   граница на дне k = c * sqrt(DAYS / k)          -> boundary_shape = np.sqrt(DAYS / np.arange(1, DAYS + 1))
    TODO: переберите c по сетке (например, np.linspace(1.5, 4, 300)) и найдите наименьшее c,
    при котором np.any(np.abs(z) > c * boundary_shape, axis=1).mean() <= alpha.
    Это и есть "симуляционная калибровка": не нужны таблицы, и вы понимаете, откуда берётся граница.
    """
    raise NotImplementedError


# ---------- Шаг 4. Мощность (бонус, TODO) ----------
def power_with_effect(p_b, boundary):
    """
    TODO (бонус): симулируйте тест с реальным эффектом (например, P=0.10 vs p_b=0.11)
    и сравните мощность: фиксированный размер выборки, наивный peeking, Pocock, O'Brien-Fleming.
    Вывод, к которому вы должны прийти: подглядывание "бесплатно" не бывает,
    корректные методы платят чуть меньшей мощностью в конце, но дают честный контроль ошибки.
    """
    raise NotImplementedError


# ---------- Графики (TODO) ----------
def plot_fpr_growth(fpr_curve):
    """TODO: линия роста доли ложных срабатываний по числу проверок + горизонтальная линия на alpha."""
    raise NotImplementedError


def plot_p_value_paths(z, n_paths=20):
    """TODO: траектории p-value для ~20 случайных A/A-тестов по дням + линия 0.05.
    p = 2 * (1 - stats.norm.cdf(np.abs(z)))"""
    raise NotImplementedError


if __name__ == "__main__":
    a, b, n = simulate(N_SIM, DAYS, DAILY_N, P, P, rng)  # A/A: p_a == p_b
    z = z_stats(a, b, n)

    # Проверка себя: в последний день доля |z| > 1.96 должна быть около 5%
    print("Sanity check, FPR в последний день:", (np.abs(z[:, -1]) > stats.norm.ppf(1 - ALPHA / 2)).mean())

    # TODO: вызовите функции шагов 2-4, соберите результаты в pandas-таблицу и сохраните графики
