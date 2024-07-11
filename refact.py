import heapq

class Mapa:
    def __init__(self, ancho, alto):
        self.cantidad_listas = ancho
        self.cantidad_sublistas = alto
        self.lista = [["." for _ in range(alto)] for _ in range(ancho)]

    def solicitar_puntos(self, ax, ay, bx, by):
        self.entrada_x = ax
        self.entrada_y = ay
        self.salida_x = bx
        self.salida_y = by

    def marcar_coordenadas(self, position1, position2):
        self.lista[self.entrada_x][self.entrada_y] = position1
        self.lista[self.salida_x][self.salida_y] = position2

    def agregar_obstaculos(self, num_edificios):
        for _ in range(num_edificios):
            while True:
                x, y = map(int, input(f"Ingrese las coordenadas del edificio (0 a {self.cantidad_listas - 1}, 0 a {self.cantidad_sublistas - 1}) separadas por espacio: ").split())
                if self.lista[x][y] == ".":
                    self.lista[x][y] = "E"
                    break
                else:
                    print("Celda ocupada. Intente en otra celda.")

    def quitar_obstaculos(self, x, y):
        if self.lista[x][y] == "E":
            self.lista[x][y] = "."

    def es_accesible(self, x, y):
        return self.lista[x][y] == "."

    def imprimir_mapa(self):
        for sublista in self.lista:
            print(' '.join(sublista))


class CalculadoraDeRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def calcular_ruta(self, inicio, fin):
        vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        lista_abierta = []
        heapq.heappush(lista_abierta, (0 + self.heuristica(inicio, fin), 0, inicio))
        de_donde_vino = {}
        g_score = {inicio: 0}
        f_score = {inicio: self.heuristica(inicio, fin)}

        while lista_abierta:
            actual = heapq.heappop(lista_abierta)[2]

            if actual == fin:
                camino = []
                while actual in de_donde_vino:
                    camino.append(actual)
                    actual = de_donde_vino[actual]
                camino.append(inicio)
                camino.reverse()
                return camino

            for vecino in vecinos:
                vecino_pos = (actual[0] + vecino[0], actual[1] + vecino[1])
                if 0 <= vecino_pos[0] < len(self.mapa.lista) and 0 <= vecino_pos[1] < len(self.mapa.lista[0]):
                    if self.mapa.lista[vecino_pos[0]][vecino_pos[1]] == "E":
                        continue
                    puntaje_tentativo_g = g_score[actual] + 1

                    if vecino_pos not in g_score or puntaje_tentativo_g < g_score[vecino_pos]:
                        de_donde_vino[vecino_pos] = actual
                        g_score[vecino_pos] = puntaje_tentativo_g
                        f_score[vecino_pos] = puntaje_tentativo_g + self.heuristica(vecino_pos, fin)
                        heapq.heappush(lista_abierta, (f_score[vecino_pos], puntaje_tentativo_g, vecino_pos))

        return None


# Inicializar el mapa
cantidad_listas = int(input("Ingrese la cantidad de listas: "))
cantidad_sublistas = int(input("Ingrese la cantidad de elementos en cada sublista: "))
mapa = Mapa(cantidad_listas, cantidad_sublistas)

# Solicitar y marcar puntos
entrada_x, entrada_y = map(int, input(f"Ingrese las coordenadas del primer punto (0 a {cantidad_listas - 1}, 0 a {cantidad_sublistas - 1}) separadas por espacio: ").split())
salida_x, salida_y = map(int, input(f"Ingrese las coordenadas del segundo punto (0 a {cantidad_listas - 1}, 0 a {cantidad_sublistas - 1}) separadas por espacio: ").split())
mapa.solicitar_puntos(entrada_x, entrada_y, salida_x, salida_y)
mapa.marcar_coordenadas("0", "0")

# Ingresar obstáculos
num_edificios = int(input("Ingrese la cantidad de edificios: "))
mapa.agregar_obstaculos(num_edificios)

# Inicializar la calculadora de rutas y calcular la ruta
calculadora = CalculadoraDeRutas(mapa)
inicio = (entrada_x, entrada_y)
fin = (salida_x, salida_y)
camino = calculadora.calcular_ruta(inicio, fin)

# Marcar el camino en el mapa
if camino:
    for paso in camino:
        if mapa.lista[paso[0]][paso[1]] == ".":
            mapa.lista[paso[0]][paso[1]] = "*"
else:
    print("No se encontró un camino")

# Imprimir el mapa actualizado con la ruta encontrada
print("\nMapa con la ruta encontrada:")
mapa.imprimir_mapa()

# Funcionalidad para quitar obstáculos y recalcular la ruta
def quitar_obstaculos_y_recalcular_ruta(mapa, calculadora):
    while True:
        opcion = input("\n¿Desea quitar un obstáculo? (s/n): ").strip().lower()
        if opcion == 'n':
            break
        x, y = map(int, input(f"Ingrese las coordenadas del obstáculo a quitar (0 a {mapa.cantidad_listas - 1}, 0 a {mapa.cantidad_sublistas - 1}) separadas por espacio: ").split())
        mapa.quitar_obstaculos(x, y)
        
        # Volver a calcular la ruta
        camino = calculadora.calcular_ruta(inicio, fin)
        
        # Limpiar el mapa y marcar nuevamente el camino
        for i in range(mapa.cantidad_listas):
            for j in range(mapa.cantidad_sublistas):
                if mapa.lista[i][j] == "*":
                    mapa.lista[i][j] = "."
        mapa.marcar_coordenadas("0", "0")
        if camino:
            for paso in camino:
                if mapa.lista[paso[0]][paso[1]] == ".":
                    mapa.lista[paso[0]][paso[1]] = "*"
        else:
            print("No se encontró un camino")
        
        # Imprimir el mapa actualizado
        print("\nMapa actualizado:")
        mapa.imprimir_mapa()

# Llamar a la función para quitar obstáculos y recalcular la ruta
quitar_obstaculos_y_recalcular_ruta(mapa, calculadora)
