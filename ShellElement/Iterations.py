import numpy as np
from Solution import Calculation
from ShellElement import ABBD


class Calc:
    """Класс представляющий итерационный расчет"""

    def __init__(self, args):
        """
        Инициализация итерационного расчета.

        :param args: Аргументы
        """

        self.args = args
        self.rslt = None

    def itrn(self):
        """Итерационный расчет по нелинейной деформационной модели."""

        v01, k, eb, eb_, plb, es, pls, fg, t, zb, ns, alpha, a_s, zs, vsb, vss, e_b, s_b, e_s, s_s, acc = self.args
        orientation = np.zeros(k)  # Угол главного направления 1 от оси X
        vb = np.ones((k, 2))  # Коэффициенты упругости бетона
        vs = np.ones(ns)  # Коэффициенты упругости арматуры
        abbd = ABBD.D(k, t, zb, ns, a_s, zs, alpha)
        d, v01, v10 = abbd.d(eb, eb_, vb, es, vs, orientation, v01)
        u = Calculation.calc(d, fg)  # Вектор общих деформаций
        sb = np.zeros(k)  # Напряжения в бетоне
        eps1 = np.zeros(k)  # Деформации бетона по направлению 1
        eps2 = np.zeros(k)  # Деформации бетона по направлению 2
        strain = np.zeros(ns)  # Деформации арматуры
        stress = np.zeros(ns)  # Напряжения в арматуре
        sxyb = np.zeros((k, 2))  # Напряжения в бетоне по осям X и Y
        sxys = np.zeros((ns, 2))  # Напряжения в арматуре по осям X и Y
        du = 0.1  # Приращение общих деформаций
        it = 0  # Количество итераций
        while du >= acc:
            it += 1
            vb, sb, sxyb, orientation, eps1, eps2 = abbd.conc(u, v01, v10, plb, vsb, e_b, s_b, eb_, eb)
            vs, sxys, strain, stress = abbd.reb(u, pls, vss, e_s, s_s, es)
            d, v01, v10 = abbd.d(eb, eb_, vb, es, vs, orientation, v01)
            u_f = Calculation.calc(d, fg)  # Вектор общих деформаций
            du = np.max(abs(u - u_f))
            u = u_f  # Вектор общих деформаций
        print('Решение получено')
        print('Выполнено', it, 'итераций')
        sig1 = sb[:][:, 0]  # Напряжения в бетоне по направлению 1
        sig2 = sb[:][:, 1]  # Напряжения в бетоне по направлению 2
        eps = np.append(eps1.reshape(k, 1), strain.reshape(ns, 1))  # Деформации бетонных и арматурных слоев
        sig = np.append(sig1.reshape(k, 1), stress.reshape(ns, 1))  # Напряжения в бетонных и арматурных слоях
        self.rslt = eps1, eps2, sig1, sig2, sxyb, sxys, orientation, strain, stress, eps, sig, u
