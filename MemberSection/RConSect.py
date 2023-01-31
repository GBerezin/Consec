import numpy as np
from PyNite.LoadCombo import LoadCombo
from MemberSection.Rebars import Rebar
from MemberSection.Shapes import Rectangle
import Sigma as Sig
from Solution import Calculation
from MemberSection.Results import Result


class FrameSec:
    """Класс преставляющий нормальное поперечное сечение жб стержневого КЭ"""

    def __init__(self, concrete, steel):
        """Инициализация сечения жб стержневого КЭ."""

        self.section = None  # Поперечное сечение
        self.concrete = concrete  # Данные по бетону
        self.steel = steel  # Данные по стали
        self.rebars = {}  # Словарь арматурных стержней
        self.Loads = []  # Список нагрузок
        self.loadcombos = {}  # Словарь комбинаций нагрузок
        self.c_p = None  # Свойства бетона
        self.c_g = None  # Свойства геометрии

    def add_rect_section(self, grade, h, b, nh, nb):
        """
        Добавляет новое прямоугольное бетонное сечение в поперечное жб сечение

        :param grade: Класс бетона, из списка в English B15	B20	B25	B30	B35	B40	B45	B50	B55	B60	B70	B80	B90	B100
        :param h: Высота сечения, мм
        :param b: Ширина сечения, мм
        :param nh: Число КЭ по высоте сечения
        :param nb: Число КЭ по ширине сечения
        :return:
        """

        # Создает новое бетонное сечение
        self.section = Rectangle(grade, h, b, nh, nb, self.concrete)
        self.c_p = self.section.conc_prop  # Свойства бетона
        self.c_g = self.section.conc_geometry  # Геометрия бетона

    def add_rebar(self, name, grade, ds, x, y):
        """
        Добавляет новый арматурный стержень в жб сечение.

        :param name: Имя стержня
        :param grade: Класс арматуры, из списка в English A240   A400	A500
        :param ds: Диаметр стержня, мм
        :param x: Координата x, мм
        :param y: Координата y, мм
        :return:
        """

        # Создает новый стержень
        new_rebar = Rebar(name, grade, ds, x, y, self.steel)
        # Добавляет новый стержень в коллекцию
        self.rebars[name] = new_rebar

    def add_load(self, n, mx, my, case='Case 1'):
        """
        Добавляет нагрузку в сечение.

        :param n: Продольная сила, кН (+ растяжение)
        :param mx: Изгибающий момент вдоль оси X, кН*м
        :param my: Изгибающий момент вдоль оси Y, кН*м
        :param case: Имя загружения, строка
        :return:
        """
        self.Loads.append((n, mx, my, case))

    def add_load_combo(self, name, factors, combo_type='strength'):
        """
        Добавляет комбинацию нагрузок к сечению

        :param name: Уникальное имя комбинации ('1.1D+1.2L')
        :param factors: Словарь включающий нагрузки и их коэффициенты ({'D': 1.1, 'L': 1.2}).
        :param combo_type: Тип комбинации нагрузок
        :return:
        """
        # Создает новую комбинацию
        new_combo = LoadCombo(name, combo_type, factors)
        # Добавляет комбинацию к словарю
        self.loadcombos[name] = new_combo

    @staticmethod
    def d(ai, xi, yi, ei, vi):
        """
        Жесткостные характеристики поперечного сечения.

        :param ai: Площади, м^2
        :param xi: Координаты по x, м
        :param yi: Координаты по y, м
        :param ei: Mодули упругости, МПа
        :param vi: Коэффициенты упругости
        :return: Матрица жесткости
        """
        d00 = sum(ai * ei * vi)
        d11 = sum(ai * xi ** 2 * ei * vi)
        d22 = sum(ai * yi ** 2 * ei * vi)
        d01 = sum(ai * xi * ei * vi)
        d02 = sum(ai * yi * ei * vi)
        d12 = sum(ai * xi * yi * ei * vi)
        d = np.array([
            [d00, d01, d02],
            [d01, d11, d12],
            [d02, d12, d22]])
        return d

    @staticmethod
    def vi(s, e, eps):
        """
        Коэффициент упругости.

        :param s: Напряжение, МПа
        :param e: Mодуль упругости, МПа
        :param eps: Относительная деформация
        :return: Коэффициент упругости
        """

        if eps != 0.0:
            v = s / e / eps
        else:
            v = 1.0
        return v

    def force(self, combo_name):
        """
        Собирает вектор нагрузки.

        :param combo_name: Имя комбинации для вектора нагрузки
        :return: Вектор нагрузки, [МН, МН*м, МН*м]
        """
        f = np.zeros(3)
        combo = self.loadcombos[combo_name]
        for case, factor in combo.factors.items():
            for load in self.Loads:
                if load[3] == case:
                    f[0] += factor * load[0] / 1000
                    f[1] += factor * load[1] / 1000
                    f[2] += factor * load[2] / 1000
        return f

    def analyze(self, combo_name, kt, gb3, acc):
        """
        Расчет железобетонного сечения.

        :param combo_name: Имя расчетной комбинации нагрузок
        :param kt: Коэффициент учета растяжения бетона
        :param gb3: Коэффициент gb3 бетона
        :param acc: Точность расчета
        :return:
        """

        vv = np.vectorize(self.vi)
        vsigmac = np.vectorize(Sig.sigmac)
        vsigmas = np.vectorize(Sig.sigmas)
        s_b = [self.c_p['Rb'] * gb3, self.c_p['Rb'] * 0.6 * gb3, self.c_p['Rbt'] * 0.6 * kt, self.c_p['Rbt'] * kt]
        e_b = [self.c_p['eb2'], self.c_p['eb0'], s_b[1] / self.c_p['E'], s_b[2] / self.c_p['E'], self.c_p['ebt0'],
               self.c_p['ebt2']]
        xbi = self.c_g[0]
        ybi = self.c_g[1]
        abi = self.c_g[2]
        zb = self.c_g[3]
        n_b = len(xbi)
        ebi = np.linspace(self.c_p['E'], self.c_p['E'], n_b)
        xsj = []
        ysj = []
        asj = []
        rsc = []
        rs = []
        esc2 = []
        esc0 = []
        es0 = []
        es2 = []
        esj = []
        for name in self.rebars.keys():
            xsj.append(self.rebars[name].x)
            ysj.append(self.rebars[name].y)
            asj.append(self.rebars[name].asj)
            rsc.append(self.rebars[name].st['Rsc'])
            rs.append(self.rebars[name].st['Rs'])
            esc2.append(self.rebars[name].st['esc2'])
            esc0.append(self.rebars[name].st['esc0'])
            es0.append(self.rebars[name].st['es0'])
            es2.append(self.rebars[name].st['es2'])
            esj.append(self.rebars[name].st['E'])
        n_s = len(xsj)
        zs = np.transpose(np.array([np.ones(n_s), xsj, ysj]))
        f = self.force(combo_name)
        vbi = np.linspace(1, 1, n_b)
        vsj = np.linspace(1, 1, n_s)
        d = self.d(abi, xbi, ybi, ebi, vbi) + self.d(np.array(asj), np.array(xsj), np.array(ysj), np.array(esj), vsj)
        u = Calculation.calc(d, f)  # Вектор общих деформаций
        eb = zb.dot(u)  # Деформации бетона
        sb = vsigmac(eb, *e_b, *s_b, ebi)  # Напряжения в бетоне
        es = zs.dot(u)  # Деформации арматуры
        ss = np.zeros(n_s)  # Напряжения в арматуре
        for i in range(n_s):
            ss[i] = Sig.sigmas(es[i], esc2[i], esc0[i], es0[i], es2[i], rsc[i], rs[i], esj[i])
        du = 0.1
        it = 0
        while du >= acc:
            it += 1
            vb = vv(sb, ebi, eb)
            vs = vv(ss, esj, es)
            d = self.d(abi, xbi, ybi, ebi, vb) + self.d(np.array(asj), np.array(xsj), np.array(ysj), np.array(esj), vs)
            u_f = Calculation.calc(d, f)  # Вектор общих деформаций
            eb = zb.dot(u_f)  # Деформации бетона
            sb = vsigmac(eb, *e_b, *s_b, ebi)  # Напряжения в бетоне
            es = zs.dot(u_f)  # Деформации арматуры
            ss = np.zeros(n_s)  # Напряжения в арматуре
            for i in range(n_s):
                ss[i] = Sig.sigmas(es[i], esc2[i], esc0[i], es0[i], es2[i], rsc[i], rs[i], esj[i])
            du = np.max(abs(u - u_f))
            u = u_f  # Вектор общих деформаций
        print('Решение получено')
        print('Выполнено', it, 'итераций')
        print('Бетон класса:', self.section.grade)
        print('Коэффициент работы бетона на растяжение: ', kt)
        print('Коэффициент gb3: ', gb3)
        res = Result(vsigmac, vsigmas, self.section, self.rebars)
        res.results(f, u, abi, xbi, ybi, e_b, eb, s_b, sb, asj, xsj, ysj, es, ss, self.c_g, self.c_p)
