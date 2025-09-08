

/// <summary>
///   Интерфейс для вывода информации о классе
/// </summary>
interface IPrint
{
  void Print();
}


/// <summary>
///   Абстрактный класс для фигур
/// </summary>
abstract class GeometricFigure
{
  public virtual double GetArea() => 0; // По заданию "виртуальный метод", хотя я бы сделал его "абстрактным"
}

/// <summary>
///   Класс прямоугольника
/// </summary>
class Rectangle : GeometricFigure, IPrint
{

  public double Width { get; set; }
  public double Height { get; set; }

  public Rectangle(double width, double height)
  {
    Width = width;
    Height = height;
  }

  public override double GetArea()
  {
    return Width * Height;
  }

  public override string ToString()
  {
    return $"Прямоугольник: ширина = {Width}, высота = {Height}, площадь = {GetArea()}";
  }

  public void Print()
  {
    Console.WriteLine(ToString());
  }
}

/// <summary>
///   Класс квадрата
/// </summary>
class Square : Rectangle
{
  public Square(double side) : base(side, side) { }

  public override string ToString()
  {

    return $"Квадрат: сторона = {Width}, площадь = {GetArea()}";
  }
}

/// <summary>
///   Класс круга
/// </summary>
class Circle : GeometricFigure, IPrint
{
  public double Radius { get; set; }

  public Circle(double radius)
  {
    Radius = radius;
  }

  public override double GetArea()
  {
    return Math.PI * Radius * Radius;
  }

  public override string ToString()
  {
    return $"Круг: радиус = {Radius}, площадь = {GetArea():F2}";
  }


  public void Print()
  {
    Console.WriteLine(ToString());
  }
}

/// <summary>
///   Класс программы
/// </summary>
class Program
{
  /// <summary>
  ///   Главный метод (запускает программу)
  /// </summary>
  static void Main()
  {


    Rectangle rect = new Rectangle(4, 6);
    rect.Print();

    Square sq = new Square(5);
    sq.Print();

    Circle circle = new Circle(3);
    circle.Print();

    Console.WriteLine("\nВывод через полиморфизм:");

    PolymorphicMain();
  }

  /// <summary>
  ///   Главный метод с полиморфизмом
  /// </summary>
  static void PolymorphicMain()
  {
    IPrint[] figures = {
        new Rectangle(40, 60),
        new Square(5),
        new Circle(3)
    };

    foreach (var f in figures)
      f.Print();
  }
}
