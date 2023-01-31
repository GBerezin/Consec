import numpy as np


class Rectangle:
    """Класс представляющий бетонное прямоугольное сечение"""

    def __init__(self, grade, h, b, nh, nb, concrete):
        """
        Инициализация прямоугольного бетонного сечения

        :param grade: Класс бетона, из списка в English B15	B20	B25	B30	B35	B40	B45	B50	B55	B60	B70	B80	B90	B100
        :param h: Высота сечения, мм
        :param b: Ширина сечения, мм
        :param nh: Число КЭ по высоте сечения
        :param nb: Число КЭ по ширине сечения
        :param concrete: Данные по бетону
        """
        self.grade = grade
        self.h = h / 1000
        self.b = b / 1000
        self.nh = nh
        self.nb = nb
        self.concrete = concrete

    @property
    def conc_prop(self):
        """Свойства бетона сечения"""

        c = self.concrete[self.grade]
        return c

    @property
    def conc_geometry(self):
        """
        Геометрические характеристики прямоугольного сечения.

        :return: Геометрические характеристики прямоугольного сечения
        """

        dh = self.h / self.nh
        db = self.b / self.nb
        ab = dh * db
        nb = self.nh * self.nb
        ab_i = np.linspace(ab, ab, nb)
        secb = np.zeros((nb, 2))
        for i in range(0, self.nb):
            for j in range(0, self.nh):
                secb[j + i * self.nh, 0] = -self.h / 2 + dh * j + dh / 2
                secb[j + i * self.nh, 1] = -self.b / 2 + db * i + db / 2
        xb1_2 = np.linspace(-self.h / 2, self.h / 2, self.nh + 1)
        yb1_2 = np.linspace(-self.b / 2, -self.b / 2, self.nh + 1)
        xb2_4 = np.linspace(self.h / 2, self.h / 2, self.nb - 2)
        yb2_4 = np.linspace(-self.b / 2 + db, self.b / 2 - db, self.nb - 2)
        xb4_3 = np.linspace(self.h / 2, -self.h / 2, self.nh + 1)
        yb4_3 = np.linspace(self.b / 2, self.b / 2, self.nh + 1)
        xb3_1 = np.linspace(-self.h / 2, -self.h / 2, self.nb - 2)
        yb3_1 = np.linspace(self.b / 2 - db, -self.b / 2 + db, self.nb - 2)
        abi = np.hstack([ab_i, np.zeros(2 * (len(xb1_2) + len(xb2_4)))])
        xbi = np.hstack([secb[:, 0], xb1_2, xb2_4, xb4_3, xb3_1])
        ybi = np.hstack([secb[:, 1], yb1_2, yb2_4, yb4_3, yb3_1])
        a = np.sum(abi)
        ix = np.sum(ab_i * secb[:, 1] ** 2)
        iy = np.sum(ab_i * secb[:, 0] ** 2)
        ci = [nb, nb + self.nh, nb + self.nh + self.nb - 1, nb + 2 * self.nh + self.nb - 1]
        zb = np.transpose(np.array([np.ones(len(xbi)), xbi, ybi]))
        g = [xbi, ybi, abi, zb, ci, a, ix, iy]
        return g
