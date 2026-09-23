# Giovanna Vaz Porfirio
# Lucas Barbosa Coutinho
# Pedro Henrique Santos

from hub import light_matrix
import runloop

from hub import port
from hub import sound
from hub import light_matrix
from hub import motion_sensor
from motor import run_for_degrees
from time import sleep
import runloop, time, motor_pair, distance_sensor, color_sensor, color, force_sensor, random

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
def girar(sinal):
    print("girando")
    motion_sensor.reset_yaw(0)
    motor_pair.stop(motor_pair.PAIR_1)
    motor_pair.move_tank(motor_pair.PAIR_1, 200*sinal, -200*sinal)
def esperarcurva(angulo):
    return abs(motion_sensor.tilt_angles()[0] * -0.1) > angulo

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
comecou = False
async def main():
    await runloop.until(toque)
    #await runloop.until(lambda: not fita())
    #comecou = True
    while True:
        print("loop comecou")
        motor_pair.move(motor_pair.PAIR_1, 0)
        await runloop.until(obstaculo)
        print("detectou obstaculo")
        #se esta livre ou nao:
        esquerda = False
        direita = False
        girar(1)
        await runloop.until(lambda: esperarcurva(90))
        motor_pair.stop(motor_pair.PAIR_1)
        print("girou")
        sleep(1)
        if obstaculo() == False:
            direita = True
        girar(-1)
        await runloop.until(lambda: esperarcurva(-180))
        motor_pair.stop(motor_pair.PAIR_1)
        if obstaculo() == False:
            esquerda = True
        if direita == True and esquerda == False:
            girar(1)
            await runloop.until(lambda: esperarcurva(180))
        elif direita == True and esquerda == True:
            escolhido = random.randint(1, 2)
            if escolhido == 1:
                girar(1)
                await runloop.until(lambda: esperarcurva(180))
        elif direita == False and esquerda == False:
            girar(-1)
            await runloop.until(lambda: esperarcurva(-90))
                

runloop.run(main())
