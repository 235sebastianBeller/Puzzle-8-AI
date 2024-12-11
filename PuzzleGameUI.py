
import pygame
import random
import time
from AgentePuzzle import AgentePuzzle
from Puzzle import Puzzle

class PuzzleGame:
    WINDOW_WIDTH = 880
    WINDOW_HEIGHT = 600
    FPS = 10
    CELL_BORDER_COLOR = (230, 57, 70)
    BACKGROUND_COLOR = (20, 33, 61)
    SELECTED_CELL_COLOR = (255, 255, 255)
    ROWS = 3
    COLS = 3
    CELLS_COUNT = ROWS * COLS

    def __init__(self):
        """
        Inicializa el objeto PuzzleGame.
        
        Inicializa pygame, crea la ventana del juego, carga los assets y
        inicializa el juego.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Puzzle Game')
        self.clock = pygame.time.Clock()
        self.load_assets()
        self.initialize_game()

    def load_assets(self):
        """
        Carga los assets para el juego.

        Carga las imagenes para el fondo, el agente, el boton del agente y
        el boton para mezclar.
        """
        self.bg = pygame.image.load('./perrito2.jpg')
        self.bg_agent = pygame.image.load('./agente2.png')
        self.btn_agente = pygame.image.load('./btn-agente.png')
        self.btn_mezclar = pygame.image.load('./btn-mezclar.png')
        self.bg_rect = self.bg.get_rect()
        self.CELL_WIDTH = self.bg_rect.width // self.COLS
        self.CELL_HEIGHT = self.bg_rect.height // self.ROWS
        self.bg_cero = pygame.Surface((self.CELL_WIDTH, self.CELL_HEIGHT))
        self.bg_cero.fill(self.BACKGROUND_COLOR)

    def initialize_game(self):
        """
        Inicializa el juego.

        Establece las areas de los botones, inicializa las celdas, y establece
        los valores iniciales de las variables para el juego.
        """
        self.area_btn_agente = pygame.Rect(50, self.WINDOW_HEIGHT // 2 - 100 + 200, 100, 25)
        self.area_btn_mezclar = pygame.Rect(50, self.WINDOW_HEIGHT // 2 - 100 + 200 + 2 * self.area_btn_agente.height, 100, 25)
        self.cells = self.get_random_cells()
        self.img_selected = None
        self.cell_selected = None
        self.agent = False
        self.show = "order"
        self.data = None
        self.index = None

    def get_random_cells(self):
        """
        Genera una lista de celdas con sus posiciones aleatorias y las
        devuelve.
        """
        cells = []
        random_list = list(range(self.CELLS_COUNT))
        for i in range(self.CELLS_COUNT):
            x = (i % self.COLS) * self.CELL_WIDTH
            y = (i // self.ROWS) * self.CELL_HEIGHT
            rect = pygame.Rect(x, y, self.CELL_WIDTH, self.CELL_HEIGHT)
            rand_pos = random.choice(random_list)
            random_list.remove(rand_pos)
            cells.append({'rect': rect, 'border': self.CELL_BORDER_COLOR, 'order': i, 'pos_shuffle': rand_pos})
        return cells

    def solve_with_agent(self, tec, heuristic, init_state):
        """
        Resuelve el puzzle con un agente utilizando la tecnica y la heuristica
        especificadas. Devuelve una lista de acciones para resolver el puzzle.

        """
        juego = Puzzle()
        juan = AgentePuzzle()
        juego.insertar(juan)
        juan.heuristica = heuristic
        juan.tecnica = tec
        juan.set_estado_inicial(init_state)
        juan.acciones = []
        juego.run()
        return juan.acciones

    def is_valid_state(self, puzzle_sin_cero):
        """
        Verifica si un estado del puzzle es resoluble.
        
        Un estado del puzzle es resoluble si el numero de inversiones
        de sus piezas es par. La funcion devuelve True si el estado
        es resoluble y False en caso contrario.
        """
        inversiones = 0
        puzzle_sin_cero = [elemento for fila in puzzle_sin_cero for elemento in fila if elemento != 0]
        for i in range(len(puzzle_sin_cero)):
            for j in range(i + 1, len(puzzle_sin_cero)):
                if puzzle_sin_cero[i] > puzzle_sin_cero[j]:
                    inversiones += 1
        return inversiones % 2 == 0

    def get_data(self):
        """
        Devuelve el estado del puzzle en forma de matriz, donde cada elemento
        es el numero de la pieza en esa posicion.
        """
        
        data = []
        lista = []
        for elemento in self.cells:
            index = elemento["order"]
            if index % self.COLS == 0 and index != 0:
                data.append(lista)
                lista = []
            lista.append(elemento["pos_shuffle"] + 1 if elemento["pos_shuffle"] != 8 else 0)
        data.append(lista)
        return data

    def is_valid_selection(self, img_selected, cell_selected):
        
        """
        Verifica si una seleccion de celda es valida.
        
        Una selecci n es valida si la celda seleccionada y la imagen
        seleccionada no son la misma pieza y la celda seleccionada
        o la imagen seleccionada es la pieza vacia (posicion 8).
        """
        return (img_selected["pos_shuffle"] != cell_selected["pos_shuffle"]) and (cell_selected["pos_shuffle"] == 8 or img_selected["pos_shuffle"] == 8)

    def is_near(self, img_selected, cell_selected):
        axis_x = abs(img_selected["rect"].x - cell_selected["rect"].x)
        axis_y = abs(img_selected["rect"].y - cell_selected["rect"].y)
        return axis_x + axis_y == 158

    def get_posiciones_mov(self, estado_actual, estado_anterior):
        """
        Devuelve una tupla con las posiciones que se movieron de estado_anterior a estado_actual.
        """
        estados_dif = []
        for i in range(len(estado_actual)):
            for j in range(len(estado_actual[0])):
                if estado_actual[i][j] != estado_anterior[i][j]:
                    estados_dif.append(estado_actual[i][j])
        return tuple(estados_dif)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button:
                self.handle_mouse_click(pygame.mouse.get_pos())
        return True

    def handle_mouse_click(self, mouse_position):        
        if self.area_btn_agente.collidepoint(mouse_position) and self.data:
            self.data = self.get_data()
            self.acciones = self.solve_with_agent("a_estrella", "manhattan", self.data)
            self.agent = True
            self.data = None
        elif self.area_btn_mezclar.collidepoint(mouse_position):
            self.shuffle_cells()
        else:
            self.handle_cell_click(mouse_position)

    def shuffle_cells(self):
        """
        Mezcla las celdas y muestra el estado actual. Este metodo se
        encarga de asignar un estado aleatorio a las celdas de manera
        que se cumpla la condicion de que el estado sea valido.
        """        
        while True:
            self.cells = self.get_random_cells()
            data = self.get_data()
            if self.is_valid_state(data):
                break
        self.data=data
        self.show = "pos_shuffle"

    def handle_cell_click(self, mouse_position):        
        for cell in self.cells:
            rect = cell["rect"].copy()
            rect.x = rect.x + self.WINDOW_WIDTH // 2 - self.CELL_WIDTH * (self.COLS / 2)
            rect.y = rect.y + self.WINDOW_HEIGHT // 2 - self.CELL_HEIGHT * (self.ROWS / 2)
            if rect.collidepoint(mouse_position):
                self.select_cell(cell)

    def select_cell(self, cell):
        """
        Selecciona una celda y la marca como seleccionada.
        """
        if not self.img_selected:
            self.img_selected = cell
            cell['border'] = self.SELECTED_CELL_COLOR
        else:
            self.cell_selected = cell
            if not self.is_near(self.img_selected, self.cell_selected):
                self.reset_selection()
            elif self.is_valid_selection(self.img_selected, self.cell_selected):
                self.swap_cells()

    def reset_selection(self):
        self.img_selected["border"] = self.CELL_BORDER_COLOR
        self.cell_selected = None
        self.img_selected = None

    def swap_cells(self):
        """
        Intercambia las celdas seleccionadas, actualizando el estado de las
        celdas y reseteando la seleccion.
        """
        self.cell_selected["pos_shuffle"], self.img_selected["pos_shuffle"] = self.img_selected["pos_shuffle"], self.cell_selected["pos_shuffle"]
        self.reset_selection()

    def update(self):
        """
        Actualiza el estado de la interfaz en cada frame.
        
        Si se esta ejecutando el agente, se mueve a la siguiente accion
        en la lista de acciones. Si se ha alcanzado el final de la lista,
        se desactiva el agente.
        """
        if self.agent:
            if self.index is None:
                self.index = 1
            if self.index == len(self.acciones):
                self.agent = False
                self.index = None
            else:
                self.move_agent()

    def move_agent(self):
        """
        Mueve al agente a la siguiente accion en la lista de acciones.
        
        Selecciona las celdas que se van a intercambiar y se actualiza el
        estado de las celdas.
        
        Si se ha alcanzado el final de la lista de acciones, se termina
        el agente.
        """
        accion_anterior = self.acciones[self.index - 1]
        accion_actual = self.acciones[self.index]
        c1, c2 = self.get_posiciones_mov(accion_actual, accion_anterior)
        for cell in self.cells:
            if cell["pos_shuffle"] == 8:
                self.cell_selected = cell
            if cell["pos_shuffle"] == max(c1, c2) - 1:
                self.img_selected = cell
        self.swap_cells()
        self.index += 1
        time.sleep(0.5)

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_ui()
        self.draw_cells()
        pygame.display.update()

    def draw_ui(self):
        self.screen.blit(pygame.transform.scale(self.bg_agent, (100, 200)), (50, self.WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(pygame.transform.scale(self.btn_agente, (self.area_btn_agente.width, self.area_btn_agente.height)), self.area_btn_agente)
        self.screen.blit(pygame.transform.scale(self.btn_mezclar, (self.area_btn_mezclar.width, self.area_btn_mezclar.height)), self.area_btn_mezclar)
        if self.agent:
            fuente = pygame.font.Font(None, 50) 
            text = f"Numero de movidas: {len(self.acciones)-1}"
            text_render = fuente.render(text, True, (255,255,26))
            rect_texto = text_render.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//16))
            self.screen.blit(text_render, rect_texto)

    def draw_cells(self):
        for cell in self.cells:
            pos_shuffle = cell[self.show]
            img = pygame.Rect(self.cells[pos_shuffle]["rect"].x, self.cells[pos_shuffle]["rect"].y, self.CELL_WIDTH, self.CELL_HEIGHT)
            i = cell["rect"].x + self.WINDOW_WIDTH // 2 - self.CELL_WIDTH * (self.COLS / 2)
            j = cell["rect"].y + self.WINDOW_HEIGHT // 2 - self.CELL_HEIGHT * (self.ROWS / 2)
            if pos_shuffle != 8:
                self.screen.blit(self.bg, (i, j), img)
            else:
                self.screen.blit(self.bg_cero, (i, j))
            rect_copy = cell["rect"].copy()
            rect_copy.x = i
            rect_copy.y = j
            pygame.draw.rect(self.screen, cell["border"], rect_copy, 1)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)