# coding=utf-8
__author__ = 'Robin Keunen'

exp1 = "x = 3 + 42 * (2 - 8)"

exp2 = """
t = 3
s = 3
x = 3 + 42 * (s - t)
"""

dangling_else = """
a = 2
b = a
if a == b:
    a = a + 1
    if a == 2:
        print(a)
    else:
        a = b + 6
        print(b)
else:
    return print("diff")
"""

printtest = """
print("Coucou !")
unNombre = 50
if unNombre < "50" :
    print("Votre nombre est plus petit que 50.")
elif unNombre == "50" :
    print("Votre nombre est exactement 50")
else :
    print("Votre nombre est plus grand que 50.")

    """

elifStmt = """
a = 2
b = 2

defun dummy(a, b):
    if not a != b:

        return a + b
    elif a > 2:
        if robin >= genie and not pierre < genie:
            return yay
        elif il or try(ceci):
            print("this message")
        lo += b/2.
    elif not a <= 3:
        return b
    else:
        return end
"""

find_bounds = """
defun find_bounds (f, y):
    x = 1.
    while f(x) < y: x = x*2.
    if x == 1:
        lo = 0
    else:
        lo = x/2.
    return lo
"""

function_def = """
defun f2(s1, s2) :
    print(s1)
    print(s2)

f2("HAHAHA !", 34)
"""

addfun = """
defun add(a, b):
   r = a + b
   return r

print(add(1, 2)
"""

slow_inverse = """
defun slow_inverse(f, delta):
    defun f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        if (f(x)-y < y-f(x-delta)):
            return x
        else:
            return x-delta
    return f_1
    """

zero = """
# Declaration des variables de depart
argent = 1000 # On a 1000 $ au debut du jeu
continuer_partie = True # Booleen qui est vrai tant qu'on doit
                        # continuer la partie

print("Vous vous installez a la table de roulette avec")
print(argent)
print("$.")

while continuer_partie: # Tant qu'on doit continuer la partie
    # on demande a l'utilisateur de saisir le nombre sur
    # lequel il va miser
    nombre_mise = -1
    while nombre_mise < 0 or nombre_mise > 49:
        nombre_mise = input("Tapez le nombre sur lequel vous voulez miser (entre 0 et 49) : ")
        # On convertit le nombre mise

        nombre_mise = int(nombre_mise)
        if nombre_mise < 0:
            print("Ce nombre est negatif")
        if nombre_mise > 49:
            print("Ce nombre est superieur a 49")

    # À present, on selectionne la somme a miser sur le nombre
    mise = 0
    while mise <= 0 or mise > argent:
        mise = input("Tapez le montant de votre mise : ")
        # On convertit la mise
        mise = int(mise)
        if mise <= 0:
            print("La mise saisie est negative ou nulle.")
        if mise > argent:
            print("Vous ne pouvez miser autant.")

    # Le nombre mise et la mise ont ete selectionnes par
    # l'utilisateur, on fait tourner la roulette
    numero_gagnant = randrange(50)
    print("La roulette tourne... ... et s'arrete sur le numero")
    print(numero_gagnant)

    # On etablit le gain du joueur
    if numero_gagnant == nombre_mise:
        print("Felicitations ! Vous obtenez", mise * 3, "$ !")
        argent += mise * 3
    elif numero_gagnant % 2 == nombre_mise % 2: # ils sont de la meme couleur
        mise = ceil(mise * 0.5)
        print("Vous avez mise sur la bonne couleur. Vous obtenez", mise, "$")
        argent += mise
    else:
        print("Desole l'ami, c'est pas pour cette fois. Vous perdez votre mise.")
        argent -= mise

    # On interrompt la partie si le joueur est ruine
    if argent <= 0:
        print("Vous etes ruine ! C'est la fin de la partie.")
        continuer_partie = False
    else:
        # On affiche l'argent du joueur
        print("Vous avez a present", argent, "$")
        quitter = input("Souhaitez-vous quitter le casino (o/n) ? ")
        if quitter == "o" or quitter == "O":
            print("Vous quittez le casino avec vos gains.")
            continuer_partie = False
"""

chain_add = addfun + """
defun sum_list(l):
    if tail(l) == []:
        return head(l)
    else:
        return head(l) + sum_list(tail(l))

ll = [1, 2, 3, 4]
print(sum_list(ll))
"""

alt_map = """
defun alt_map(f, l):
    if tail(l) == []:
        return list(f(head(l)))
    else:
        return cons(f(head(l)), alt_map(f, tail(l)))
"""

fact = """
def fact(n) :
    if n == 1 or n == 0 :
        return 1
    else :
        return n * fact(n - 1)

print fact(6)
"""

n_ary = """

defun len(l):


defun n_ary(f):
    #Given binary function f(x, y), return an n_ary function such
    #that f([x, y, z]) = f(x, f([y, z])), etc. Also allow f(x) = x.

    defun n_ary_f(argsl):
        if len(argsl) == 2:
            return f(head(argsl), head(tail(argsl)))
        else:
            return f(head(argsl), n_ary_f(tail(argsl)))
    return n_ary_f

def add(a, b):
    return a + b

add_n = n_ary(add)

print add_n([1, 2, 3, 4, 5])
"""

inputs = {"exp1": exp1,
          "exp2": exp2,
          "dangling_else": dangling_else,
          "elifStmt": elifStmt,
          "find_bounds": find_bounds,
          "slow_inverse": slow_inverse,
          "zero": zero,
          "printtest": printtest,
          "fundef": function_def,
          "addfun": addfun,
          "chain_add": chain_add,
          "alt_map": alt_map,
          "fact": fact,
          "n_ary": n_ary,
          }


def lex_test(lexer, test_index=-1):
    """

    :param lexer:
    :param test_index:
    """
    extended_print = ('ID', 'INT', 'FLOAT', 'STRING', 'WS')

    if test_index == -1:
        for data in inputs:
            lexer.input(data)
            lexer.lineno = 1
            print(data)
            for tok in lexer:
                if tok.type == 'NEWLINE':
                    print(tok.type)
                elif tok.type == 'WS':
                    print('(' + tok.type + ', ' + str(tok.value) + ')', end=' ')
                elif tok.type in extended_print:
                    print('(' + tok.type + ', ' + str(tok.value) + ')', end=' ')
                else:
                    print(tok.type, end=' ')
            print("\n")
    else:
        data = inputs[test_index]
        lexer.input(data)
        lexer.lineno = 1
        print('"', data, '"')

        for tok in lexer:
            if tok.type == 'NEWLINE':
                print(tok.type)
            elif tok.type in extended_print:
                print('(' + tok.type + ', ' + str(tok.value) + ')', end=' ')
            else:
                print(tok.type, end=' ')
        print('\n')


