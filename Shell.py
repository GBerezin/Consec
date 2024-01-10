# Выделенный жб элемент оболочки
# Георгий Березин
from ShellElement.RConShell import ShellElem
import Materials as Mtr

def main():
    # Свойства материалов
    concrete, steel = Mtr.materials()

    # Создание нового выделенного жб элемента оболочки
    shell = ShellElem(concrete, steel)

    # Создание выделенного бетонного элемента оболочки
    shell.add_conc_element('B60', 500, 25)

    # Создание арматурных слоев
    shell.add_ply('0', 'A500', 25, 5, 178, 0)
    shell.add_ply('1', 'A500', 25, 5, 153, 90)
    shell.add_ply('2', 'A500', 25, 5, -153, 90)
    shell.add_ply('3', 'A500', 25, 5, -178, 0)

    # Добавить нагрузки
    shell.add_load(-50, 50, 0, 150, 150, 25, case='D')
    shell.add_load(-50, 50, 0, 150, 150, 25, case='L')

    # Создание комбинаций
    shell.add_load_combo('1.0D+1.0L', factors={'D': 1.0, 'L': 1.0})
    shell.add_load_combo('1.1D+1.2L', factors={'D': 1.1, 'L': 1.2})

    combo_name = '1.0D+1.0L'
    kt = 0
    gb3 = 1
    shell.analyze(combo_name, kt, gb3, 0, 0.0000001)


if __name__ == '__main__':
    main()
