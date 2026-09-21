# Giovanna Vaz Porfirio
# Lucas Barbosa Coutinho
# Pedro Henrique Santos

from hub import light_matrix
import runloop

from hub import port
from hub import sound
from hub import light_matrix
import runloop, time, motor_pair, distance_sensor, color_sensor, color, force_sensor

#fita preta: comeco
#fita branca: fim

def obstaculo():
    distancia = distance_sensor.distance(port.D)
    return distancia > 0 and distancia < 50
def fita():
    intensidade = color_sensor.reflection(port.E)
    if intensidade > 90:
        return True
    elif intensidade < 10:
        return False
def toque():
    return force_sensor.pressed(port.F)

tentativa = {}
#tentativa[1] += [90, 180]

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
comecou = False
async def main():
    await runloop.until(toque)
    motor_pair.move(motor_pair.PAIR_1, 0)
    #await runloop.until(lambda: not fita())
    #comecou = True
    while not fita()
    

runloop.run(main())
