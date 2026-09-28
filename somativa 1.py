# Giovanna Vaz Porfirio
# Lucas Barbosa Coutinho
# Pedro Henrique Santos

# Direita: A
# Esquerda: B
# 
# Distância: D
# Cor: E
# Força: F

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
TURN_DEG_MOT = 180
CM_PER_ROT = 17.6
def deg_for_cm(cm):# cm -> graus do motor
    return int(cm / CM_PER_ROT * 360)
async def main():
    voltando = False
    await runloop.until(toque)
    #await runloop.until(lambda: not fita())
    #comecou = True
    while True:
        print("loop comecou")
        if voltando == False:
            motor_pair.move(motor_pair.PAIR_1, 0)
            await runloop.until(obstaculo)
            print("detectou obstaculo")
        else:
            voltando = False
        #se esta livre ou nao:
        esquerda = False
        direita = False
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1,
            TURN_DEG_MOT,
            600, # esquerdo
            -600 # direito
        )
        if obstaculo() == False:
            direita = True
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1,
            TURN_DEG_MOT * 2,
            -600, # esquerdo
            600 # direito
        )
        if obstaculo() == False:
            esquerda = True
        if direita == True and esquerda == False:
            await motor_pair.move_tank_for_degrees(
                motor_pair.PAIR_1,
                TURN_DEG_MOT * 2,
                600, # esquerdo
                -600 # direito
            )
        elif direita == True and esquerda == True:
            escolhido = random.randint(1, 2)
            if escolhido == 1:
                await motor_pair.move_tank_for_degrees(
                    motor_pair.PAIR_1,
                    TURN_DEG_MOT * 2,
                    600, # esquerdo
                    -600 # direito
                )
        elif direita == False and esquerda == False:
            await motor_pair.move_tank_for_degrees(
                motor_pair.PAIR_1,
                TURN_DEG_MOT,
                -600, # esquerdo
                600 # direito
            )
            await motor_pair.move_for_degrees(
                motor_pair.PAIR_1,
                deg_for_cm(20),
                0 # steering reto
            )
            voltando = True



runloop.run(main())
