import math
from collections import namedtuple
import turtle

STEP = 5
Point = namedtuple('Point', ['x', 'y'])

def angle_two_point(p1, p2):
    """Определяем угол для направления черепашки."""
    dy = p2.y - p1.y
    dx = p2.x - p1.x
    return math.atan2(dy, dx) * 180. / math.pi

def draw_box(p1, p2):
    """Рисуем прямоугольник по двум точкам."""
    for y_left in range(p1.y, p2.y + STEP, STEP):
        yield (90, p1.x, y_left)
    for x_top in range(p1.x, p2.x + STEP, STEP):
        yield (0, x_top, p2.y)
    for y_right in range(p2.y, p1.y - STEP, -STEP):
        yield (-90, p2.x, y_right)
    for x_down in range(p2.x, p1.x - STEP, -STEP):
        yield (180, x_down, p1.y)

def draw_circle(center, radius):
    """Рисуем круг по заданному центру и радиусу."""
    points = []
    for angle in range(0, 360, STEP):
        x = center.x + radius * math.cos(math.radians(angle))
        y = center.y + radius * math.sin(math.radians(angle))
        points.append((x, y))
    return points

def draw_nose(center, width, height):
    """Рисуем нос с помощью параболической кривой."""
    points = []
    for x in range(-width, width + 1):
        y = -height * (x / width) ** 2 + height  
        points.append((center.x + x, center.y + y))
    return points

# Инициализация черепашки
bob = turtle.Turtle()
bob.screen.setup(400, 400)
bob.screen.bgcolor("lightgreen")
bob.shape("turtle")
bob.pencolor("red")
bob.pensize(3)

# Контур лица
face_box = (Point(-100, -100), Point(100, 100))
bob.penup()
bob.setpos(face_box[0])
bob.pendown()
for angle, *position in draw_box(*face_box):
    bob.setheading(angle)
    bob.setpos(*position)

# Глаза
left_eye = Point(-40, 30)
right_eye = Point(40, 30)
eye_radius = 10

# Левый глаз
bob.penup()
left_eye_points = draw_circle(left_eye, eye_radius)
bob.setpos(left_eye_points[0])
bob.pendown()
for position in left_eye_points:
    bob.setpos(position)

# Правый глаз
bob.penup()
right_eye_points = draw_circle(right_eye, eye_radius)
bob.setpos(right_eye_points[0])
bob.pendown()
for position in right_eye_points:
    bob.setpos(position)

# Рисуем нос
nose_center = Point(0, 10)
nose_width = 10
nose_height = 5
bob.penup()
nose_points = draw_nose(nose_center, nose_width, nose_height)
bob.setpos(nose_points[0])
bob.pendown()
for position in nose_points:
    bob.setpos(position)

# Нейтральный рот
bob.penup()
bob.setpos(-40, -30)  
bob.pendown()
bob.setheading(0)  
bob.forward(80)  

# Челка
bob.penup()
bob.setpos(-20, 100)  
bob.pendown()
bob.setheading(-30)  
bob.forward(30)      

bob.penup()
bob.setpos(0, 100)   
bob.pendown()
bob.setheading(-60)  
bob.forward(30)      

bob.penup()
bob.setpos(20, 100)  
bob.pendown()
bob.setheading(-30)  
bob.forward(30)      

bob.hideturtle()
bob.screen.mainloop()
