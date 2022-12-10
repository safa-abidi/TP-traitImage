from random import randrange
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label

import os

from kivy.uix.textinput import TextInput


def get_params(nom):
    mat = lire(nom)
    file_type = nom.split(".")[1]
    lx = len(mat[0])
    ly = len(mat)
    return {'mat': mat, 'file_type': file_type, 'lx': lx, 'ly': ly}


def lire(nom):
    file = open(nom, 'r')
    file.seek(0)
    file_type = str(file.readline()).strip()
    comment = file.readline()
    file_size = file.readline()
    file_size = file_size.split(' ')
    ly = int(file_size[1])
    lx = int(file_size[0])
    val_size = file.readline()

    mat = list(list([]))

    for y in range(0, ly):
        line = file.readline()
        pixels = line.split(' ')
        if file_type == "P2":
            mat.append(pixels)
            mat[y][lx - 1] = mat[y][lx - 1].strip()
        elif file_type == "P3":
            row = list()
            for x in range(0, lx * 3, 3):
                row.append(list([pixels[x], pixels[x + 1], pixels[x + 2]]))
            mat.append(row)
            mat[y][lx - 1][2] = mat[y][lx - 1][2].strip()
    file.close()
    return mat


def ecrire(nom, mat):
    file = open(nom, 'w')
    file.seek(0)
    file_type = nom.split(".")[1]

    lx = len(mat[0])
    ly = len(mat)

    if file_type == "pgm":
        file.write("P2\n")
    else:
        file.write("P3\n")
    file.write("# " + nom + "nbr de lignes = " + str(ly) + "nbre de colonnes = " + str(lx) + "\n")
    file.write(str(lx) + " " + str(ly) + "\n")
    file.write("255" + "\n")

    for y in range(0, ly):
        line = ""
        for x in range(0, lx):
            if file_type == "pgm":
                line += str(mat[y][x]) + " "
            elif file_type == "ppm":
                line += mat[y][x][0] + " " + mat[y][x][1] + " " + mat[y][x][2] + " "
        file.write(line[:len(line) - 1] + "\n")
    file.close()


def moy(nom):
    mat = lire(nom)
    file_type = nom.split(".")[1]
    lx = len(mat[0])
    ly = len(mat)
    s = list([0, 0, 0])
    for i in range(0, ly):
        for j in range(0, lx):
            if file_type == "pgm":
                s[0] += int(mat[i][j])
            elif file_type == "ppm":
                s[0] += int(mat[i][j][0])
                s[1] += int(mat[i][j][1])
                s[2] += int(mat[i][j][2])
    nb_pixels = lx * ly
    if file_type == "pgm":
        return s[0] / nb_pixels
    elif file_type == "ppm":
        return s[0] / nb_pixels, s[1] / nb_pixels, s[2] / nb_pixels


def ecart_type(nom):
    mat = lire(nom)
    file_type = nom.split(".")[1]
    lx = len(mat[0])
    ly = len(mat)
    et = list([0, 0, 0])
    m = moy(nom)
    print(m)
    for i in range(0, ly):
        for j in range(0, lx):
            if file_type == "pgm":
                et[0] += (int(mat[i][j]) - m) ** 2
            elif file_type == "ppm":
                et[0] += (int(mat[i][j][0]) - m[0]) ** 2
                et[1] += (int(mat[i][j][1]) - m[1]) ** 2
                et[2] += (int(mat[i][j][2]) - m[2]) ** 2
    nb_pixels = lx * ly
    if file_type == "pgm":
        return (et[0] / nb_pixels) ** 0.5
    elif file_type == "ppm":
        return (et[0] / nb_pixels) ** 0.5, (et[1] / nb_pixels) ** 0.5, (et[2] / nb_pixels) ** 0.5


def histogramme(nom):
    mat = lire(nom)
    file_type = nom.split(".")[1]
    lx = len(mat[0])
    ly = len(mat)
    if file_type == "pgm":
        h = [0] * 256
        for i in range(0, ly):
            for j in range(0, lx):
                k = int(mat[i][j])
                h[k] += 1
        return h
    elif file_type == "ppm":
        hr = hg = hb = [0] * 256
        for i in range(0, ly):
            for j in range(0, lx):
                [r, g, b] = int(mat[i][j])
                hr[r] += 1
                hg[g] += 1
                hb[b] += 1
        return [hr, hg, hb]


def histogrammeCumul(nom):
    hc = [0] * 256
    h = histogramme(nom)
    hc[0] = h[0]
    for i in range(1, 256):
        for j in range(0, i + 1):
            hc[i] += h[j]
    return hc


def probabilities(nom):
    mat = lire(nom)
    lx = len(mat[0])
    ly = len(mat)
    total = lx * ly
    h = histogramme(nom)
    p = [0.0] * 256
    for i in range(0, 256):
        p[i] = h[i] / total
    return p


def probabilitiesCumul(nom):
    p = probabilities(nom)
    pc = [0.0] * 256
    pc[0] = p[0]
    for i in range(1, 256):
        pc[i] = pc[i - 1] + p[i]
    return pc


def a_(nom):
    a = [0.0] * 256
    pc = probabilitiesCumul(nom)
    for i in range(0, 256):
        a[i] = 255 * pc[i]
    return a


def n1_(nom):
    a = a_(nom)
    n1 = [0] * 256
    for i in range(0, 256):
        n1[i] = int(a[i])
    return n1


def histogramme_egalisation(nom):
    h = histogramme(nom)
    n1 = n1_(nom)
    he = [0] * 256
    j = 0
    for i in range(0, 256):
        while j < 256 and n1[j] == i:
            he[i] += h[j]
            j += 1
    return he


def transformation_linear(points, nom):
    x = points[0][0]
    y = points[0][1]
    x1 = points[1][0]
    y1 = points[1][1]

    b = 0
    a = int(y / x)

    a1 = int((y1 - y) / (x1 - x))
    b1 = int(y1 - a1 * x1)

    a2 = int((255 - y1) / (255 - x1))
    b2 = 255 - a2 * 255

    mat = lire(nom)
    lx = len(mat[0])
    ly = len(mat)

    for i in range(0, ly):
        for j in range(0, lx):
            if int(mat[i][j]) <= x:
                mat[i][j] = str(a * int(mat[i][j]) + b)
            elif int(mat[i][j]) <= x1:
                mat[i][j] = str(a1 * int(mat[i][j]) + b1)
            else:
                mat[i][j] = str(a2 * int(mat[i][j]) + b2)
    return ecrire("temp_tl.pgm", mat)


def bruit(image):
    mat = lire(image)
    for i in range(0, len(mat)):
        for j in range(0, len(mat[0])):
            r = randrange(21)
            if r == 0:
                mat[i][j] = 0
            elif r == 20:
                mat[i][j] = 255
    return mat


def convolution(filter, image):
    mat = lire(image)
    result = mat
    s = 0.0
    for i in range(int(len(filter) / 2), len(mat) - int(len(filter) / 2)):
        for j in range(int(len(filter) / 2), len(mat[0]) - int(len(filter) / 2)):
            for k in range(int(-len(filter) / 2), int(len(filter) / 2) + 1):
                for z in range(int(-len(filter) / 2), int(len(filter) / 2) + 1):
                    s += float(mat[i + k][j + z]) * filter[k + int(len(filter) / 2)][z + int(len(filter) / 2)]
            if s < 0.0:
                s = 0.0
            elif s > 255.0:
                s = 255.0
            result[i][j] = int(s)
            s = 0.0
    return result


def moyenneur(taille, image):
    filt = [[1 / (taille ** 2)] * taille] * taille
    return convolution(filt, image)


def median(taille, image):
    mat = lire(image)
    result = mat
    med = [0] * (taille ** 2)
    for i in range(int(taille / 2), len(mat) - int(taille / 2)):
        for j in range(int(taille / 2), len(mat[0]) - int(taille / 2)):
            for k in range(int(-taille / 2), int(taille / 2) + 1):
                for z in range(int(-taille / 2), int(taille / 2) + 1):
                    med[(k * taille) + z] = int(mat[i + k][j + z])
            med.sort()
            result[i][j] = med[int((taille ** 2) / 2)]
    return result


def rehausser_contours(image):
    fh = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
    print(fh)
    return convolution(fh, image)


def SNR(image, filtered):
    mu = moy(image)
    mat_o = lire(image)
    mat_f = lire(filtered)
    s1 = 0
    s2 = 0
    for i in range(0, len(mat_o)):
        for j in range(0, len(mat_o[0])):
            s1 += (int(mat_o[i][j]) - mu) ** 2
            s2 += (int(mat_f[i][j]) - int(mat_o[i][j])) ** 2
    return -(s1 / s2) ** 0.5


def seuillage_manual(image, seuil_r, seuil_g, seuil_b):
    seuil = [seuil_r, seuil_g, seuil_b]
    mat_img = lire(image)
    ly = len(mat_img)
    lx = len(mat_img[0])
    for y in range(0, ly):
        for x in range(0, lx):
            for c in range(0, 3):
                if int(mat_img[y][x][c]) > seuil[c]:
                    mat_img[y][x][c] = '255'
                else:
                    mat_img[y][x][c] = '0'
    return mat_img


def seuillage_ETOU(image, seuil, flag):
    mat_img = lire(image)
    ly = len(mat_img)
    lx = len(mat_img[0])
    for y in range(0, ly):
        for x in range(0, lx):
            if flag == "ET":
                conserver = True
                for c in range(0, 3):
                    if int(mat_img[y][x][c]) > seuil:
                        conserver = conserver and True
                    else:
                        conserver = conserver and False
                if not (conserver):
                    mat_img[y][x] = ['0', '0', '0']
            elif flag == "OU":
                conserver = True
                for c in range(0, 3):
                    if int(mat_img[y][x][c]) > seuil:
                        conserver = conserver or True
                    else:
                        conserver = conserver or False
                    if not (conserver):
                        mat_img[y][x] = ['0', '0', '0']
    return mat_img


'''
chat_mat = lire('chat.pgm')
print(chat_mat)
ecrire("chat_new.pgm", chat_mat)
print(moy("chat.pgm"))
print(ecart_type("chat.pgm"))
'''
print(histogramme("C:\\Users\\Rayen\\OneDrive\\Documents\\Image Analysis\\TP1-traitImage-main\\chat_flou.pgm"))
'''
print(histogrammeCumul("chat.pgm"))
print(probabilities("chat.pgm"))
print(probabilitiesCumul("chat.pgm"))
print(a_("chat.pgm"))
print(n1_("chat.pgm"))
print(histogramme_egalisation("chat.pgm"))
transformation_linear([[20, 100], [100, 200]], "chat.pgm")
ecrire("chat_bruitié.pgm", bruit('chat.pgm'))
ecrire("chat_flou.pgm", moyenneur(3, "chat_bruitié.pgm"))
ecrire("chat_median.pgm", median(3, "chat_bruitié.pgm"))
ecrire("rehausser_chat.pgm", rehausser_contours("chat.pgm"))
print("SNR image filtrée en moyenneur :")
print(SNR("chat_bruitié.pgm", "chat_flou.pgm"))
print("SNR filtrée avec le median :")
print(SNR("chat_bruitié.pgm", "chat_median.pgm"))
felfel_ppm = lire("peppers.ppm")
mat_seuil = seuillage_manual("peppers.ppm", 128, 128, 128)
print(mat_seuil)
ecrire("felfel_new.ppm", mat_seuil)
felfel_et = seuillage_ETOU("felfel_new.ppm", 128, "ET")
felfel_ou = seuillage_ETOU("felfel_new.ppm", 128, "OU")
ecrire("felfel_et.ppm", felfel_et)
ecrire("felfel_ou.ppm", felfel_ou)
'''


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, picture, popup, root, p, x, console,m,e, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        self.box = BoxLayout(orientation="vertical", size=root.size, pos=root.pos, padding=(150, 0, 0, 70))
        self.add_widget(self.box)
        file_chooser = FileChooserIconView()
        self.box.add_widget(file_chooser)
        self.button_submit = Button(text="OK", size_hint=(None, None), size=(1064, 50))

        def recalculate_characteristics():
            moyenne = Label(text=("Moyenne : " + str(moy(picture.source))))
            ecart = Label(text=("Ecart Type : " + str(ecart_type(picture.source))))
            console.remove_widget(m)
            console.remove_widget(e)
            console.remove_widget(p)
            console.add_widget(moyenne)
            console.add_widget(ecart)
            plt.clf()
            plt.plot(x, histogramme(picture.source))
            console.remove_widget(p)
            plot = FigureCanvasKivyAgg(plt.gcf())
            console.add_widget(p)

        def load_file(instance):
            picture.source = file_chooser.selection[0]
            picture.reload()
            recalculate_characteristics()
            popup.dismiss()

        self.button_submit.bind(on_press=load_file)
        self.box.add_widget(self.button_submit)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, picture, plot,x,console,moyenne,ecart):
        self._popup = Popup(title="Load File", size_hint=(0.9, 0.9))
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, picture=picture, popup=self._popup, root=self, p=plot,x=x,console=console,m=moyenne,e=ecart)
        self._popup.content = content
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()


class Editor(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


class Picture(Scatter):
    source = StringProperty(None)


class Grid(GridLayout):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2
        self.left = GridLayout()
        self.left.cols = 1
        self.left.rows = 3
        self.layoutLeft = BoxLayout(orientation="vertical")

        def transform_in_range(n):
            if n > 255:
                return 255
            elif n < 0:
                return 0
            else:
                return n

        def LT(instance):
            x1 = transform_in_range(int(in_1.text))
            y1 = transform_in_range(int(in_2.text))
            x2 = transform_in_range(int(in_3.text))
            y2 = transform_in_range(int(in_4.text))
            transformation_linear([[x1, y1], [x2, y2]], self.picture.source)
            self.picture.source = "temp_tl.pgm"
            self.picture.reload()

        self.linearTransform = BoxLayout(orientation="vertical")
        btn_lt = Button(text="Transformation Linéaire", size_hint_x=None, width=300)
        btn_lt.bind(on_press=LT)
        box_lt = BoxLayout(orientation="horizontal", spacing=15)
        box_lt_pt1 = BoxLayout(orientation="horizontal", padding=20, spacing=7.5)
        box_lt_pt2 = BoxLayout(orientation="horizontal", padding=20, spacing=7.5)
        in_1 = TextInput(input_filter="int")
        in_2 = TextInput(input_filter="int")
        in_3 = TextInput(input_filter="int")
        in_4 = TextInput(input_filter="int")
        box_lt_pt1.add_widget(in_1)
        box_lt_pt1.add_widget(in_2)
        box_lt_pt2.add_widget(in_3)
        box_lt_pt2.add_widget(in_4)
        box_lt.add_widget(box_lt_pt1)
        box_lt.add_widget(box_lt_pt2)
        self.linearTransform.add_widget(btn_lt)
        self.linearTransform.add_widget(box_lt)
        self.hist = Button(text="Histogramme", size_hint_x=None, width=300)
        self.filter = Button(text="Filter", size_hint_x=None, width=300)

        def apply_filter(instance):
            self.filter_pop_up = Popup(title="Filter Size", size_hint=(0.5, 0.5))
            content = BoxLayout()
            filter_size = TextInput(input_filter="int")
            content.add_widget(filter_size)
            button_validate_filter_size = Button(text="OK")

            def open_filter(instance):
                self.filter_input = Popup(title="Filter", size_hint=(0.5, 0.5))
                content = BoxLayout(orientation="vertical")
                inputs = [[TextInput()] * int(filter_size.text)] * int(filter_size.text)
                for i in range(0, int(filter_size.text)):
                    line = BoxLayout(orientation="horizontal")
                    for j in range(0, int(filter_size.text)):
                        inputs[i][j] = TextInput(input_filter="float")
                        line.add_widget(inputs[i][j])
                    content.add_widget(line)
                validate_filter_input = Button(text="OK")

                def calculate_filtered_image(instance):
                    filter_mat = [[0.0] * int(filter_size.text)] * int(filter_size.text)
                    for i in range(0, int(filter_size.text)):
                        for j in range(0, int(filter_size.text)):
                            filter_mat[i][j] = float(inputs[i][j].text)
                    ecrire("temp_filtered.pgm", convolution(filter_mat, self.picture.source))
                    self.picture.source = "temp_filtered.pgm"
                    self.picture.reload()
                    self.filter_input.dismiss()
                    self.filter_pop_up.dismiss()

                validate_filter_input.bind(on_press=calculate_filtered_image)
                content.add_widget(validate_filter_input)
                self.filter_input.content = content
                self.filter_input.open()

            button_validate_filter_size.bind(on_press=open_filter)
            content.add_widget(button_validate_filter_size)
            self.filter_pop_up.content = content
            self.filter_pop_up.open()

        self.filter.bind(on_press=apply_filter)
        self.segment = Button(text="Segment", size_hint_x=None, width=300)
        self.seuillage = Button(text="Seuillage", size_hint_x=None, width=300)
        self.layoutLeft.add_widget(self.linearTransform)
        self.layoutLeft.add_widget(self.filter)
        self.layoutLeft.add_widget(self.segment)
        self.layoutLeft.add_widget(self.seuillage)
        try:
            self.picture = Image(source="chat.pgm", size_hint_x=None, width=1067, size_hint_y=None, height=550)
        except Exception as e:
            print(e)
        x = [0] * 256
        for i in range(0, 256):
            x[i] = i
        plt.xlabel('NdG', fontsize=18)
        plt.ylabel('H(n)', fontsize=16)
        plt.clf()
        plt.plot(x, histogramme(self.picture.source))
        self.console = BoxLayout(orientation="vertical")
        moyenne = Label(text=("Moyenne : " + str(moy(self.picture.source))))
        ecart = Label(text=("Ecart Type : " + str(ecart_type(self.picture.source))))
        self.console.add_widget(moyenne)
        self.console.add_widget(ecart)
        self.plot = FigureCanvasKivyAgg(plt.gcf())
        self.console.add_widget(self.plot)

        def import_file(instance):
            root = Root()
            root.show_load(picture=self.picture, plot=self.plot,x=x,console=self.console,moyenne=moyenne,ecart=ecart)

        self.importFile = Button(text="Import File", background_color=(0.18039215686, 0.76862745098, 0.71372549019, 1),
                                 size_hint_x=None, width=1067, size_hint_y=None, height=147)
        self.importFile.bind(on_press=import_file)
        self.add_widget(self.layoutLeft)
        self.add_widget(self.picture)
        self.add_widget(self.console)
        self.add_widget(self.importFile)


class GUI(App):
    def build(self):
        return Grid()


if __name__ == "__main__":
    GUI().run()
