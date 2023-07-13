# Código Preliminar (antes de las sugerencias de Chat GPT)

# Implementación de la Lógica Proposicional en Python

# A diferencia del código final, éste no cuenta con una clase padre de la que el resto de clases (Interseccion, Union, etc) hereden
# métodos. Tampoco cuenta con un menú para el usuario, ni recursos como return f.


class Atomica():
    def __init__(self, nombre):
        self.__nombre = nombre
    def evaluar(self, valores):
        return valores[self.__nombre]
    def __str__(self):
        return self.__nombre

class Interseccion():
    def __init__(self, atomica1, atomica2):
        self.__atomica1 = atomica1
        self.__atomica2 = atomica2
    def evaluar(self, valores):
        return self.__atomica1.evaluar(valores) and self.__atomica2.evaluar(valores)
    def __str__(self):
        return "(" + str(self.__atomica1) +  " ^ " +  str(self.__atomica2) + ")"

class Union():
    def __init__(self, atomica1, atomica2):
        self.__atomica1 = atomica1
        self.__atomica2 = atomica2
    def evaluar(self, valores):
        return self.__atomica1.evaluar(valores) or self.__atomica2.evaluar(valores)
    def __str__(self):
        return "(" + str(self.__atomica1) +  " v " +  str(self.__atomica2) + ")"

class Negacion():
    def __init__(self, atomica1):
        self.__atomica1 = atomica1
    def evaluar(self, valores):
        return not self.__atomica1.evaluar(valores)
    def __str__(self):
        return "(" + "~" + str(self.__atomica1) + ")"

class Condicional():
    def __init__(self, atomica1, atomica2):
        self.__atomica1 = atomica1 
        self.__atomica2 = atomica2
    def evaluar(self, valores):
        return Union(Negacion(self.__atomica1), self.__atomica2).evaluar(valores) 
    def __str__(self):
        return "(" + str(self.__atomica1) +  " --> " +  str(self.__atomica2) + ")"
       
class Bicondicional():
    def __init__(self, atomica1, atomica2):
        self.__atomica1 = atomica1 
        self.__atomica2 = atomica2
    def evaluar(self, valores):
        return Interseccion(Condicional(self.__atomica1, self.__atomica2), Condicional(self.__atomica2, self.__atomica1)).evaluar(valores) 
    def __str__(self):
        return "(" + str(self.__atomica1) +  " <--> " +  str(self.__atomica2) + ")"
        
class XOR():
    def __init__(self, atomica1, atomica2):
        self.__atomica1 = atomica1 
        self.__atomica2 = atomica2
    def evaluar(self, valores):
        return Negacion(Bicondicional(self.__atomica1, self.__atomica2)).evaluar(valores) 
    def __str__(self):
        return "(" + str(self.__atomica1) +  " xor " +  str(self.__atomica2) + ")"


valores1 = {"p": True, "q": False, "r": False}

p = Atomica("p")
q = Atomica("q")
r = Atomica("r")

formula_final1 = Interseccion(Bicondicional(r, q), Negacion(r))
formula_final2 = XOR(p, q)

print("La expresión " + str(formula_final1) + " es " + str(formula_final1.evaluar(valores1)) + " con " + str(valores1))
print("La expresión " + str(formula_final2) + " es " + str(formula_final2.evaluar(valores1)) + " con " + str(valores1))

