

class Entorno:

    def __init__(self):
        self.agentes = []

    def get_percepciones(self, agente):
        raise Exception("No existe implementacion")

    def ejecutar(self, agente):
        raise Exception("No existe implementacion")

    def evolucionar(self):
        if not self.finalizar():
            for agente in self.agentes:
                self.get_percepciones(agente)
                self.ejecutar(agente)

    def run(self):
        while True:
            if self.finalizar():
                break
            self.evolucionar()

    def finalizar(self):
        return any(not agente.vive for agente in self.agentes)

    def insertar(self, agente):
        self.agentes.append(agente)
