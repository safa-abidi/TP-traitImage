def lire(nom):
    file = open(nom, 'r')
    file_type = str(file.readline()).strip()
    file.readline()
    file_size = file.readline()
    file_size = file_size.split(' ')
    ly = int(file_size[1])
    lx = int(file_size[0])
    file.readline()

    mat = [[0] * lx] * ly

    for y in range(0, ly):
        x3 = 0
        line = file.readline()
        pixels = line.split(' ')
        if file_type == "P2":
            for x in range(0, lx):
                mat[y][x] = pixels[x]
        else:
            for x in range(0, lx):
                mat[y][x] = [pixels[x3], pixels[x3 + 1], pixels[x3 + 2]]
                x3 += 3
    file.close()
    return mat


def ecrire(nom, mat):
    file = open(nom, 'w')
    file_type = nom.split(".")[1]

    lx = len(mat[0])
    ly = len(mat)

    if file_type == "pgm":
        file.write("P2\n")
    else:
        file.write("P3\n")
    file.write("# " + nom + "\n")
    file.write(str(lx) + " " + str(ly) + "\n")
    file.write("255" + "\n")

    for y in range(0, ly):
        line = ""
        for x in range(0, lx):
            line += mat[y][x] + " "
        file.write(line[:len(line) - 1] + "\n")
    file.close()


# def moy(nom):
#    mat = lire(nom)
#    s = 0
#    for i in range(0,len(mat)):

print(lire("chat.pgm"))
# print(chat_mat)
# ecrire("chat_new.pgm", chat_mat)
