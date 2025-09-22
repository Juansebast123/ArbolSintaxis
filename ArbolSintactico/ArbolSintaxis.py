import sys
import networkx as nx
import matplotlib.pyplot as plt

#Para que el arbol se vea ordenado
from networkx.drawing.nx_agraph import graphviz_layout

#Tokeniza cada parte de la cadena para identificar que es
def tokenizar(cadena):
    tokens = []
    i = 0
    while i < len(cadena):
        c = cadena[i]
        if c.isspace():
            i += 1
            continue
        elif c.isdigit():
            num = c
            i += 1
            while i < len(cadena) and cadena[i].isdigit():
                num += cadena[i]
                i += 1
            tokens.append(("num", num))
        elif c.isalpha():
            ident = c
            i += 1
            while i < len(cadena) and cadena[i].isalnum():
                ident += cadena[i]
                i += 1
            tokens.append(("id", ident))
        elif c in "+-":
            tokens.append(("opsuma", c))
            i += 1
        elif c in "*/":
            tokens.append(("opmul", c))
            i += 1
        elif c == "(":
            tokens.append(("pari", c))
            i += 1
        elif c == ")":
            tokens.append(("pard", c))
            i += 1
        else:
            print(f"Token inválido: {c}")
            return None
    return tokens

#Analizador recursivo
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.G = nx.DiGraph()
        self.node_id = 0

    def nuevo_nodo(self, label):
        self.node_id += 1
        nodo = f"{label}_{self.node_id}"
        self.G.add_node(nodo, label=label)
        return nodo

    def ver_token(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def consumir(self, tipo):
        tok = self.ver_token()
        if tok and tok[0] == tipo:
            self.i += 1
            return tok
        return None

    def parseE(self):
        nodoE = self.nuevo_nodo("E")
        nodoT = self.parseT()
        if not nodoT:
            return None
        self.G.add_edge(nodoE, nodoT)

        while self.ver_token() and self.ver_token()[0] == "opsuma":
            op = self.consumir("opsuma")
            nodoOp = self.nuevo_nodo(op[1])
            self.G.add_edge(nodoE, nodoOp)
            nodoT2 = self.parseT()
            if not nodoT2:
                return None
            self.G.add_edge(nodoE, nodoT2)
        return nodoE

    def parseT(self):
        nodoT = self.nuevo_nodo("T")
        nodoF = self.parseF()
        if not nodoF:
            return None
        self.G.add_edge(nodoT, nodoF)

        while self.ver_token() and self.ver_token()[0] == "opmul":
            op = self.consumir("opmul")
            nodoOp = self.nuevo_nodo(op[1])
            self.G.add_edge(nodoT, nodoOp)
            nodoF2 = self.parseF()
            if not nodoF2:
                return None
            self.G.add_edge(nodoT, nodoF2)
        return nodoT

    def parseF(self):
        tok = self.ver_token()
        if not tok:
            return None
        nodoF = self.nuevo_nodo("F")
        if tok[0] == "id":
            self.consumir("id")
            nodoId = self.nuevo_nodo(tok[1])
            self.G.add_edge(nodoF, nodoId)
            return nodoF
        elif tok[0] == "num":
            self.consumir("num")
            nodoNum = self.nuevo_nodo(tok[1])
            self.G.add_edge(nodoF, nodoNum)
            return nodoF
        elif tok[0] == "pari":
            self.consumir("pari")
            nodoPari = self.nuevo_nodo("(")
            self.G.add_edge(nodoF, nodoPari)
            nodoE = self.parseE()
            if not nodoE:
                return None
            self.G.add_edge(nodoF, nodoE)
            if not self.consumir("pard"):
                return None
            nodoPard = self.nuevo_nodo(")")
            self.G.add_edge(nodoF, nodoPard)
            return nodoF
        else:
            return None

    def parse(self):
        raiz = self.parseE()
        if raiz and self.i == len(self.tokens):
            return raiz
        return None

#Abre 2 archivos, (primero debe ser gramatica y luego cadenas)
if __name__ == "__main__":
    archivo_cadenas = sys.argv[2]
    with open(archivo_cadenas) as f:
        cadenas = f.read().splitlines()

    for cadena in cadenas:
        tokens = tokenizar(cadena)
        if not tokens:
            print(f"{cadena} = NO acepta")
            continue
        parser = Parser(tokens)
        raiz = parser.parse()
        if raiz:
            print(f"{cadena} = acepta")

            pos = graphviz_layout(parser.G, prog='dot')

            labels = nx.get_node_attributes(parser.G, "label")
            nx.draw(parser.G, pos,
                    labels=labels,
                    with_labels=True,
                    node_size=1500,
                    node_color="lightblue",
                    arrows=True)
            plt.show()
        else:
            print(f"{cadena} = NO acepta")
