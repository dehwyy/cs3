from operator import itemgetter

class File:
    """Файл"""
    def __init__(self, id, name, size, catalog_id):
        self.id = id
        self.name = name
        self.size = size  # Количественный признак (аналог зарплаты) 
        self.catalog_id = catalog_id # Для связи один-ко-многим [cite: 9]

class Catalog:
    """Каталог файлов"""
    def __init__(self, id, name):
        self.id = id
        self.name = name

class FileCatalog:
    """
    'Файлы каталога' для реализации
    связи многие-ко-многим [cite: 13]
    """
    def __init__(self, catalog_id, file_id):
        self.catalog_id = catalog_id
        self.file_id = file_id

# Каталоги [cite: 10]
catalogs = [
    Catalog(1, 'Документы'),
    Catalog(2, 'Изображения'),
    Catalog(3, 'Системный каталог'),
    Catalog(4, 'Музыка'),
    Catalog(5, 'Временный каталог'),
]

# Файлы [cite: 5]
files = [
    File(1, 'отчет.docx', 150, 1),
    File(2, 'резюме.pdf', 300, 1),
    File(3, 'photo_1.jpg', 1024, 2),
    File(4, 'logo.png', 512, 2),
    File(5, 'kernel.dll', 2048, 3),
    File(6, 'song.mp3', 4096, 4),
    File(7, 'temp_file.tmp', 100, 5),
    File(8, 'archive.zip', 5120, 1), # Еще один файл в Документах
]

# Файлы и каталоги (многие-ко-многим) 
files_catalogs = [
    FileCatalog(1, 1), # Документы -> отчет.docx
    FileCatalog(1, 2), # Документы -> резюме.pdf
    FileCatalog(1, 8), # Документы -> archive.zip
    FileCatalog(2, 3), # Изображения -> photo_1.jpg
    FileCatalog(2, 4), # Изображения -> logo.png
    FileCatalog(3, 5), # Системный каталог -> kernel.dll
    FileCatalog(4, 6), # Музыка -> song.mp3
    FileCatalog(5, 7), # Временный каталог -> temp_file.tmp

    # Добавляем связи многие-ко-многим
    # Допустим, логотип используется и в документах
    FileCatalog(1, 4), # Документы -> logo.png
    # И системный файл упоминается в документах
    FileCatalog(1, 5)  # Документы -> kernel.dll
]

def main():
    """Основная функция"""

    # --- Подготовка данных ---

    # Соединение данных один-ко-многим (Файл -> Каталог)
    # (Имя файла, Размер файла, Имя каталога)
    one_to_many = [(f.name, f.size, c.name)
                   for c in catalogs
                   for f in files
                   if f.catalog_id == c.id]

    # Соединение данных многие-ко-многим
    # 1. Промежуточное соединение
    many_to_many_temp = [(c.name, fc.catalog_id, fc.file_id)
                         for c in catalogs
                         for fc in files_catalogs
                         if c.id == fc.catalog_id]
    
    # 2. Основное соединение
    # (Имя файла, Размер файла, Имя каталога)
    many_to_many = [(f.name, f.size, cat_name)
                    for cat_name, cat_id, file_id in many_to_many_temp
                    for f in files if f.id == file_id]

    # --- Выполнение запросов (Вариант А) ---

    print('Задание A1')
    # [cite: 25] "Выведите список всех связанных сотрудников и отделов, 
    # отсортированный по отделам..."
    # Адаптация: Выводим список (Файл, Каталог), отсортированный по Каталогам.
    res_1 = sorted(one_to_many, key=itemgetter(2))
    print(res_1)


    print('\nЗадание A2')
    # [cite: 26] "Выведите список отделов с суммарной зарплатой сотрудников... 
    # отсортированный по суммарной зарплате."
    # Адаптация: Выводим список каталогов с суммарным размером файлов, 
    # отсортированный по суммарному размеру.
    res_2_unsorted = []
    # Перебираем все каталоги
    for c in catalogs:
        # Список файлов в текущем каталоге (из one_to_many)
        c_files = list(filter(lambda i: i[2] == c.name, one_to_many))
        # Если каталог не пустой
        if len(c_files) > 0:
            # Размеры файлов в каталоге
            c_sizes = [size for _, size, _ in c_files]
            # Суммарный размер
            c_sizes_sum = sum(c_sizes)
            res_2_unsorted.append((c.name, c_sizes_sum))

    # Сортировка по суммарному размеру (по убыванию)
    res_2 = sorted(res_2_unsorted, key=itemgetter(1), reverse=True)
    print(res_2)


    print('\nЗадание A3')
    # [cite: 27] "Выведите список всех отделов, у которых в названии 
    # присутствует слово «отдел», и список работающих в них сотрудников."
    # Адаптация: Выводим список каталогов, у которых в названии есть 
    # слово "каталог", и список их файлов (из many-to-many).
    res_3 = {}
    # Перебираем все каталоги
    for c in catalogs:
        # Ищем слово "каталог" в названии (без учета регистра)
        if 'каталог' in c.name.lower():
            # Список файлов в этом каталоге (из many_to_many)
            c_files = list(filter(lambda i: i[2] == c.name, many_to_many))
            # Только имена файлов
            c_files_names = [name for name, _, _ in c_files]
            # Добавляем результат в словарь
            res_3[c.name] = c_files_names
    print(res_3)


if __name__ == '__main__':
    main()
