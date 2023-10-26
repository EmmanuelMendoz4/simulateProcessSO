# Importación de las clases Queue y namedtuple desde sus respectivos módulos
from queue import Queue
from collections import namedtuple

# Definición de la estructura de datos para un proceso
Proceso = namedtuple("Proceso", ["nombre", "tiempo_ejecucion", "prioridad"])

# Clase para el planificador de procesos
class PlanificadorProcesos:

  def __init__(self, procesos):
    self.procesos = procesos

  def calcular_quantum(self):
    # Calcula el quantum usando el tiempo de ejecución del primer proceso en la lista
    if self.procesos:
      tiempoTotal = 0.0
      canProcesos = 0
      for i in range(len(self.procesos)):
        tiempoTotal += self.procesos[i].tiempo_ejecucion
        canProcesos += 1
        
      return tiempoTotal/canProcesos
    return 0

  def fifo(self, quantum):
    tiempo_total = 0
    tiempo_respuesta = 0  # Variable para calcular el tiempo de respuesta promedio
    tiempo_promedio = 0
    print("Tabla de procesos (FIFO):")
    print(
        "Proceso | Tiempo de Ejecución | Tiempo de Comienzo | Tiempo de Finalización | Tiempo de Respuesta"
    )
    for proceso in self.procesos:
      tiempo_quantum = proceso.tiempo_ejecucion
      tiempo_respuesta += tiempo_total
      tiempo_finalizacion = tiempo_total + tiempo_quantum
      tiempo_promedio += tiempo_finalizacion  # Acumula el tiempo de finalización total
      print(
          f"{proceso.nombre:^7}| {proceso.tiempo_ejecucion:^20} | {tiempo_total:^18} | {tiempo_finalizacion:^21}  | {tiempo_respuesta:^19}"
      )
      tiempo_total += tiempo_quantum
      proceso = proceso._replace(tiempo_ejecucion=proceso.tiempo_ejecucion - tiempo_quantum)
      if proceso.tiempo_ejecucion <= 0:
        continue
    tiempo_promedio = tiempo_promedio / len(
        self.procesos)  # Calcula el tiempo de respuesta promedio
    print(f"\nTiempo total de ejecución: {tiempo_total}")
    print(f"Tiempo promedio de respuesta: {tiempo_promedio}")

  def sjf(self, quantum):
    # Ordena los procesos por su tiempo de ejecución
    procesos_ordenados = sorted(self.procesos,
                                key=lambda x: x.tiempo_ejecucion)
    tiempo_total = 0
    tiempo_respuesta = 0
    tiempo_promedio = 0
    print("Tabla de procesos (Shortest Job First - SJF):")
    print(
        "Proceso | Tiempo de Ejecución | Tiempo de Comienzo | Tiempo de Finalización | Tiempo de Respuesta"
    )
    for proceso in procesos_ordenados:
      tiempo_quantum = proceso.tiempo_ejecucion
      tiempo_respuesta += tiempo_total
      tiempo_finalizacion = tiempo_total + tiempo_quantum
      tiempo_promedio += tiempo_finalizacion
      print(
          f"{proceso.nombre:^7} | {proceso.tiempo_ejecucion:^20} | {tiempo_total:^18} | {tiempo_finalizacion:^21} | {tiempo_respuesta:^19}"
      )
      tiempo_total += tiempo_quantum
    tiempo_promedio = tiempo_promedio / len(
      self.procesos)
    print(f"Tiempo promedio de respuesta: {tiempo_promedio}")

  def round_robin(self, quantum):
    cola = Queue()
    for proceso in self.procesos:
      cola.put(proceso)
    tiempo_total = 0
    tiempo_respuesta = 0
    print(f"Tabla de procesos (Round Robin con Quantum {quantum}):")
    print(
        "Proceso | Tiempo de Ejecución | Tiempo de Comienzo | Tiempo de Finalización | Tiempo de Respuesta"
    )
    while not cola.empty():
      proceso_actual = cola.get()
      tiempo_ejecucion_actual = min(quantum, proceso_actual.tiempo_ejecucion)
      tiempo_respuesta += tiempo_total
      print(
          f"{proceso_actual.nombre:^7} | {proceso_actual.tiempo_ejecucion:^20} | {tiempo_total:^18} | {tiempo_total + tiempo_ejecucion_actual:^21} | {tiempo_respuesta:^19}"
      )
      tiempo_total += tiempo_ejecucion_actual
      proceso_actual = proceso_actual._replace(
          tiempo_ejecucion=proceso_actual.tiempo_ejecucion -
          tiempo_ejecucion_actual)
      if proceso_actual.tiempo_ejecucion > 0:
        cola.put(proceso_actual)
    tiempo_respuesta /= len(self.procesos)
    print(f"Tiempo promedio de respuesta: {tiempo_respuesta}")

  def prioridad(self, quantum):
    # Ordena los procesos por su prioridad (mayor a menor)
    procesos_ordenados = sorted(self.procesos)
    tiempo_total = 0
    tiempo_respuesta = 0
    print("Tabla de procesos (Prioridad):")
    print(f"\n Quantum: {quantum}")
    print(
        "Proceso | Tiempo de Ejecución | Tiempo de Comienzo | Tiempo de Finalización | Tiempo de Respuesta"
    )

    tiempo_quantum = 0
    
    for proceso in procesos_ordenados:
      
      if proceso.tiempo_ejecucion < quantum:
        print(
            f"{proceso.nombre:^7}|{proceso.tiempo_ejecucion:^20}|{tiempo_total:^18}|{tiempo_total + tiempo_quantum:^21}|{tiempo_respuesta:^19}"
        )

      
      
      tiempo_respuesta /= len(self.procesos)
    print(f"Tiempo promedio de respuesta: {tiempo_respuesta}")


# Ejemplo de uso con los datos proporcionados
procesos = [
    Proceso("A", 7, 4),
    Proceso("B", 6, 1),
    Proceso("C", 6, 5),
    Proceso("D", 9, 2),
    Proceso("E", 10, 3)
]

planificador = PlanificadorProcesos(procesos)
quantum = planificador.calcular_quantum()

print("FIFO:")
planificador.fifo(quantum)

print("\nShortest Job First (SJF):")
planificador.sjf(quantum)

print("\nRound Robin:")
planificador.round_robin(quantum)

print("\nPrioridad:")
planificador.prioridad(quantum)
