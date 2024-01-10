import numpy as np

class Shell:
    """Класс представляющий бетонный элемент оболочки"""

    def __init__(self, grade, h, nh, concrete):
        """
        Инициализация выделенного бетонного элемента оболочки

        :param grade: Класс бетона, из списка в English B15	B20	B25	B30	B35	B40	B45	B50	B55	B60	B70	B80	B90	B100
        :param h: Высота элемента, мм
        :param nh: Число слоев по высоте сечения
        :param concrete: Данные по бетону
        """
        self.grade = grade
        self.h = h / 1000
        self.nh = nh
        self.concrete = concrete

    @property
    def conc_prop(self):
        """Свойства бетона сечения"""

        c = self.concrete[self.grade]
        return c

    @property
    def conc_geometry(self):
        """
        Геометрические характеристики выделенного бетонного элемента оболочки.

        :return: Геометрические характеристики бетонного элемента оболочки
        """

        dh = self.h / self.nh
        ab = dh
        nb = self.nh
        abi = np.linspace(ab, ab, nb)
        zbi = np.linspace(self.h / 2 - dh / 2, -self.h / 2 + dh / 2, nb)
        t = np.concatenate([[0], abi, [0]])
        zb = np.concatenate([[self.h / 2], zbi, [-self.h / 2]])
        g = [t, zb]
        return g
