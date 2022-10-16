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
                line += mat[y][x] + " "
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
                et[0] += (int(mat[i][j]) - m)**2
            elif file_type == "ppm":
                et[0] += (int(mat[i][j][0]) - m[0])**2
                et[1] += (int(mat[i][j][1]) - m[1])**2
                et[2] += (int(mat[i][j][2]) - m[2])**2
    nb_pixels = lx * ly
    if file_type == "pgm":
        return (et[0] / nb_pixels)**0.5
    elif file_type == "ppm":
        return (et[0] / nb_pixels)**0.5, (et[1] / nb_pixels)**0.5, (et[2] / nb_pixels)**0.5

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

def histogrammeCumule(nom):
    hc = [0]*256
    h = histogramme(nom)
    hc[0] = h[0]
    for i in range(1, 256):
        for j in range(0, i+1):
            hc[i] += h[j]
    return hc


chat_mat = lire('chat.pgm')
print(chat_mat)
ecrire("chat_new.pgm", chat_mat)
print(moy("chat.pgm"))
print(ecart_type("chat.pgm"))
print(histogramme("chat.pgm"))
print(histogrammeCumule("chat.pgm"))

