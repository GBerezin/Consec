import numpy as np
from prettytable import PrettyTable
import MemberSection.Mcharts as Mch
import Ccharts as Cch


class Result:
    """Класс представляющий результаты расчета"""

    def __init__(self, vsigmac, vsigmas, section, rebars):
        """
        Инициализация результатов расчета.

        :param vsigmac: Векторизованная функция бетона
        :param vsigmas: Векторизованная функция арматуры
        :param section: Бетонное сечение
        :param rebars: Арматурные стержни
        """
        self.vsigmac = vsigmac
        self.vsigmas = vsigmas
        self.section = section
        self.rebars = rebars

    def results(self, f, u, abi, xbi, ybi, e_b, eb, s_b, sb, asj, xsj, ysj, es, ss, c_g, c_p):
        """
        Вывод результатов расчета.

        :param f: Вектор нагрузки
        :param u: Вектор деформаций
        :param abi: Площади КЭ бетона
        :param xbi: Координаты x КЭ бетона
        :param ybi: Координаты y КЭ бетона
        :param e_b: Относительные деформации бетона
        :param eb: Результаты относительных деформаций бетона
        :param s_b: Напряжения бетона
        :param sb: Результаты напряжений бетона
        :param asj: Площади арматурных стержней
        :param xsj: Координаты x арматурных стержней
        :param ysj: Координаты y арматурных стержней
        :param es: Результаты относительных деформаций арматуры
        :param ss: Результаты напряжений арматуры
        :param c_g: Геометрия КЭ бетона
        :param c_p: Свойства бетона
        :return:
        """
        i = 0
        for name in self.rebars.keys():
            self.rebars[name].strain = es[i]
            self.rebars[name].stress = ss[i]
            i += 1
        ep = np.zeros(2)
        sp = np.zeros(2)
        ep[0] = round(min(eb), 6)
        ep[1] = round(max(es), 6)
        sp[0] = round(min(sb), 6)
        sp[1] = round(max(ss), 6)
        print('Относительные деформации, напряжения [МПа]:')
        df = PrettyTable(['Значение', 'Бетон[min]', 'Арматура[max]'])
        df.add_row(['Деформации', ep[0], ep[1]])
        df.add_row(['Напряжения', sp[0], sp[1]])
        print(df)
        print('Проверка:')
        nr = 8
        cloads = np.round(1000 * np.array((sum(sb * np.array(abi)) + sum(ss * np.array(asj)),
                                           sum(sb * np.array(abi) * np.array(xbi)) + sum(
                                               ss * np.array(asj) * np.array(xsj)),
                                           sum(sb * np.array(abi) * np.array(ybi)) + sum(
                                               ss * np.array(asj) * np.array(ysj)))), nr)
        ptl = PrettyTable(["Нагрузка", "N, кН", "Mx, кН*м", "My, кН*м"])
        ptl.add_row(["Заданная", np.round(f[0] * 1000, nr), np.round(f[1] * 1000, nr), np.round(f[2] * 1000, nr)])
        ptl.add_row(["Полученная", cloads[0], cloads[1], cloads[2]])
        ptl.add_row(["u", np.round(u[0], nr), np.round(u[1], nr), np.round(u[2], nr)])
        print(ptl)
        print('Арматурные стержни:')
        ptr = PrettyTable(["Имя", "X, мм", "Y, мм", "Диаметр, мм", "Класс", "Деформации", "Напряжения, МПа"])
        for i in self.rebars:
            ptr.add_row(
                [i, self.rebars[i].x * 1000, self.rebars[i].y * 1000, self.rebars[i].ds * 1000, self.rebars[i].grade,
                 np.round(self.rebars[i].strain, 6), np.round(self.rebars[i].stress, 2)])
        print(ptr)
        arge = [eb, es, xbi, ybi, np.array(xsj), np.array(ysj), np.array(asj), c_g[4]]
        args = [sb, ss, xbi, ybi, np.array(xsj), np.array(ysj), np.array(asj), c_g[4]]
        sigmac = self.vsigmac(e_b, *e_b, *s_b, c_p['E'])  # Напряжения в бетоне для диаграммы состояния
        Cch.loads('MemberSection/member_section.png')  # Правило знаков нагрузок
        Cch.strainstress(e_b, sigmac, self.section.grade)  # Диаграмма состояния бетона
        rbrs = {}  # Словарь арматурных стержней с уникальными классами
        for key in self.rebars.keys():
            rbrs[self.rebars[key].grade] = self.rebars[key]
        for key in rbrs.keys():
            s_s = [rbrs[key].st['Rsc'], rbrs[key].st['Rs']]
            e_s = [rbrs[key].st['esc2'], rbrs[key].st['esc0'], rbrs[key].st['es0'], rbrs[key].st['es2']]
            sigmas = self.vsigmas(e_s, *e_s, *s_s, rbrs[key].st['E'])
            Cch.strainstress(e_s, sigmas, key)  # Диаграмма состояния арматуры
        Mch.strain2d(*arge)  # График деформаций в сечении 2D
        Mch.strain3d(eb, xbi, ybi)  # График деформаций в сечении 3D
        Mch.stress2d(*args)  # График напряжений в сечении 2D
        Mch.stress3d(sb, xbi, ybi)  # График напряжений в сечении 3D
