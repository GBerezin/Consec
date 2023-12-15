def sigmac(eps, eb2, eb0, eb1, ebt1, ebt0, ebt2, rb, sb1, sbt1, rbt, e, k_rc):
    """
    Диаграмма состояния бетона.

    :param eps: Относительная деформация
    :param eb2: Относительная деформация укорочения
    :param eb0: Относительная деформация укорочения
    :param eb1: Относительная деформация укорочения
    :param ebt1: Относительная деформация удлинения
    :param ebt0: Относительная деформация удлинения
    :param ebt2: Относительная деформация удлинения
    :param rb: Расчетное сопротивление бетона осевому сжатию, МПа
    :param sb1: Напряжение сжатия
    :param sbt1: Напряжение растяжения
    :param rbt: Расчетное сопротивление бетона осевому растяжению, МПа
    :param e: Mодуль упругости, МПа
    :return: Напряжение, МПа
    """

    rb = rb * k_rc
    sb1 = sb1 * k_rc
    if eb0 >= eps:
        s = rb
    elif eb0 < eps < eb1:
        s = ((1 - sb1 / rb) * (eps - eb1) / (eb0 - eb1) + sb1 / rb) * rb
    elif eb1 <= eps < 0.0:
        s = e * eps
    elif ebt1 >= eps > 0.0 != sbt1:
        s = e * eps
    elif ebt1 < eps < ebt0 and rbt != 0.0:
        s = ((1 - sbt1 / rbt) * (eps - ebt1) / (ebt0 - ebt1) + sbt1 / rbt) * rbt
    elif ebt0 <= eps:
        s = rbt
    else:
        s = 0.0
    return s


def sigmas(eps, esc2, esc0, es0, es2, rsc, rs, e):
    """
    Диаграмма состояния арматурной стали.

    :param eps: Относительная деформация
    :param esc2: Относительная деформация укорочения
    :param esc0: Относительная деформация укорочения
    :param es0: Относительная деформация удлинения
    :param es2: Относительная деформация удлинения
    :param rsc: Расчетное сопротивление арматуры сжатию, МПа
    :param rs: Расчетное сопротивление арматуры растяжению, МПа
    :param e: Mодуль упругости, МПа
    :return: Напряжение, МПа
    """

    if esc0 >= eps:
        s = rsc
    elif esc0 < eps < es0:
        s = e * eps
    elif es0 <= eps:
        s = rs
    else:
        s = 0.0
    return s
