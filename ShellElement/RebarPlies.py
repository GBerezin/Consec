import numpy as np


class Ply:
    """Класс представляющий арматурный слой"""

    def __init__(self, name, grade, ds, ns, z, a, steel):
        """
        Инициализация слоя арматурных стержней

        :param name: Имя слоя стержней
        :param grade: Класс арматуры, из списка в English A240  A400    A500
        :param ds: Диаметр стержней слоя, мм
        :param ns: Количество стержней в слое на 1 м
        :param z: Координата от центра элемента, мм
        :param a: Угол направления от оси X, градус
        :param steel: Данные по стали
        """
        self.name = name
        self.grade = grade
        self.ds = ds / 1000
        self.ns = ns
        self.z = z / 1000
        self.alpha = np.radians(a)
        self.steel = steel
        self.strain = {}  # Относительные деформации
        self.stress = {}  # Напряжения, МПа

    @property
    def st(self):
        """Свойства стали слоя арматурноых стержней"""
        s = self.steel[self.grade]
        return s

    @property
    def asj(self):
        """Площадь поперечного сечения слоя арматурных стержней, м^2"""
        asj = np.pi * self.ds ** 2 / 4 * self.ns
        return asj
