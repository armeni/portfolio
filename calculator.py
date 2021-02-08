import scipy
import numpy as np
from scipy import special
from functools import reduce


class Calculator:
    def __init__(self, returns, t=0.085, kf=0.05):
        """
        :param returns: прогнозные данные актива на месяц
        :param t: срок действия опциона (31 день / 365)
        :param kf: безрисковая доходность
        """
        self.returns = returns
        self.t = t
        self.kf = kf

    def expected_asset_profit(self):
        """
        Расчёт ожидаемой доходности актива по дням (столбец матрицы доходностей)
        :return: математическое ожидание доходности актива по дням; list
        """

        expected_profit = []
        daily_change = self.returns.pct_change()
        vol = self.asset_volatility(daily_change)  # волатильность актива, подсчитанная с помощью pct_change()
        for i in range(len(self.returns) - 1):
            s1 = self.returns[i + 1]
            s0 = self.returns[i]
            k = s0 - vol * s0  # цена исполнения
            p = self.black_formula(s0, k, vol)  # стоимость опциона пут по модели Блэка - Шоулза
            if s1 > k:
                expected_profit.append((s1 - p) / s0 - 1)
            else:
                expected_profit.append((k - p) / s0 - 1)
        return expected_profit

    @staticmethod
    def asset_volatility(daily_change, freq=22):
        """
        Расчёт среднемесячной волатильности актива
        :param daily_change: дневное изменение цен
        :param freq: количество рабочих дней в месяц
        :return: среднемесячная волатильность актива; double
        """
        return daily_change.std() * np.sqrt(freq)

    def black_formula(self, s0, k, vol):
        """
        Расчёт стоимости опциона на конец инвестирования (по модели Блэка-Шоулза)
        :param s0: стоимость акции в начальный момент времени
        :param k: цена исполнения
        :param vol: среднемесячная волатильность акции
        :return: стоимость опциона пут; double
        """
        def N(x):
            return 1 / 2 * (1 + scipy.special.erf(x / np.sqrt(2)))

        d1 = (np.log(s0 / k) + (self.kf + 1 / 2 * vol ** 2) * self.t) / (vol * np.sqrt(self.t))
        d2 = d1 - vol * np.sqrt(self.t)
        result = k * np.exp(-self.kf * self.t) * N(-d2) - s0 * N(-d1)
        return result

    def covariance(self, freq=22):
        """
        Расчёт ковариационной матрицы
        :param freq: количество рабочих дней в месяц
        :return: ковариационная матрица; pandas-датафрейм
        """
        return self.returns.cov() * freq

    def portfolio_risk(self, allocations):
        """
        Риск портфеля, который будем минимизировать
        :param allocations: распределение активов в портфеле
        :return: риск портфеля; double
        """
        return reduce(np.dot, [allocations, self.covariance(), allocations.T])