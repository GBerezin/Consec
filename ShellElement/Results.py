import numpy as np
import pandas as pd


class Result:
    """Результаты расчета"""

    def __init__(self, zb, zs, ab, a_s):
        """
        Инициализация вывода результатов расчета.

        :param zb: Координаты слоя бетона от центра элемента, м
        :param zs: Координаты слоя арматуры от центра элемента, м
        :param ab: Площади бетонных слоев, м^2
        :param as: Площади арматурных слоев, м^2
        """
        self.zb = zb
        self.zs = zs
        self.z = ab
        self.a_s = a_s

    def results(self, orientation, alpha, k, eps1, eps2, sig1, sig2, t, ns, strain, stress):
        """
        Результаты расчета.

        :param orientation: Угол направления напряжения 1 в слоях бетона от оси X, радиан
        :param alpha: Угол направления  стержней в арматурных слоях от оси X, радиан
        :param k: Количество слоев бетона
        :param eps1: Относительная деформация в слоях бетона по направлению 1
        :param eps2: Относительная деформация в слоях бетона по направлению 2
        :param sig1: Напряжения в слоях бетона по направлению 1, МПа
        :param sig2: Напряжения в слоях бетона по направлению 2, МПа
        :param t: Толщина слоев бетона, м
        :param ns: Количество арматурных слоев
        :param strain: Относительная деформация в слоях арматуры
        :param stress: Напряжения в слоях арматуры, МПа
        :return: Таблица Pandas
        """
        ang_c = np.degrees(orientation)
        ang_s = np.degrees(alpha)
        res1_b = np.hstack((self.zb.reshape(k, 1),
                            np.round(eps1.reshape(k, 1), 5),
                            np.round(eps2.reshape(k, 1), 5),
                            np.round(sig1.reshape(k, 1), 2),
                            np.round(sig2.reshape(k, 1), 2),
                            np.round(ang_c.reshape(k, 1), 3),
                            t.reshape(k, 1)))
        res1_s = np.hstack((np.array(self.zs).reshape(ns, 1),
                            np.round(strain.reshape(ns, 1), 5),
                            np.zeros(ns).reshape(ns, 1),
                            np.round(stress.reshape(ns, 1), 2),
                            np.zeros(ns).reshape(ns, 1),
                            np.round(ang_s.reshape(ns, 1), 3),
                            np.array(self.a_s).reshape(ns, 1)))
        res = np.vstack((res1_b, res1_s))
        result = pd.DataFrame(res, columns=['Z', 'Strain1', 'Strain2', 'Stress1', 'Stress2', 'Angle', 'Area'])
        return result

    def convergence(self, fg, sxyb, sxys, u):
        """
        Проверка сходимости.

        :param fg: Вектор нагрузки, [МН, МН, МН, МН*м, МН*м, МН*м]
        :param sxyb: Напряжения в бетоне, МПа
        :param sxys: Напряжения в арматуре, МПа
        :param u: Вектор деформаций
        :return: Таблица Pandas
        """

        z = np.hstack((self.zb, self.zs))
        sxy = np.vstack((sxyb, sxys))
        a = np.hstack((self.z, self.a_s))
        ff = np.zeros(6)
        n = len(z)
        for i in range(0, n):
            ff[0] = ff[0] + sxy[i][0] * a[i]
            ff[1] = ff[1] + sxy[i][1] * a[i]
            ff[2] = ff[2] + sxy[i][2] * a[i]
            ff[3] = ff[3] + sxy[i][0] * a[i] * z[i]
            ff[4] = ff[4] + sxy[i][1] * a[i] * z[i]
            ff[5] = ff[5] + sxy[i][2] * a[i] * z[i]
        cvr = np.hstack((fg.reshape(6, 1), np.round(ff.reshape(6, 1), 4), u.reshape(6, 1)))
        cvrg = pd.DataFrame(cvr, index=['Nxx', 'Nyy', 'Nxy', 'Mxx', 'Myy', 'Mxy'], columns=['Дано:', 'Получено:', 'u:'])
        return cvrg
