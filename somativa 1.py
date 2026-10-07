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
from time import sleep, sleep_ms
import runloop, time, motor_pair, distance_sensor, color_sensor, color, force_sensor, random

# fita preta: comeco 0
# fita branca: fim 1


def obstaculo():
    distancia = distance_sensor.distance(port.D)

    if (distancia > 0 and distancia < 105):
        return True
    else:
        return False


def fita():
    intensidade = color_sensor.reflection(port.E)

    if intensidade > 89.5: ##branco
        return 1
    elif intensidade < 20: #preto
        return 0
    else:
        return 2


def toque():
    return force_sensor.pressed(port.F)

async def girar(angulo):

    sinal = 1

    if angulo < 0:
        sinal = -1

    # Zera o giroscópio antes do giro
    motion_sensor.reset_yaw(0)
    await runloop.until(motion_sensor.stable)

    alvo = abs(angulo)

    inicio = time.ticks_ms()

    while True:

        atual = motion_sensor.tilt_angles()[0] * -0.1
        atual = abs(atual)

        restante = alvo - atual

        # Chegou no ângulo
        if restante <= 0:
            break

        # Segurança contra travamento
        if time.ticks_diff(time.ticks_ms(), inicio) >= 3000:
            break

        if restante > 25:
            velocidade = 300

        elif restante > 15:
            velocidade = 200

        elif restante > 8:
            velocidade = 100

        elif restante > 3:
            velocidade = 50

        else:
            velocidade = 25

        motor_pair.move_tank(
            motor_pair.PAIR_1,
            velocidade * sinal,
            -velocidade * sinal
        )

        await runloop.sleep_ms(2)

    motor_pair.stop(motor_pair.PAIR_1)

    # Pequena estabilização
    await runloop.sleep_ms(30)

    motion_sensor.reset_yaw(0)

    await runloop.until(motion_sensor.stable)


motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)


comecou = False

TURN_DEG_MOT = 180

# Quantos cm o robô anda com 1 volta da roda
CM_PER_ROT = 17.6


def deg_for_cm(cm):
    return int(cm / CM_PER_ROT * 360)
async def main():
    comecou = False
    chegou = False
    fugiu = False
    pfita = 0
    await runloop.until(toque)
    while True:
        print("loop comecou")
        graus = deg_for_cm(19.5)
        motion_sensor.reset_yaw(0)
        await motor_pair.move_for_degrees(
            motor_pair.PAIR_1,
            graus,
            0,
            velocity=450
        )
        await girar(90)
        if obstaculo() == False:
            continue
        else:
            
            await girar(-90)
            if obstaculo() == False:
                continue
            else:
                
                await girar(-90)
                if obstaculo() == False:
                    continue
                else:
        
                    await girar(-90)


runloop.run(main())
