from AgenteIA.Entorno import Entorno


class Puzzle(Entorno):
    def __init__(self):
        Entorno.__init__(self)

    def get_percepciones(self, agente):
        agente.set_estado_meta([[1,2,3],[4,5,6],[7,8,0]])
        agente.programa()

    def ejecutar(self, agente):
        print(agente.acciones)
        print(len(agente.acciones))
        agente.vive=False
