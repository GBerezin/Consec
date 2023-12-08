import numpy as np


class D:
    """Класс представляющий матрицу жесткости"""

    def __init__(self, k, t, zb, ns, a_s, zs, alpha):
        """
        Инициализация класса матрицы жесткости.

        :param k: Количество бетонных слоев
        :param t: Толщины бетонных слоев
        :param zb: Координаты бетонных слоев от центра элемента
        :param ns: Количество арматурных слоев
        :param a_s: Площади арматурных слоев
        :param zs: Координаты арматурных слоев от центра элемента
        :param alpha: Углы направления арматурных слоев от оси X
        """

        self.k = k
        self.t = t
        self.zb = zb
        self.ns = ns
        self.a_s = a_s
        self.zs = zs
        self.alpha = alpha

    def v_b(self, sb, eps1, eps2, eс):
        """
        Коэффициент упругости бетона.

        :param sb: Напряжения в бетоне по главным направлениям
        :param eps1: Деформации бетона по главному направлению 1
        :param eps2: Деформации бетона по главному направлению 2
        :param eс: Модули упругости бетона в слоях по главным направлениям
        :return: Коэффициенты упругости бетона в слоях по главным направлениям
        """

        vb = np.ones((self.k, 2))  # Коэффициенты упругости бетона в слоях по главным направлениям
        for i in range(0, self.k):
            if eps1[i] != 0:
                vb[i, 0] = sb[i][0] / eс[i][0] / eps1[i]
            else:
                vb[i, 0] = 1.0
            if eps2[i] != 0:
                vb[i, 1] = sb[i][1] / eс[i][1] / eps2[i]
            else:
                vb[i, 1] = 1.0
        return vb

    def sxyb(self, orientation, sb):
        """
        Напряжения в бетоне по осям X и Y.

        :param orientation: Углы направления напряжения 1 в слоях бетона от оси X
        :param sb: Напряжения в бетоне по главным направлениям
        :return: Напряжения в бетоне по осям X и Y
        """
        c = np.cos(orientation)
        s = np.sin(orientation)
        s_xyb = np.zeros((self.k, 3, 1))  # Напряжения в слоях бетона по осям X и Y
        for i in range(0, self.k):
            cb = np.array([[c[i] ** 2, s[i] ** 2], [s[i] ** 2, c[i] ** 2], [s[i] * c[i], -s[i] * c[i]]])
            s_xyb[i][:, :] = cb @ sb[i][:, :]
        return s_xyb

    def conc(self, u, v01, v10, plb, vsigmac, e_b, s_b, eb_, eb):
        """
        Расчет бетонных слоев.

        :param u: Вектор общих деформаций
        :param v01: Коэффициенты Пуассона в слоях бетона по главной оси 1
        :param v10: Коэффициенты Пуассона в слоях бетона по главной оси 2
        :param plb: Матрица коэффициентов деформаций бетонных слоев
        :param vsigmac: Векторизованная функция диаграммы состояния бетона
        :param e_b: Относительные деформации диаграммы состояния бетона
        :param s_b: Напряжения диаграммы состояния бетона
        :param eb_: Начальные модули упругости в слоях бетона
        :param eb: Начальный модуль упругости бетона
        :return:
        """
        vv = 1 - v01 * v10  # Коэффициент Пуассона
        epsc = (plb @ u).reshape(self.k, 3, 1)  # Деформации в слоях бетона
        exx = epsc[:, 0].reshape(self.k)  # Деформации в слоях бетона по оси X
        eyy = epsc[:, 1].reshape(self.k)  # Деформации в слоях бетона по оси Y
        gxy = epsc[:, 2].reshape(self.k)  # Сдвиговые деформации в слоях бетона
        ee1 = exx + eyy
        ee2 = exx - eyy
        emax = (ee1 / 2 + np.sqrt((ee2 / 2) ** 2 + (gxy / 2) ** 2))
        emin = (ee1 / 2 - np.sqrt((ee2 / 2) ** 2 + (gxy / 2) ** 2))
        eps1 = (emax + v01 * emin) / vv  # Деформации в слоях бетона по главной оси 1
        eps2 = (v10 * emax + emin) / vv  # Деформации в слоях бетона по главной оси 2
        orientation = 0.5 * np.arctan2(gxy, ee2)  # Угол главного направления 1 от оси X
        k_rc = np.ones(self.k)  # Коэффициент уменьшения прочности бетона из-за поперечного растяжения
        for i in range(0, self.k):
            if eps1[i] > 0.002:
                k_rc[i] = 1.0 / (0.8 + 100 * eps1[i])
            else:
                k_rc[i] = 1.0
        sb = np.vstack((vsigmac(eps1, *e_b, *s_b, eb_), vsigmac(eps2, *e_b, *s_b, eb_))).transpose().reshape(self.k, 2,
                                                                                                             1)
        vb = self.v_b(sb, eps1, eps2, eb)
        s_xyb = self.sxyb(orientation, sb)
        return vb, sb, s_xyb, orientation, eps1, eps2

    def cqb(self, eb, v01, eb_):
        qb = np.zeros((self.k, 3, 3))
        g01 = np.zeros(self.k)
        v10 = np.zeros(self.k)
        for i in range(0, self.k):
            if eb[i, 0] != 0.0:
                v10[i] = eb[i, 1] * v01[i] / eb[i, 0]
            else:
                v10[i] = 0.0
            g01[i] = eb_[i] / (2 * (1 + v10[i]))
        v01 = v10
        vv = 1 - v01 * v10
        qb[:, 0, 0] = eb[:, 0] / vv
        qb[:, 0, 1] = v01 * eb[:, 1] / vv
        qb[:, 1, 1] = eb[:, 1] / vv
        qb[:, 1, 0] = v10 * eb[:, 1] / vv
        qb[:, 2, 2] = g01
        return qb, v01, v10

    def ct(self, a):
        n = len(a)
        c = np.cos(a)
        s = np.sin(a)
        t = np.zeros((n, 3, 3))
        for i in range(0, n):
            t[i, 0, :] = np.array((c[i] ** 2, s[i] ** 2, (2 * c[i] * s[i])))
            t[i, 1, :] = np.array((s[i] ** 2, c[i] ** 2, (-2 * c[i] * s[i])))
            t[i, 2, :] = np.array(((-c[i] * s[i]), c[i] * s[i], (c[i] ** 2 - s[i] ** 2)))
        return t

    def cd(self, a, z, t, q):
        r = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 2]])
        r_ = np.linalg.inv(r)
        t_ = np.linalg.inv(t)
        n = len(a)
        m = t_ @ q @ r @ t @ r_
        a_ = sum(m * a.reshape(n, 1, 1))
        b_ = sum(m * z.reshape(n, 1, 1) * a.reshape(n, 1, 1))
        d_ = sum(m * z.reshape(n, 1, 1) ** 2 * a.reshape(n, 1, 1))
        di = np.vstack((np.hstack((a_, b_)), np.hstack((b_, d_))))
        return di

    def v_s(self, strain, stress, es):
        """
        Коэффициент упругости арматуры.

        :param strain: Деформации в слоях арматуры
        :param stress: Напряжения в слоях арматуры
        :param es: Модули упругости арматуры в слоях
        :return: Коэффициенты упругости арматуры в слоях
        """

        vs = np.ones(self.ns)  # Коэффициенты упругости арматуры в слоях
        for i in range(0, self.ns):
            if strain[i] != 0:
                vs[i] = stress[i] / es[i] / strain[i]
            else:
                vs[i] = 1.0
        return vs

    def sxys(self, c, s, stress):
        """
        Напряжения в арматуре по осям X и Y.

        :param c: Косинусы углов арматуры в слоях от оси X
        :param s: Синусы углов арматуры в слоях от оси X
        :param stress: Напряжения в арматурных слоях
        :return: Напряжения в арматурных слоях по осям X и Y
        """
        s_xys = np.zeros((self.ns, 3, 1))  # Напряжения в арматурных слоях по осям X и Y
        for i in range(0, self.ns):
            cs = np.array([[c[i] ** 2, s[i] ** 2], [s[i] ** 2, c[i] ** 2], [s[i] * c[i], -s[i] * c[i]]])
            s_ts = np.hstack([stress[i], 0])
            s_xys[i][:, :] = (cs @ s_ts).reshape(3, 1)
        return s_xys

    def reb(self, u, pls, vsigmas, e_s, s_s, es):
        """
        Расчет арматурных слоев.

        :param u: Вектор общих деформаций
        :param pls: Матрица коэффициентов деформаций арматурных слоев
        :param vsigmas: Векторизованная функция диаграммы состояния арматуры
        :param e_s: Относительные деформации диаграммы состояния арматуры
        :param s_s: Напряжения диаграммы состояния арматуры
        :param es: Начальный модуль упругости арматуры
        :return:
        """
        epss = (pls @ u).reshape(self.ns, 3, 1)
        c = np.cos(self.alpha)
        s = np.sin(self.alpha)
        strain = np.zeros(self.ns)
        stress = np.zeros(self.ns)
        for i in range(0, self.ns):
            dc = np.array([c[i] ** 2, s[i] ** 2, 2 * s[i] * c[i]])
            strain[i] = dc @ epss[i]
            stress[i] = vsigmas(strain[i], *e_s[i, :, :][0], *s_s[i, :, :][0], es[i])
        vs = self.v_s(strain, stress, es)
        s_xys = self.sxys(c, s, stress)
        return vs, s_xys, strain, stress

    def d(self, e_b, eb_, vb, e_s, vs, orientation, v01):
        """
        Жесткостные характеристики плоских выделенных элементов жб оболочек.

        :param e_b: Модули упругости бетона
        :param eb_: Начальные модули упругости бетона в слоях, МПа
        :param vb: Коэффициент упругости бетона
        :param e_s: Модули упругости арматурной стали
        :param vs: Коэффициент упругости арматурной стали
        :param orientation: Угол направления напряжения 1 в слоях бетона от оси X, радиан
        :param v01:Коэффициенты Пуассона в слоях бетона по главной оси 1
        :return:
        """

        qb, v01, v10 = self.cqb(e_b * vb, v01, eb_)
        t_ = self.ct(orientation)
        db = self.cd(self.t, self.zb, t_, qb)
        qs = np.zeros((self.ns, 3, 3))
        qs[:, 0, 0] = e_s * vs
        t_ = self.ct(self.alpha)
        ds = self.cd(self.a_s, self.zs, t_, qs)
        abbd = db + ds
        return abbd, v01, v10
