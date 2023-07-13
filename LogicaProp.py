# Implementación de la Lógica Proposicional en Python.

# Uso del paradigma de Programación Orientada a Objetos.

# Autor: Óscar Mirás Sánchez.

# MEMORIA DEL DESARROLLO DEL PROGRAMA

# 1) DESCRIPCIÓN DEL CÓDIGO

# El código implementa la Lógica Proposicional básica en Python. Una proposicion elemental (atómica) puede tener sólo uno de los 2 valores
# lógicos (True o False). Las proposiciones elementales se pueden combinar para dar lugar a otras proposiciones más complejas mediante
# operaciones lógicas: Negacion, Interseccion, Union, Condicional, Bicondicional y XOR.

# Las proposiciones elementales se implementan con la clase "Atómica", que con el método "evaluar" accede a sus valores de verdad.
# Para implementar las operaciones lógicas, se construye inicialmente la clase padre "FormulaCompuesta", que servirá como "almacén" 
# de las proposiciones o fórmulas de las clases operacionales hijas y permitirá obtener sus valores de verdad concatenando el método 
# get_formula con "evaluar" de la clase padre.

# Las clases hijas que representan operaciones lógicas simples (Interseccion, Union y Negacion) heredan los métodos de la clase padre 
# y los emplean para llevar a cabo sus propias evaluaciones mediante los conectores lógicos básicos (and, or y not). 

# Las restantes operaciones lógicas (Condicional, Bicondicional y XOR) son variaciones de las 3 clases previas, de modo que 
# en sus propios métodos de evaluación trabajaremos con objetos de tipo Negacion, Interseccion y Union, lo que mejora
# la eficiencia del código.

# Por otra parte, se construye un menú de usuario que permite elaborar el diccionario con los valores de verdad de las 
# proposiciones atómicas. La opción 3 calcula el valor de verdad de una expresión dada por el usuaro (para ésto es imprescindible 
# haber inicializado las proposiciones atómicas con sus valores de verdad en la opción 1 del menú). Además, si el usuario 
# desea visualizar la tabla de verdad completa de una expresión cualquiera, no tendrá que asignar a cada atómica un valor de verdad, 
# sino que la propia opción 4 generará todas las posibilidades.

# 2) EVOLUCIÓN DEL PROGRAMA

# Tras la escritura de una versión preliminar del código, se probaron sugerencias en ChatGPT, algunas de las cuáles se añadieron
# al programa posteriormente. Entre ellas se encuentran: 

# 1) El método de f-strings en Python, es decir, la devolución de __str__ en las sucesivas clases operación.
# 2) Ayuda en la implementación de la tabla de verdad, en líneas de código como print(("{:<7}" * (n+1)).format(*(...)) que dejan
#    los suficientes espacios para las columnas de la tabla de verdad (7 espacios a la izquierda en el ejemplo).
# 3) La implementación de la función zfill(n) en la opción 4 del menú, útil en este cógdigo para ajustar las cifras de un número 
#    binario a una longitud n dada.

# Además, se implementaron algunas funciones para agilizar el código, referentes a comprobaciones como intlibre(cadena) o letra_valida
# para controlar que el usuario emplee una única letra (minúscula o mayúscula) como proposición atómica, así como una 
# función espera() que facilita el manejo del menú.

# También, fue creada la función reducir_expresion con la intención de cambiar la expresión introducida por teclado
# (una cadena de texto) para poder ser ejecutada correctamente con la orden eval (es decir, introduciendo el prefijo Atomica()
# cuando sea necesario). 

# Finalmente, fue añadida la opción 5 para presentar al usuario la sintaxis del programa con algún ejemplo ilustrativo.



'''
Programación orientada a objetos. Definición de la clase Atómica, clase padre FormulaCompuesta y las clases hija (operaciones lógicas).

'''

class Atomica:
    '''Clase base. Sobre ésta, se construyen las sucesivas fórmulas de mayor complejidad'''
    def __init__(self, nombre):
        self.__nombre = nombre
    
    def evaluar(self, valores): #El atributo valores se correspondería al diccionario en el cual están guardados los valores de verdad.
        return valores[self.__nombre] #Se accede al posible valor de verdad de la Atómica (True o False).
    
    def __str__(self):
        return self.__nombre

class FormulaCompuesta:
    '''Clase padre de las clases referentes a operaciones lógicas. Almacena las fórmulas en una lista y las recupera con get_formula'''
    def __init__(self, *formula):
        self.__formula = list(formula) #Almacenamos las distintas fórmulas en una lista. El __init__ de ésta clase servirá como padre para otras.
    
    def get_formula(self, índice): #Método de obtención de los valores de verdad almacenados en la lista self.__formula.
        return self.__formula[índice]

class Interseccion(FormulaCompuesta): #Cada clase hija emplea de FormulaCompuesta el almacenamiento de los atributos y su obtención mediante get_formula.
    '''Operación lógica simple de Intersección o Conjunción de una pareja de valores de verdad'''
    def __init__(self, formula1, formula2):
        super().__init__(formula1, formula2)

    def evaluar(self, valores):
        return super().get_formula(0).evaluar(valores) and super().get_formula(1).evaluar(valores)

    def __str__(self):
        return f"({super().get_formula(0)} ^ {super().get_formula(1)})"

class Union(FormulaCompuesta):
    '''Operación lógica simple de Unión o Disyunción de una pareja de valores de verdad'''
    def __init__(self, formula1, formula2):
        super().__init__(formula1, formula2)
    
    def evaluar(self, valores):
        return super().get_formula(0).evaluar(valores) or super().get_formula(1).evaluar(valores)

    def __str__(self):
        return f"({super().get_formula(0)} v {super().get_formula(1)})"

class Negacion(FormulaCompuesta):
    '''Operación lógica simple de Negación de una única fórmula o valor de verdad'''
    def __init__(self, formula):
        super().__init__(formula)

    def evaluar(self, valores):
        return not super().get_formula(0).evaluar(valores)

    def __str__(self):
        return f"~{super().get_formula(0)}"

class Condicional(FormulaCompuesta):
    '''Operación lógica compuesta de Condicional, construída sobre la Unión y la Negación'''
    def __init__(self, formula1, formula2):
        super().__init__(formula1, formula2)

    def evaluar(self, valores): #Aplicamos la definición lógica de Condicional. Por ejemplo: A --> B => ~A v B
        return Union(Negacion(super().get_formula(0)), super().get_formula(1)).evaluar(valores)

    def __str__(self):
        return f"({super().get_formula(0)} --> {super().get_formula(1)})"

class Bicondicional(FormulaCompuesta):
    '''Operación lógica compuesta de Bicondicional, construída sobre la Intersección de Condicionales'''
    def __init__(self, formula1, formula2):
        super().__init__(formula1, formula2)

    def evaluar(self, valores): #Aplicamos la definición lógica de Bicondicional como Intersección de condicionales.
        return Interseccion(Condicional(super().get_formula(0), super().get_formula(1)), Condicional(super().get_formula(1), super().get_formula(0))).evaluar(valores)

    def __str__(self):
        return f"({super().get_formula(0)} <--> {super().get_formula(1)})"

class XOR(FormulaCompuesta): 
    '''Operación lógica compuesta de XOR'''

    #Construímos el XOR como la Negación del Bicondicional. No es la definición lógica propiamente dicha, pero nos permite reutilizar 
    #de forma eficiente la recién creada clase Bicondicional.

    def __init__(self, formula1, formula2):
        super().__init__(formula1, formula2)

    def evaluar(self, valores):
        return Negacion(Bicondicional(super().get_formula(0), super().get_formula(1))).evaluar(valores)

    def __str__(self):
        return f"({super().get_formula(0)} xor {super().get_formula(1)})"
        

'''
Funciones de comprobación y espera para el menú.

'''

def intlibre(cadena):
    '''Función de comprobación (números enteros)'''
    flag = False
    while flag == False:
        try:
            a = int(input(cadena))
            flag = True
        except ValueError:
            print('\nNo has introducido un número válido. Inténtalo de nuevo.')
    return a

def letra_valida(cadena):
    '''Función de comprobación (letras mayúsculas o minúsculas)'''
    flag = False
    while flag == False:
        a = input(cadena)
        if len(a) == 1:
            if ((65 <= ord(a) <= 90) or (97 <= ord(a) <= 122)): #Control de que la cadena proporcionada sea una única letra del alfabeto.
                flag = True
            else:
                print("\nSu caracter no se encuentra en el rango de letras aceptado. Vuelva a intentarlo.")
        else:
            print("\nHa adjuntado más de un único caracter. Escriba una única letra.")
    return a

def espera():
    '''Función que solicita "input" hasta que el usuario pulsa la tecla <ENTER>'''
    a = 0
    while a != '':
        a = input('Pulse <ENTER> para continuar: ')  


def reducir_expresion(diccionario, expresion):
    '''Función que devuelve la expresion_final preparada para ser ejecutada con la orden eval'''
    expresion_final = expresion[:]
    for i in diccionario.keys():
        if (expresion == i):
            expresion_final = 'Atomica("' + i + '")'
        elif ("(" + str(i) + ")" in expresion) or ("," + str(i) in expresion) or (str(i) + "," in expresion): #Posibilidades de que la clave se encuentre en el input de usuario.
            expresion_final = expresion_final.replace("(" + i + ",", "(" + 'Atomica("' + i + '")' + ",")
            expresion_final = expresion_final.replace("," + i + ")", "," + 'Atomica("' + i + '")' + ")")
            expresion_final = expresion_final.replace("(" + i + ")", "(" + 'Atomica("' + i + '")' + ")")
    return expresion_final


'''
Estructura de menú.

'''

d = {} #Diccionario de almacenamiento de valores de verdad.
instrucciones_reservadas = ["Negacion", "Union", "Interseccion", "Condicional", "Bicondicional", "XOR", ")", "(", ","]
#Se reservan para posteriormente en la opción 4 (construcción de las tablas de verdad) obtener las expresiones atómicas 
#eliminando de la cadena proporcionada por el usuario los elementos de la lista instrucciones_reservadas.

def menu():

    print('\n0: Salir del menú                               1: Añadir valores de verdad.')
    print('2: Comprobar valores de verdad.                 3: Evaluar fórmula.')
    print('4: Tabla de verdad de una expresión.            5: Ayuda y ejemplos.')

    opcion = intlibre('\nDime la opcion que deseas: ')
    while opcion not in range(0,6):
        print('Esa no es una opción válida')
        opcion = intlibre('\nDime la opcion que deseas: ')

    if opcion == 1:
        letra = letra_valida("\nLetra: ")
        valor_verdad = bool(int(input("Valor de verdad (0 = False, 1 = True): ")))
        d[letra] = valor_verdad
        espera()
        menu()

    elif opcion == 2:
        print("\nValores de verdad guardados: " + str(d))
        espera()
        menu()

    elif opcion == 3: #Para aplicar ésta opción, es necesario haber inicializado las atómicas previamente en la opción 1.
        expresion = input("\nProporcione una fórmula: ")
        expresion = expresion.replace(" ", "") #Eliminamos los espacios de la cadena proporcionada por el usuario.
        expresion_final = reducir_expresion(d, expresion)
        expresion_final = eval(expresion_final) #Evaluamos la expresión.
        print(f"\nLa formula {expresion_final} es {expresion_final.evaluar(d)} con {d}")
        espera()
        menu()
    
    elif opcion == 4: #Para aplicar ésta opción, no hace falta haber inicializado las atómicas previamente, pues se generan todas las posibilidades.
        d_completo = {} #Diccionario empleado para las tablas de verdad.
        expresion = input("\nProporcione una fórmula: ")
        expresion = expresion.replace(" ", "") #Eliminamos los espacios en la fórmula original proporcionada por el usuario.
        atomicas_base = expresion[:]
        for i in instrucciones_reservadas:
            if i in atomicas_base:
                atomicas_base = atomicas_base.replace(i, "") #Eliminamos los caracteres que se encuentran en instrucciones_reservadas.

        atomicas_base = "".join(set(atomicas_base)) #Eliminamos las repeticiones de caracteres con la orden conjunto (set).
        n = len(atomicas_base) #Número de variables que han sido localizadas en la fórmula proporcionada por el usuario.

        for a in range(2**n): #Iteramos sobre el número total de combinaciones de valores de verdad (2^n).
            binario = bin(a)[2:]
            binario = binario.zfill(n) #Colocamos 0s para que todos los binarios cuenten con el mismo tamaño.
            for i in range(n):
                d_completo[atomicas_base[i]] = bool(int(binario[i])) #Añadimos el valor de verdad booleano al diccionario.

            expresion_final = reducir_expresion(d_completo, expresion)
            expresion_final = eval(expresion_final) #Evaluamos la expresión.

            if a == 0: #Creación de la tabla de verdad propiamente dicha.
                print("\n")
                print("'''''''" * (n+1))
                print(("{:<7}" * (n+1)).format(*(list(i for i in atomicas_base)), str(expresion_final)) + "\n")
            print(("{:<7}" * (n+1)).format(*(list(str(d_completo[i]) for i in d_completo.keys())), str(expresion_final.evaluar(d_completo))))
        print("\n" + "'''''''" * (n+1))

        espera()    
        menu()
    
    elif opcion == 5: #Opción de ayuda del menú.
        d_prueba = {"p": True, "q": False, "r": True}
        p = Atomica("p")
        q = Atomica("q")
        r = Atomica("r")
        prueba = Interseccion(Union(p,Negacion(q)), XOR(q,r))
        print("\n-Operaciones disponibles: Union, Interseccion, Negacion, Condicional, Bicondicional, XOR")
        print("-Las expresiones operacionales funcionan con pares de atómicas (salvo Negacion) y se pueden anidar. Ejemplo: Condicional(p,Negacion(q))")
        print("\nEjemplo de uso:")
        espera()
        print("\n[Input]: " + "Interseccion(Union(p,Negacion(q)), XOR(q,r))")
        print("\n[Output]: ")
        print(f"La expresión {prueba} es {prueba.evaluar(d_prueba)} con {d_prueba}")
        menu()

menu()