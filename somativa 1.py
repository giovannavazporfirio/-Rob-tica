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
    return distancia > 0 and distancia < 60
def fita():
    intensidade = color_sensor.reflection(port.E)
    if intensidade > 90:
        return True
    elif intensidade < 10:
        return False
def toque():
    return force_sensor.pressed(port.F)
async def girar(angulo):
    sinal = 1
    if angulo < 0:
        sinal = -1
    motor_pair.move_tank(
        motor_pair.PAIR_1,
        120 * sinal,
        -120 * sinal
    )
    inicio = time.ticks_ms()
    if sinal == 1:
        while motion_sensor.tilt_angles()[0] * -0.1 <= angulo:
            if time.ticks_diff(time.ticks_ms(), inicio) >= 3000:
                break
            await runloop.sleep_ms(1)
    else:
        while motion_sensor.tilt_angles()[0] * -0.1 >= angulo:
            if time.ticks_diff(time.ticks_ms(), inicio) >= 3000:
                break
            await runloop.sleep_ms(1)
    motor_pair.stop(motor_pair.PAIR_1)
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)

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
            motor_pair.stop(motor_pair.PAIR_1)
        else:
            voltando = False
        #se esta livre ou nao:
        async def checar():
            motion_sensor.reset_yaw(0)
            await runloop.until(motion_sensor.stable)
            esquerda = False
            direita = False
            await girar(90)
            if obstaculo() == False:
                direita = True
            await girar(-90)
            await girar(-90)
            if obstaculo() == False:
                esquerda = True
            return esquerda, direita
        esquerda, direita = await checar()
        if direita == True and esquerda == False:
            await girar(90)
            await girar(90)
        elif direita == True and esquerda == True:
            escolhido = random.randint(1, 2)
            if escolhido == 1:
                await girar(90)
                await girar(90)
        elif direita == False and esquerda == False:
            print("dando meia volta")
            await girar(-90)
            await motor_pair.move_for_degrees(
                motor_pair.PAIR_1,
                deg_for_cm(20),
                0 # steering reto
            )
            esquerda, direita = await checar()
            if direita == True and esquerda == False:
                await girar(90)
                await girar(90)
            elif direita == True and esquerda == True:
                escolhido = random.randint(1, 2)
                if escolhido == 1:
                    await girar(90)
                    await girar(90)
            elif direita == False and esquerda == False:
                await girar(90)
                await motor_pair.move_for_degrees(
                    motor_pair.PAIR_1,
                    deg_for_cm(20),
                    0 # steering reto
                )
                voltando = True



runloop.run(main())
