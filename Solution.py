import numpy as np


class Calculation:
    """Решение"""

    @staticmethod
    def calc(d, f):
        """
        Получение вектора деформаций.

        :param d: Матрица жесткости
        :param f: Вектор нагрузок
        :return: Вектор деформаций
        """
        try:
            u = np.linalg.solve(d, f)
        except np.linalg.LinAlgError as var1:
            d = np.eye(3)
            fi = np.array(([0.0, 0.0, 0.0]))
            u = np.linalg.solve(d, fi)
            print('Решение невозможно:', var1)
            quit()
        return u
