from random import randrange


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
        elif file_type == "P3":
            row = list()
            for x in range(0, lx, 3):
                row.append((pixels[x], pixels[x + 1], pixels[x + 2]))
            mat.append(row)
        mat[y][lx - 1] = mat[y][lx - 1].strip()
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
    h = [0] * 256
    for i in range(0, ly):
        for j in range(0, lx):
            k = int(mat[i][j])
            h[k] += 1
    return h


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


def transformation_linear(points,nom):
    x = points[0][0]
    y = points[0][1]
    x1 = points[1][0]
    y1 = points[1][1]

    b = 0
    a = int(y/x)

    a1 = int((y1-y)/(x1-x))
    b1 = int(y1 - a1*x1)

    a2 = int((255 - y1)/(255 - x1))
    b2 = 255 - a2*255

    mat = lire(nom)
    lx = len(mat[0])
    ly = len(mat)

    for i in range(0, ly):
        for j in range(0, lx):
            if int(mat[i][j]) <= x:
                mat[i][j] = str(a*int(mat[i][j]) + b)
            elif int(mat[i][j]) <= x1:
                mat[i][j] = str(a1*int(mat[i][j]) + b1)
            else:
                mat[i][j] = str(a2 * int(mat[i][j]) + b2)
    return ecrire("chat_transformé.pgm", mat)


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


def convolution(filter,image):
    mat = lire(image)
    result = mat
    s = 0.0
    for i in range(int(len(filter)/2),len(mat)-int(len(filter)/2)):
        for j in range(int(len(filter)/2),len(mat[0])-int(len(filter)/2)):
            for k in range(int(-len(filter)/2), int(len(filter)/2)+1):
                for z in range(int(-len(filter)/2), int(len(filter)/2)+1):
                    s += float(mat[i+k][j+z])*filter[k+int(len(filter)/2)][z+int(len(filter)/2)]
            if s < 0.0:
                s = 0.0
            elif s > 255.0:
                s = 255.0
            result[i][j] = int(s)
            s = 0.0
    return result


def moyenneur(taille,image):
    filt = [[1/(taille**2)]*taille]*taille
    return convolution(filt, image)


def median(taille,image):
    mat = lire(image)
    result = mat
    med = [0] * (taille**2)
    for i in range(int(taille/2),len(mat)-int(taille/2)):
        for j in range(int(taille/2),len(mat[0])-int(taille/2)):
            for k in range(int(-taille/2), int(taille/2)+1):
                for z in range(int(-taille/2), int(taille/2)+1):
                    med[(k*taille)+z] = int(mat[i+k][j+z])
            med.sort()
            result[i][j] = med[int((taille**2)/2)]
    return result


def rehausser_contours(image):
    fh = [[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]
    print(fh)
    return convolution(fh,image)


def SNR(image,filtered):
    mu = moy(image)
    mat_o = lire(image)
    mat_f = lire(filtered)
    s1 = 0
    s2 = 0
    for i in range(0,len(mat_o)):
        for j in range(0,len(mat_o[0])):
            s1 += (int(mat_o[i][j]) - mu)**2
            s2 += (int(mat_f[i][j]) - int(mat_o[i][j]))**2
    return -(s1/s2)**0.5


chat_mat = lire('chat.pgm')
print(chat_mat)
ecrire("chat_new.pgm", chat_mat)
print(moy("chat.pgm"))
print(ecart_type("chat.pgm"))
print(histogramme("chat.pgm"))
print(histogrammeCumul("chat.pgm"))
print(probabilities("chat.pgm"))
print(probabilitiesCumul("chat.pgm"))
print(a_("chat.pgm"))
print(n1_("chat.pgm"))
print(histogramme_egalisation("chat.pgm"))
transformation_linear([[20,100],[100,200]],"chat.pgm")
ecrire("chat_bruitié.pgm",bruit('chat.pgm'))
ecrire("chat_flou.pgm",moyenneur(7,"chat_bruitié.pgm"))
ecrire("chat_median.pgm",median(3,"chat_bruitié.pgm"))
ecrire("rehausser_chat.pgm",rehausser_contours("chat.pgm"))
print("SNR image filtrée en moyenneur :")
print(SNR("chat.pgm","chat_flou.pgm"))
print("SNR filtrée avec le median :")
print(SNR("chat.pgm","chat_median.pgm"))
