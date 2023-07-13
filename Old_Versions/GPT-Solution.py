# Código proporcionado por ChatGPT.

# Chat GPT introduce la idea de aplicar una clase FormulaCompuesta() que sirva como clase padre del resto
# de clases operacionales. No obstante, el código es incorrecto, ya que introduce el método get_formula con parámetro "índice" y luego
# intenta emplear programación funcional en las clases Interseccion y Union (sin éxito) ya que no itera sobre los diferentes índices 
# que se requieren en get_formula.

# Se tomará la idea de la clase FormulaCompuesta y se reformulará toda ésta programación en el programa final, además de añadir un
# menú de usuario.


class Formula():
    '''Clase que representa una fórmula lógica.'''
    def __init__(self, nombre):
        self.__nombre = nombre
    
    def evaluar(self, valores):
        return valores[self.__nombre]
    
    def __str__(self):
        return self.__nombre

class FormulaCompuesta():
    '''Clase padre de las clases referentes a operaciones lógicas. Almacena las fórmulas en una lista y las recupera con get_formula'''
    def __init__(self, *formula):
        self.__formula = list(formula)
    
    def get_formula(self, indice):
        return self.__formula[indice]

class Interseccion(FormulaCompuesta):
    '''Clase que representa la operación lógica de intersección (^).'''
    def evaluar(self, valores):
        resultado = True
        for formula in self.get_formula():
            resultado = resultado and formula.evaluar(valores)
        return resultado
    
    def __str__(self):
        return "(" + " ^ ".join(str(formula) for formula in self.get_formula()) + ")"

class Union(FormulaCompuesta):
    '''Clase que representa la operación lógica de unión (v).'''
    def evaluar(self, valores):
        resultado = False
        for formula in self.get_formula():
            resultado = resultado or formula.evaluar(valores)
        return resultado
    
    def __str__(self):
        return "(" + " v ".join(str(formula) for formula in self.get_formula()) + ")"

class Negacion(FormulaCompuesta):
    '''Clase que representa la operación lógica de negación (~).'''
    def evaluar(self, valores):
        return not self.get_formula(0).evaluar(valores)
    
    def __str__(self):
        return "(~" + str(self.get_formula(0)) + ")"

class Condicional(FormulaCompuesta):
    '''Clase que representa la operación lógica de condicional (-->).'''
    def evaluar(self, valores):
        return Union(Negacion(self.get_formula(0)), self.get_formula(1)).evaluar(valores)
    
    def __str__(self):
        return "(" + str(self.get_formula(0)) + " --> " + str(self.get_formula(1)) + ")"

class Bicondicional(FormulaCompuesta):
    '''Clase que representa la operación lógica de bicondicional (<-->).'''
    def evaluar(self, valores):
        return Interseccion(Condicional(self.get_formula(0), self.get_formula(1)), Condicional(self.get_formula(1), self.get_formula(0))).evaluar(valores)
    
    def __str__(self):
        return "(" + str(self.get_formula(0)) + " <--> " + str(self.get_formula(1)) + ")"

class XOR(FormulaCompuesta):
    '''Clase que representa la operación lógica de XOR (xor).'''
    def evaluar(self, valores):
        return Negacion(Bicondicional(self.get_formula(0), self.get_formula(1))).evaluar(valores)
    
    def __str__(self):
        return "(" + str(self.get_formula(0)) + " xor " + str(self.get_formula(1)) + ")"


valores1 = {"p": True, "q": False, "r": False}

p = Formula("p")
q = Formula("q")
r = Formula("r")

formula_final1 = Interseccion(Bicondicional(r, q), Negacion(r))
formula_final2 = XOR(p, q)

print("La expresión " + str(formula_final1) + " es " + str(formula_final1.evaluar(valores1)) + " con " + str(valores1))
print("La expresión " + str(formula_final2) + " es " + str(formula_final2.evaluar(valores1)) + " con " + str(valores1))
