import sys
import math

class BiquadraticSolver:
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def discriminant(self):
        return self.b*self.b - 4*self.a*self.c

    def solve(self):
        d = self.discriminant()
        print(f"Дискриминант: {d}")
        if d < 0:
            print("Действительных корней нет.")
            return []

        if d > 1e16:
            print("Дискриминант слишком большой.")
            return []

        # Use formula
        sqrt_d = math.sqrt(d)
        x1 = (-self.b + sqrt_d) / (2*self.a)
        x2 = (-self.b - sqrt_d) / (2*self.a)

        # Get roots result
        roots = [x1]
        if x1 != x2:
            roots = [x1, x2]

        return roots

# Helper function
def get_coefficient(name: str, args: [str], index: int):
    while True:
        try:
            # Try to retrieve coefficient from args
            if len(args) > index:
                return float(args[index])

            # or ask for it
            return float(input(f"Введите коэффициент {name}: "))
        except ValueError:
            print(f"Некорректное значение для {name}, попробуйте снова.")
            # Clear argument value for next try if providede
            if len(args) > index:
                args[index] = None

def main():
    # Get coefficients
    args = sys.argv
    a = get_coefficient("A", args, 1)
    if a == 0:
        print("Коэффициент A в квадратном уравнении не может быть равен 0.")
        return

    b = get_coefficient("B", args, 2)
    c = get_coefficient("C", args, 3)

    # Initialize class
    solver = BiquadraticSolver(a, b, c)
    # solve
    roots = solver.solve()
    if roots:
        print("Действительные корни:", roots)
        return

    print("Корней нет.")

if __name__ == "__main__":
    main()
