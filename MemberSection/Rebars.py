import numpy as np


class Rebar:
    """Класс представляющий арматурный стержень"""

    def __init__(self, name, grade, ds, x, y, steel):
        """
        Инициализация арматурного стержня

        :param name: Имя стержня
        :param grade: Класс арматуры, из списка в English A240  A400    A500
        :param ds: Диаметр стержня, мм
        :param x: Координата x, мм
        :param y: Координата y, мм
        :param steel: Данные по стали
        """
        self.name = name
        self.grade = grade
        self.ds = ds / 1000
        self.x = x / 1000
        self.y = y / 1000
        self.steel = steel
        self.strain = {}  # Относительные деформации
        self.stress = {}  # Напряжения, МПа

    @property
    def st(self):
        """Свойства стали арматурного стержня"""
        s = self.steel[self.grade]
        return s

    @property
    def asj(self):
        """Площадь поперечного сечения арматурного стержня, м^2"""
        as_j = np.pi * self.ds ** 2 / 4
        return as_j
