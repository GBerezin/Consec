import matplotlib.pyplot as plt
import matplotlib.image as mpimg

plt.style.use('seaborn-whitegrid')


def strainstress(x, y, grade):
    """
    Диаграмма состояния.
    """

    fig, ax = plt.subplots(num='Диаграмма состояния ' + grade)
    ax.plot(x, y)
    ax.set_xlabel('Относительные деформации')
    ax.set_ylabel('Напряжения, МПа')
    plt.title('Диаграмма состояния ' + grade)
    ax.scatter(x, y, c='red', alpha=0.5)
    plt.show()


def loads(img):
    """
    Правило знаков нагрузок.

    :param img: Файл рисунка
    :return:
    """
    fig, ax = plt.subplots(num='Правило знаков нагрузок')
    ax.imshow(mpimg.imread(img))
    ax.axis('off')
    plt.title('Правило знаков нагрузок')
    plt.show()
