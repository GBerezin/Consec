import numpy as np
import pandas as pd
from pynite import LoadCombo
from ShellElement.RebarPlies import Ply
from ShellElement.Shells import Shell
import ShellElement.Scharts as Sch
import Ccharts as Cch
import Sigma as Sgm
from ShellElement.Results import Result
from ShellElement.Iterations import Calc


class ShellElem:
    """Класс представляющий выделенный  жб элемент оболочки"""

    def __init__(self, concrete, steel):
        """Инициализация выделенного  жб элемента оболочки."""

        self.cshell = None  # Элемент оболочки
        self.concrete = concrete  # Данные по бетону
        self.steel = steel  # Данные по стали
        self.plies = {}  # Словарь слоев арматурных стержней
        self.Loads = []  # Список нагрузок
        self.loadcombos = {}  # Словарь комбинаций нагрузок
        self.c_p = None  # Свойства бетона
        self.c_g = None  # Свойства геометрии

    def add_conc_element(self, grade, h, nh):
        """
        Добавляет новый выделенный  жб элемент оболочки.

        :param grade: Класс бетона, из списка в English B15	B20	B25	B30	B35	B40	B45	B50	B55	B60	B70	B80	B90	B100
        :param h: Высота сечения, мм
        :param nh: Количество слоев бетона по высоте сечения
        :return:
        """

        # Создает новый выделенный  бетонный элемент оболочки
        self.cshell = Shell(grade, h, nh, self.concrete)
        self.c_p = self.cshell.conc_prop  # Свойства бетона
        self.c_g = self.cshell.conc_geometry  # Геометрия бетона

    def add_ply(self, name, grade, ds, ns, z, a):
        """
        Добавляет новый слой арматурных стержней в жб элемент оболочки.

        :param name: Имя слоя стержней
        :param grade: Класс арматуры, из списка в English A240   A400	A500
        :param ds: Диаметр стержней слоя, мм
        :param ns: Количество стержней в слое на 1 м
        :param z: Координата от центра элемента, мм
        :param a: Угол направления от оси X, градус
        :return:
        """

        # Создает новый слой арматурных стержней
        new_ply = Ply(name, grade, ds, ns, z, a, self.steel)
        # Добавляет новый слой стерженей в коллекцию
        self.plies[name] = new_ply

    def add_load(self, nxx, nyy, nxy, mxx, myy, mxy, case='Case 1'):
        """
        Добавляет нагрузку в элемент.

        :param nxx: Продольная сила по X, кН (+ растяжение)
        :param nyy: Продольная сила по Y, кН (+ растяжение)
        :param nxy: Сдвиговая сила XY, кН
        :param mxx: Изгибающий момент вдоль оси X, кН*м
        :param myy: Изгибающий момент вдоль оси Y, кН*м
        :param mxy: Крутящий момент XY, кН*м
        :param case: Имя загружения, строка
        :return:
        """
        self.Loads.append((nxx, nyy, nxy, mxx, myy, mxy, case))

    def add_load_combo(self, name, factors, combo_type='strength'):
        """
        Добавляет комбинацию нагрузок к элементу

        :param name: Уникальное имя комбинации ('1.1D+1.2L')
        :param factors: Словарь включающий нагрузки и их коэффициенты ({'D': 1.1, 'L': 1.2}).
        :param combo_type: Тип комбинации нагрузок
        :return:
        """
        # Создает новую комбинацию
        new_combo = LoadCombo.LoadCombo(name, combo_type, factors)
        # Добавляет комбинацию к словарю
        self.loadcombos[name] = new_combo

    def force(self, combo_name):
        """
        Собирает вектор нагрузки.

        :param combo_name: Имя комбинации для вектора нагрузки
        :return: Вектор нагрузки, [МН, МН, МН, МН*м, МН*м, МН*м]
        """
        f = np.zeros(6)
        combo = self.loadcombos[combo_name]
        for case, factor in combo.factors.items():
            for load in self.Loads:
                if load[6] == case:
                    f[0] += factor * load[0] / 1000
                    f[1] += factor * load[1] / 1000
                    f[2] += factor * load[2] / 1000
                    f[3] += factor * load[3] / 1000
                    f[4] += factor * load[4] / 1000
                    f[5] += factor * load[5] / 1000
        return f

    def analyze(self, combo_name, kt, gb3, v, acc):
        """
        Расчет выделенного  жб элемента оболочки.

        :param combo_name: Имя расчетной комбинации нагрузок
        :param kt: Коэффициент учета растяжения бетона
        :param gb3: Коэффициент gb3 бетона
        :param v: Коэффициент Пуассона
        :param acc: Точность расчета
        """

        pl1 = np.eye(3)
        fg = self.force(combo_name)
        vsigmac = np.vectorize(Sgm.sigmac)  # Векторизованная функция диаграммы состояния бетона
        t, zb = self.c_g
        k = len(zb)  # Количество слоев бетона по высоте сечения
        plb = np.zeros((k, 3, 6))  # Матрица коэффициентов деформаций бетонных слоев
        for i in range(0, k):
            pl2 = pl1 * zb[i]
            plb[i, :, :] = np.hstack((pl1, pl2))
        v0_1 = np.ones(k) * v  # Коэффициенты Пуассона в слоях бетона
        # Параметры диаграммы состояния бетона
        s_b = [self.c_p['Rb'] * gb3, self.c_p['Rb'] * 0.6 * gb3, self.c_p['Rbt'] * 0.6 * kt, self.c_p['Rbt'] * kt]
        e_b = [self.c_p['eb2'], self.c_p['eb0'], s_b[1] / self.c_p['E'], s_b[2] / self.c_p['E'], self.c_p['ebt0'],
               self.c_p['ebt2']]
        eb = self.c_p['E']  # Начальный модуль упругости бетона, МПа
        sigc = vsigmac(e_b, *e_b, *s_b, eb)  # Напряжения в бетонных слоях
        eb_ = np.linspace(eb, eb, k)  # Начальные модули упругости в слоях бетона, МПа
        eb = np.stack((eb_, eb_), axis=-1)  # Начальные модули упругости в слоях бетона по главным направлениям, МПа
        vsigmas = np.vectorize(Sgm.sigmas)  # Векторизованная функция диаграммы состояния арматурной стали
        ds = []  # диаметры арматурных стержней в каждом арматурном слое, м
        n_s = []  # Количество арматурных стержней в каждом арматурном слое
        zs = []  # Координаты арматурных слоев от центра элемента, м
        alpha = []  # Углы направления арматурных слоев от оси X, градусы
        a_s = []  # Площади поперечного сечения слоев арматурных стержней, м^2
        rsc = []  # Расчетные сопротивления арматуры сжатию, МПа
        rs = []  # Расчетные сопротивления арматуры растяжению, МПа
        esc2 = []  # Относительные деформации укорочения арматуры
        esc0 = []  # Относительные деформации укорочения арматуры
        es0 = []  # Относительные деформации удлинения арматуры
        es2 = []  # Относительные деформации удлинения арматуры
        es = []  # Начальные модули упругости в слоях арматуры, МПа
        for name in self.plies.keys():
            ds.append(self.plies[name].ds)
            n_s.append(self.plies[name].ns)
            zs.append(self.plies[name].z)
            alpha.append(self.plies[name].alpha)
            a_s.append(self.plies[name].asj)
            rsc.append(self.plies[name].st['Rsc'])
            rs.append(self.plies[name].st['Rs'])
            esc2.append(self.plies[name].st['esc2'])
            esc0.append(self.plies[name].st['esc0'])
            es0.append(self.plies[name].st['es0'])
            es2.append(self.plies[name].st['es2'])
            es.append(self.plies[name].st['E'])
        ns = len(zs)  # Количество слоев арматуры по высоте сечения
        eps_s = np.array([esc2, esc0, es0, es2]).transpose().reshape(ns, 1, 4)
        sig_s = np.array([rsc, rs]).transpose().reshape(ns, 1, 2)
        pls = np.zeros((ns, 3, 6))  # Матрица коэффициентов деформаций арматурных слоев
        for i in range(0, ns):
            pl2 = np.eye(3) * zs[i]
            pls[i, :, :] = np.hstack((pl1, pl2))
        v01 = v0_1
        args = v01, k, eb, eb_, plb, es, pls, fg, t, zb, ns, alpha, np.array(a_s), np.array(
            zs), vsigmac, vsigmas, e_b, s_b, eps_s, sig_s, acc
        calc = Calc(args)
        calc.itrn()
        eps1, eps2, sig1, sig2, sxyb, sxys, orientation, strain, stress, eps, sig, u = calc.rslt
        res = Result(zb, zs, t, a_s)
        result = res.results(orientation, alpha, k, eps1, eps2, sig1, sig2, t, ns, strain, stress)
        cvrg = res.convergence(fg, sxyb, sxys, u)
        print('Результаты расчета:')
        print(result)
        min_ = min(min(eps1), min(eps2), min(strain))
        max_ = max(max(eps1), max(eps2), max(strain))
        ep = np.zeros((1, 2))
        ep[0, 0] = round(min_, 6)
        ep[0, 1] = round(max_, 6)
        res = pd.DataFrame(ep, columns=['Strain_min', 'Strain_max'])
        print(res.head(np.size(res)))
        print('Проверка сходимости:')
        print(cvrg)
        Cch.loads('ShellElement/shell_element.png')  # Правило знаков нагрузок
        print('Бетон класса:', self.cshell.grade)
        print('Коэффициент работы бетона на растяжение: ', kt)
        print('Коэффициент gb3: ', gb3)
        print('Коэффициент Пуассона: ', v)
        Cch.strainstress(e_b, sigc, self.cshell.grade)  # Диаграмма состояния бетона
        pls = {}  # Словарь арматурных стержней с уникальными классами
        for key in self.plies.keys():
            pls[self.plies[key].grade] = self.plies[key]
        for key in pls.keys():
            es = np.array([pls[key].st['esc2'], pls[key].st['esc0'], pls[key].st['es0'], pls[key].st['es2']])
            ss = np.array([pls[key].st['Rsc'], pls[key].st['Rs']])
            e_s = np.array([pls[key].st['E']])
            sigmas = vsigmas(es, *es, *ss, e_s)
            print('Арматура класса:', key)
            Cch.strainstress(es, sigmas, key)  # Диаграмма состояния арматуры
        df = result.iloc[:k, :]
        Sch.strain(df)
        rstress = result['Stress1'].values[k:]
        z = result['Z'].values[k:]
        Sch.stress(z, df, rstress)
        Sch.reb3d(self.plies, rstress, 'Напряжения в слоях арматуры, МПа')
        Sch.con3d(zb, sig1, sig2, orientation, 'Напряжения в слоях бетона, МПа')
