
# from http://www.fundza.com/c4serious/noise/perlin/index.html

import math


def lerp(t, a, b):
    """lerp

    :param t:
    :param a:
    :param b:
    :return:
    """
    return a + t * (b - a)


def fade(t):
    """fade

    :param t:
    :return:
    """
    return t * t * t * (t * (t * 6 - 15) + 10)


def grad(hash, x, y, z):
    """grad

    :param hash:
    :param x:
    :param y:
    :param z:
    :return:
    """
    h = hash & 15
    if h < 8:
        u = x
    else:
        u = y
    if h < 4:
        v = y
    elif h in [12, 14]:
        v = x
    else:
        v = z
    if h & 1 != 0:
        u = -u
    if h & 2 != 0:
        v = -v
    return u + v


def pnoise(x, y, z):
    """perlin noise

    :param x:
    :param y:
    :param z:
    :return:
    """
    p = (151, 160, 137,  91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7,
         225, 140, 36, 103,  30,  69, 142, 8, 99, 37, 240, 21, 10, 23, 190,
         6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117,
         35, 11, 32, 57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136,
         171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158,
         231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46,
         245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76,
         132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86,
         164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5,
         202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16,
         58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152, 2, 44,
         154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9, 129, 22, 39, 253,
         19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97,
         228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51,
         145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
         184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205,
         93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61,
         156, 180, 151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194,
         233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23,
         190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203,
         117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136,
         171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158,
         231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46,
         245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76,
         132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86,
         164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5,
         202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16,
         58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119, 248, 152, 2, 44,
         154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9, 129, 22, 39, 253,
         19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97,
         228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51,
         145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
         184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205,
         93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61,
         156, 180)

    X = int(math.floor(x)) & 255
    Y = int(math.floor(y)) & 255
    Z = int(math.floor(z)) & 255
    x -= math.floor(x)
    y -= math.floor(y)
    z -= math.floor(z)

    u = fade(x)
    v = fade(y)
    w = fade(z)

    A = p[X] + Y
    AA = p[A] + Z
    AB = p[A + 1] + Z
    B = p[X + 1] + Y
    BA = p[B] + Z
    BB = p[B + 1] + Z

    perlin_aa = p[AA]
    perlin_ab = p[AB]
    perlin_ba = p[BA]
    perlin_bb = p[BB]
    perlin_aa1 = p[AA + 1]
    perlin_ba1 = p[BA + 1]
    perlin_ab1 = p[AB + 1]
    perlin_bb1 = p[BB + 1]

    grad_aa = grad(perlin_aa, x, y, z)
    grad_ba = grad(perlin_ba, x - 1, y, z)
    grad_ab = grad(perlin_ab, x, y - 1, z)
    grad_bb = grad(perlin_bb, x - 1, y - 1, z)
    grad_aa1 = grad(perlin_aa1, x, y, z - 1)
    grad_ba1 = grad(perlin_ba1, x - 1, y, z - 1)
    grad_ab1 = grad(perlin_ab1, x, y - 1, z - 1)
    grad_bb1 = grad(perlin_bb1, x - 1, y - 1, z - 1)
    return lerp(w, lerp(v, lerp(u, grad_aa, grad_ba),
                        lerp(u, grad_ab, grad_bb)),
                lerp(v, lerp(u, grad_aa1, grad_ba1),
                     lerp(u, grad_ab1, grad_bb1)))
