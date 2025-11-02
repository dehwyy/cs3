class Microprocessor:
    def __init__(self, id, model, clock_speed_ghz, computer_id):
        self.id = id
        self.model = model
        self.clock_speed_ghz = clock_speed_ghz 
        self.computer_id = computer_id

class Computer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MicroprocessorComputer:
    def __init__(self, computer_id, microprocessor_id):
        self.computer_id = computer_id
        self.microprocessor_id = microprocessor_id

computers = [
    Computer(1, "Игровой ПК 'Аврора'"),
    Computer(2, "Игровой ПК 'Счастье'"),
    Computer(3, "Ноутбук 'HP'"),
    Computer(4, "Ноутбук 'Титан'"),
]

microprocessors = [
    Microprocessor(1, "Intel Core i9-13900X", 5.8, 1),
    Microprocessor(2, "AMD Ryzen 9 7950X", 5.7, 1),
    Microprocessor(3, "Intel Core i7-13700", 5.2, 2),
    Microprocessor(4, "AMD Ryzen 7 7800X3D", 5.0, 3),
    Microprocessor(5, "Intel Xeon W-3400", 4.8, 4),
    Microprocessor(6, "AMD EPYC 9654", 3.7, 4),
]

microprocessors_computers = [
    MicroprocessorComputer(1, 1),
    MicroprocessorComputer(1, 2), 
    MicroprocessorComputer(2, 3),
    MicroprocessorComputer(3, 4),
    MicroprocessorComputer(4, 5),
    MicroprocessorComputer(4, 6),
    MicroprocessorComputer(1, 3),
    MicroprocessorComputer(2, 1),
]

def main():
    one_to_many = [[proc.model, proc.clock_speed_ghz, comp.name]
                   for proc in microprocessors
                   for comp in computers
                   if proc.computer_id == comp.id]

    print("--- Запрос Б1 ---")
    print("Список всех связанных микропроцессоров и компьютеров (1:M), отсортированный по моделям процессоров:")
    arr1 = sorted(one_to_many, key=lambda x: x[0])
    for i in arr1:
        print(f"  Процессор: {i[0]}, Частота: {i[1]} ГГц, Компьютер: {i[2]}")


    print("\n--- Запрос Б2 ---")
    print('Список компьютеров с количеством процессоров в каждом (1:M), отсортированный по количеству (по возрастанию):')

    arr2 = []
    for comp in computers:
        procs_in_comp = list(filter(lambda x: x[2] == comp.name, one_to_many))
        
        if len(procs_in_comp) > 0:
            arr2.append((comp.name, len(procs_in_comp)))

    arr2.sort(key=lambda x: x[1])
    for i in arr2:
        print(f"  Компьютер: {i[0]}, Количество процессоров: {i[1]}")


    print("\n--- Запрос Б3 ---")
    print("Список всех процессоров, у которых модель заканчивается на 'X', и названия их компьютеров (M:M):")

    many_to_many_first = [[comp.name, mc.computer_id, mc.microprocessor_id]
                          for comp in computers
                          for mc in microprocessors_computers
                          if comp.id == mc.computer_id]

    many_to_many = [[proc.model, comp_name]
                    for comp_name, comp_id, proc_id in many_to_many_first
                    for proc in microprocessors
                    if proc.id == proc_id]

    arr3 = []
    for model, comp_name in many_to_many:
        if model.endswith("X"):
            arr3.append([model, comp_name])

    arr3.sort(key=lambda x: x[0])
    for i in arr3:
        print(f"  Процессор: {i[0]}, Компьютер: {i[1]}")

if __name__ == "__main__":
    main()
