# Прямоугольное сечение
# Георгий Березин
from MemberSection.RConSect import FrameSec
import Materials as Mtr


def main():
    # Свойства материалов
    concrete, steel = Mtr.materials()

    # Создание нового прямоугольного жб сечения
    rect = FrameSec(concrete, steel)

    # Создание прямоугольного бетонного сечения
    rect.add_rect_section('B30', 500, 400, 10, 8)

    # Создание стержней
    rect.add_rebar('0', 'A500', 28, 210, -160)
    rect.add_rebar('1', 'A400', 14, 210, 0)
    rect.add_rebar('2', 'A500', 28, 210, 160)
    rect.add_rebar('3', 'A400', 14, 0, -160)
    rect.add_rebar('4', 'A400', 14, 0, 160)
    rect.add_rebar('5', 'A500', 28, -210, -160)
    rect.add_rebar('6', 'A400', 14, -210, 0)
    rect.add_rebar('7', 'A500', 28, -210, 160)

    # Добавить нагрузки
    rect.add_load(-1000, 160, 70, case='D')
    rect.add_load(-500, 160, 70, case='L')

    # Создание комбинаций
    rect.add_load_combo('1.0D+1.0L', factors={'D': 1.0, 'L': 1.0})
    rect.add_load_combo('1.1D+1.2L', factors={'D': 1.1, 'L': 1.2})

    combo_name = '1.0D+1.0L'
    kt = 0
    gb3 = 1
    rect.analyze(combo_name, kt, gb3, 0.0000001)


if __name__ == '__main__':
    main()
