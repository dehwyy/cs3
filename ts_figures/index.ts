interface Printable {
  Print(): void
}

abstract class Figure {
  constructor(public name: string) { }

  public abstract GetArea(): number
}

class Rectangle
  extends Figure
  implements Printable {
  constructor(
    name: string,
    private width: number,
    private height: number,
  ) {
    super(name)
  }

  Print() {
    console.log(`${this.name} (${this.width}x${this.height}), area=${this.GetArea()}`)
  }

  GetArea() {
    return this.width * this.height
  }
}

class Square
  extends Rectangle
  implements Printable {
  constructor(
    name: string,
    private side: number,
  ) {
    super(name, side, side)
  }

  override Print() {
    console.log(`${this.name} (${this.side}x${this.side}), area=${this.GetArea()}`)
  }

  override GetArea() {
    return this.side * this.side
  }
}

class Circle
  extends Figure
  implements Printable {
  constructor(
    name: string,
    private radius: number,
  ) {
    super(name)
  }

  Print() {
    console.log(`${this.name} with radius=${this.radius}, area=${this.GetArea()}`)
  }

  GetArea() {
    return Math.PI * this.radius * this.radius
  }
}

function Print(...printables: Printable[]) {
  for (const printable of printables) {
    printable.Print()
  }
}

function GetTotalAreaOfFigures(...figures: Figure[]) {
  let area = 0
  for (const figure of figures) {
    console.info(`Adding figure "${figure.name}" with area=${figure.GetArea()}...`)
    area += figure.GetArea()
  }
  return area
}

const square = new Square('Square', 3)
const rectangle = new Rectangle('Rectangle', 3, 4)
const circle = new Circle('Circle', 5)

Print(square, rectangle, circle)
console.log(GetTotalAreaOfFigures(square, rectangle, circle))
