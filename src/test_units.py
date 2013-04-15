# coding=utf-8
__author__ = 'Robin Keunen'

exp1 = "x = 3 + 42 * (s - t)"

exp2 = """
while 1 != 5:
    print(this)
    return "say hello"
t = 3
x = 3 + 42 * (s - t)
"""

dangling_else = """
if a == b:
    a = a + 1
    if a == 2:
        print(x)
    else:
        a = b + 6
        dothis(b+6)
else:
    return func(x, y)
"""

elifStmt = """
if not a != b:
    a = a + 1
    r -= 2 + 3
    return a
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
    while f(x) < y:
        x = x*2.
    if x == 1:
        lo = 0
    else:
        lo = x/2.
    return lo
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
# Déclaration des variables de départ
argent = 1000 # On a 1000 $ au début du jeu
continuer_partie = True # Booléen qui est vrai tant qu'on doit
                        # continuer la partie

print("Vous vous installez à la table de roulette avec", argent, "$.")

while continuer_partie: # Tant qu'on doit continuer la partie
    # on demande à l'utilisateur de saisir le nombre sur
    # lequel il va miser
    nombre_mise = -1
    while nombre_mise < 0 or nombre_mise > 49:
        nombre_mise = input("Tapez le nombre sur lequel vous voulez miser (entre 0 et 49) : ")
        # On convertit le nombre misé

        nombre_mise = int(nombre_mise)
        if nombre_mise < 0:
            print("Ce nombre est négatif")
        if nombre_mise > 49:
            print("Ce nombre est supérieur à 49")

    # À présent, on sélectionne la somme à miser sur le nombre
    mise = 0
    while mise <= 0 or mise > argent:
        mise = input("Tapez le montant de votre mise : ")
        # On convertit la mise
        mise = int(mise)
        if mise <= 0:
            print("La mise saisie est négative ou nulle.")
        if mise > argent:
            print("Vous ne pouvez miser autant, vous n'avez que", argent, "$")

    # Le nombre misé et la mise ont été sélectionnés par
    # l'utilisateur, on fait tourner la roulette
    numero_gagnant = randrange(50)
    print("La roulette tourne... ... et s'arrête sur le numéro", numero_gagnant)

    # On établit le gain du joueur
    if numero_gagnant == nombre_mise:
        print("Félicitations ! Vous obtenez", mise * 3, "$ !")
        argent += mise * 3
    elif numero_gagnant % 2 == nombre_mise % 2: # ils sont de la même couleur
        mise = ceil(mise * 0.5)
        print("Vous avez misé sur la bonne couleur. Vous obtenez", mise, "$")
        argent += mise
    else:
        print("Désolé l'ami, c'est pas pour cette fois. Vous perdez votre mise.")
        argent -= mise

    # On interrompt la partie si le joueur est ruiné
    if argent <= 0:
        print("Vous êtes ruiné ! C'est la fin de la partie.")
        continuer_partie = False
    else:
        # On affiche l'argent du joueur
        print("Vous avez à présent", argent, "$")
        quitter = input("Souhaitez-vous quitter le casino (o/n) ? ")
        if quitter == "o" or quitter == "O":
            print("Vous quittez le casino avec vos gains.")
            continuer_partie = False
"""

inputs = {"exp1":exp1,
          "exp2":exp2,
          "dangling_else":dangling_else,
          "elifStmt":elifStmt,
          "find_bounds":find_bounds,
          "slow_inverse":slow_inverse,
          "zero":zero,
          }

def lex_test(lexer, test_index = -1):
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


def parse_test(parser, test_index = -1):
    print("dummy")

