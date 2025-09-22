Este programa lee expresiones aritmeticas desde un archivo de texto, tokeniza cada expresión, analiza sintacticamente la expresión con un analizador recursivo descendente y finalmente dibuja su arbol de sintaxis de forma jerarquica usando NetworkX y Graphviz.

# Tokenización (tokenizar):

Convierte una cadena de entrada en tokens (unidades reconocibles).

Tipos de tokens que reconoce:

- num → números (2, 3, 4)
- id → identificadores (x, y)
- opsuma → operadores de suma/resta (+, -)
- opmul → operadores de multiplicación/división (*, /)
- pari y pard → parentesis izquierdo y derecho.

# Clase Parser
- Implementa un analizador sintactico recursivo.
- Construye el arbol de sintaxis a partir de los tokens.
- Usa las reglas de una gramatica libre de contexto:

  # Métodos principales:

  - parseE → analiza expresiones con + y -.
  - parseT → analiza términos con * y /.
  - parseF → analiza factores (números, identificadores o expresiones entre paréntesis).
  - Cada vez que reconoce una regla, crea un nodo en el grafo (networkx.DiGraph).

# Visualización con Graphviz
En vez de spring_layout (que genera un grafo “desordenado”), se usa:

from networkx.drawing.nx_agraph import graphviz_layout
pos = graphviz_layout(parser.G, prog='dot')

- Esto organiza los nodos jerárquicamente (la raíz arriba, hojas abajo).
- nx.draw(...) dibuja el grafo con etiquetas y nodos en azul.

# Ejecución del programa

Se ejecuta con:
- python3 ArbolSintaxis.py gra.txt cadenas.txt
