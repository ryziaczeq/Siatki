from PIL import Image, ImageDraw, ImageFont
import math

im = Image.open('v1.png')
im = im.convert('RGB')
print(im.size)
iter1 = 0


def to_check_triangleIsTriangle(to_check_triangle, t):
    l = [point_on_triangle(to_check_triangle.p1, t), point_on_triangle(to_check_triangle.p2,
                                                                       t), point_on_triangle(to_check_triangle.p3,
                                                                                             t)]

    if l.count(True) > 0:
        return True
    return False


def porownaj(to_check_triangle, t):
    l = [t.p1 in (to_check_triangle.p1, to_check_triangle.p2, to_check_triangle.p3),
         t.p2 in (to_check_triangle.p1, to_check_triangle.p2, to_check_triangle.p3),
         t.p3 in (to_check_triangle.p1, to_check_triangle.p2, to_check_triangle.p3),
         ]

    if l.count(True) > 0:
        return True
    return False


def triangle_on_triangle(to_check_triangle, t):
    # Wylicz poziom adaptacj
    if to_check_triangle.adaptation - t.adaptation == 1:
        wylicz = wylicz_pkt(t, False)
        ll = [porownaj(to_check_triangle, wylicz[0]), porownaj(to_check_triangle, wylicz[1]),
              porownaj(to_check_triangle, wylicz[2]), porownaj(to_check_triangle, wylicz[3])]
    elif to_check_triangle.adaptation - t.adaptation == 1:
        wylicz = wylicz_pkt(to_check_triangle, False)
        ll = [porownaj(t, wylicz[0]), porownaj(t, wylicz[1]),
              porownaj(t, wylicz[2]), porownaj(t, wylicz[3])]
    else:
        return False

    if ll.count(True) > 0:
        return True
    return False


def point_on_triangle(to_check, t):
    return point_on_line(to_check, t.p1, t.p2) or point_on_line(to_check, t.p2, t.p3) or point_on_line(to_check, t.p3,
                                                                                                       t.p1)


def point_on_line(to_check, point1, point2):
    dxc = to_check[0] - point1[0]
    dyc = to_check[1] - point1[1]

    dxl = point2[0] - point1[0]
    dyl = point2[1] - point1[1]

    cross = dxc * dyl - dyc * dxl
    if cross == 0:
        return True
    return False


def set_neighbours(t1, l):
    set_of_neighbours = []
    for i1, triangle in enumerate(l):
        # TODO Powinienem Lamac tylko jak jest roznica apadpatacji!!!
        if t1.to_break and abs(
                t1.adaptation - triangle.adaptation) > 0 and triangle_on_triangle(t1,
                                                                                  triangle):  # and l[i1].breakable():

            l[i1].to_break = True
            # TODO Sprawdz Sasiada Sasiada czy mozesz dac tu TRUE
            set_of_neighbours.append(l[i1])
    return set_of_neighbours


def wylicz_pkt(t0, wylicz=True):
    pkt1 = t0.p1
    pkt2 = t0.p2
    pkt3 = t0.p3

    x1 = pkt1[0]
    y1 = pkt1[1]

    x2 = pkt2[0]
    y2 = pkt2[1]

    x3 = pkt3[0]
    y3 = pkt3[1]

    n1_x = math.floor((x2 + x3) / 2.)
    n1_y = math.floor((y2 + y3) / 2.)
    n2_x = math.floor((x3 + x1) / 2.)
    n2_y = math.floor((y3 + y1) / 2.)
    n3_x = math.floor((x1 + x2) / 2.)
    n3_y = math.floor((y1 + y2) / 2.)

    n1 = (n1_x, n1_y)
    n2 = (n2_x, n2_y)
    n3 = (n3_x, n3_y)

    # Powstaja 4 trojkoty
    # t1 = (pkt1, n3, n2)
    # t2 = (n1, n2, n3)
    # t3 = (n1, n3, pkt2)
    # t4 = (pkt3, n2, n1)

    t1 = Triangle(pkt1, n3, n2, t0.adaptation + 1, False, wylicz)
    t2 = Triangle(n1, n2, n3, t0.adaptation + 1, False, wylicz)
    t3 = Triangle(n1, n3, pkt2, t0.adaptation + 1, False, wylicz)
    t4 = Triangle(pkt3, n2, n1, t0.adaptation + 1, False, wylicz)

    return [t1, t2, t3, t4]


def save_file_with_to_break(result1):
    global iter1
    iter1 += 1

    new_im_iter = Image.new("RGB", im.size, 'white')
    draw_iter = ImageDraw.Draw(new_im_iter)
    for i_iter in result1:
        draw_iter.polygon([i_iter.p1, i_iter.p2, i_iter.p3], i_iter.calculate_color(), 'green')
        draw_iter.text(i_iter.calculate_centroid(),
                       str(i_iter.adaptation),
                       # + "_" + str(int(i_iter.to_break)) + "_" + str(i_iter.black) + "_" + str(i_iter.white),
                       'red',
                       ImageFont.truetype("arial.ttf", 10))
    new_im_iter.save("C:/Repos/py/Archiwum/Nowyfolder/iter/" + str(iter1) + '_iter_sama_siatka.png')


def algorytm(tablica_trojkatow):
    for t in tablica_trojkatow:
        # Calculate Error

        # Make decision(Set toBreak flag)
        if t.is_big_error() and t.breakable() and t.adaptation < 15:
            t.to_break = True

    # Ustaw Flagi dla sasiadow
    set_of_neighbours = []
    for t in tablica_trojkatow:
        set_of_neighbours = set_neighbours(t, tablica_trojkatow)

    # Dodatkowe ustawianie
    for t in set_of_neighbours:
        set_of_neighbours = set_neighbours(t, tablica_trojkatow)

    # Save - checkpoint
    save_file_with_to_break(tablica_trojkatow)

    # Break
    new_tablica = []
    for t in tablica_trojkatow:
        # Algorytm to repeat
        if t.to_break:
            new_tablica += wylicz_pkt(t)
        else:
            new_tablica += [t]

    # Oznacza ze cos doszlo
    if len(new_tablica) != len(tablica_trojkatow):
        print("roznica = " + str(len(new_tablica)) + "," + str(len(tablica_trojkatow)))
        return algorytm(new_tablica)
    else:
        return tablica_trojkatow


class Triangle:
    def __init__(self, p1, p2, p3, adaptation, to_break, wylicz=True):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.adaptation = adaptation
        self.to_break = to_break
        if wylicz:
            black_and_white = self.calculate_black_and_white()
            self.black = black_and_white[0]
            self.white = black_and_white[1]

    def __str__(self):
        return str(self.p1) + "," + str(self.p2) + "," + str(self.p3) + "," + str(self.adaptation) + "," + str(
            self.to_break)

    def calculate_color(self):
        if self.black >= 0.5:
            return 0, 0, 0
        if self.white >= 0.5:
            return 255, 255, 255
        print(str(self.black) + "," + str(self.white))

    def is_big_error(self):
        if self.black > 0.95:
            return False
        if self.white > 0.95:
            return False
        return True

    def calculate_centroid(self):
        return math.floor((self.p1[0] + self.p2[0] + self.p3[0]) / 3), math.floor(
            (self.p1[1] + self.p2[1] + self.p3[1]) / 3)

    def calculate_black_and_white(self):
        # Narysowac go i sprawdzic jakie pkt sa czarne
        temp_im = Image.new("RGB", im.size, 'white')
        tem_draw = ImageDraw.Draw(temp_im)
        tem_draw.polygon([self.p1, self.p2, self.p3], None, 'black')
        czarne = 0
        biale = 0
        suma = 0
        x_min = min(self.p1[0], self.p2[0], self.p3[0])
        x_max = max(self.p1[0], self.p2[0], self.p3[0])
        y_min = min(self.p1[1], self.p2[1], self.p3[1])
        y_max = max(self.p1[1], self.p2[1], self.p3[1])
        for i1 in range(x_min, x_max):
            for j1 in range(y_min, y_max):
                # Pkt w trojkacie
                if temp_im.getpixel((i1, j1)) == (0, 0, 0):
                    # Sprawdz normalny kolor
                    color = im.getpixel((i1, j1))
                    suma += 1
                    if color == (0, 0, 0):
                        czarne += 1
                    elif color == (255, 255, 255):
                        biale += 1
                    else:
                        print(color)
        # print(str(biale / suma) + "," + str(czarne / suma) + "," + str(suma))
        return czarne / suma, biale / suma

    def breakable(self):
        area = math.fabs(
            self.p1[0] * (self.p2[1] - self.p3[1]) + self.p2[0] * (self.p3[1] - self.p1[1]) + self.p3[0] * (
                    self.p1[1] - self.p2[1]) / 2.)

        # print(area)
        if area > 2_000.:
            return True
        else:
            return False


if __name__ == '__main__':
    pkt01 = (0, 0)
    pkt02 = (0, im.size[1] - 1)
    pkt03 = (im.size[0] - 1, 0)
    pkt04 = (im.size[0] - 1, im.size[1] - 1)
    # print(pkt01, pkt02, pkt03)
    # print(pkt02, pkt03, pkt04)

    tt = []
    tt.append(Triangle(pkt01, pkt02, pkt03, 1, False))
    tt.append(Triangle(pkt02, pkt03, pkt04, 1, False))

    result = algorytm(tt)
    print("done")

    new_im = Image.new("RGB", im.size, 'white')
    draw = ImageDraw.Draw(new_im)
    for i in result:
        draw.polygon([i.p1, i.p2, i.p3], i.calculate_color(), 'green')
        # draw.text(i.calculate_centroid(), str(i.adaptation), 'red', ImageFont.truetype("arial.ttf", 10))
    new_im.save('dupa.png')
    print("done")

    if to_check_f(result):
        print("dupa na koncu")
