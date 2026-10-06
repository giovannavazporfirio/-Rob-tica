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

# fita preta: comeco 0
# fita branca: fim 1


def obstaculo():
    distancia = distance_sensor.distance(port.D)

    if (distancia > 0 and distancia < 70) or distancia == -1:
        return True
    else:
        return False


def fita():
    intensidade = color_sensor.reflection(port.E)

    if intensidade > 90:
        return 1
    elif intensidade < 20:
        return 0


def toque():
    return force_sensor.pressed(port.F)


# ============================================================
# GIRO RÁPIDO E PRECISO
# ============================================================

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

        # ----------------------------------------------------
        # VELOCIDADE
        # ----------------------------------------------------
        #
        # Longe do alvo = muito rápido
        # Perto do alvo = desacelera
        #

        if restante > 25:
            velocidade = 300

        elif restante > 15:
            velocidade = 200

        elif restante > 8:
            velocidade = 100

        elif restante > 3:
            velocidade = 150

        else:
            velocidade = 50

        # ----------------------------------------------------
        # GIRAR
        # ----------------------------------------------------

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

# ============================================================
# CALIBRAÇÃO DO DESLOCAMENTO
# ============================================================

TURN_DEG_MOT = 180

# Quantos cm o robô anda com 1 volta da roda
CM_PER_ROT = 17.6


def deg_for_cm(cm):
    return int(cm / CM_PER_ROT * 360)


# ============================================================
# ANDAR 20 CM
# ============================================================

async def andar_20cm():

    graus = deg_for_cm(19)

    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1,
        graus,
        0,
        velocity=200
    )


# ============================================================
# MAIN
# ============================================================

async def main():

    comecou = False

    await runloop.until(toque)

    motor_pair.move(motor_pair.PAIR_1, 0)

    await runloop.until(lambda: (distance_sensor.distance(port.D) > 0 and distance_sensor.distance(port.D) < 50) or distance_sensor.distance(port.D) == -1)
    motor_pair.stop(motor_pair.PAIR_1)

    while True:

        print("loop comecou")

        # ====================================================
        # ANDAR
        # ====================================================

        if comecou == True:

            await andar_20cm()

        else:

            comecou = True

        # ====================================================
        # SUA LÓGICA ORIGINAL
        # ====================================================
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
