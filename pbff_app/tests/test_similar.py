
l1 = [1, 64, 19880, 4]
l2 = [64, 2, 3]
l3 = [890, 64, 1, 67, 4, 2]


def similar(l1, l2, l3):
    L1L2 = 0
    L1L3 = 0
    L2L3 = 0
    for i in range(len(l1)):
        if l1[i] in l2:
            L1L2 += 1
        if l1[i] in l3:
            L1L3 += 1
    for i in range(len(l2)):
        if l2[i] in l3:
            L2L3 += 1
    # print(L1L2, L1L3, L2L3)
    max1 = 0
    max2 = 0
    if L1L2 >= L1L3 >= L2L3:
        print("La liste l1 et la liste l2 sont les plus proches (", L1L2, "éléments en communs.)")
    elif L2L3 >= L1L2 >= L1L3:
        print("La liste l2 et la liste l3 sont les plus proches (", L2L3, "éléments en communs.)")
    elif L1L3 >= L2L3 >= L1L2:
        print("La liste l1 et la liste l3 sont les plus proches (", L1L3, "éléments en communs.)")


similar(l1, l2, l3)