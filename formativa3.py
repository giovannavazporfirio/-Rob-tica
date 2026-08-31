# Giovanna Vaz Porfirio
# Lucas Barbosa Coutinho
# Pedro Henrique Santos

from hub import port
from hub import sound
from hub import light_matrix
import runloop, time, motor_pair, distance_sensor, color_sensor, color, force_sensor

def obstaculo():
    distance = distance_sensor.distance(port.D)
    return distance > 0 and distance < 50
def toque():
    return force_sensor.pressed(port.F)
def vermelho():
    return color_sensor.color(port.C) == color.RED
def velocidade():
    distance = distance_sensor.distance(port.D)
    if distance > 200:
        return 500
    elif distance > 100:
        return 250
    elif distance > 50:
        return 50
    else:
        return 0

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

async def main():
    velocidadeatual = 500
    motor_pair.move(
                motor_pair.PAIR_1,
                0,
                velocity = velocidadeatual
            )
    while not obstaculo() and not toque():
        if velocidade() != velocidadeatual:
            velocidadeatual = velocidade()
            motor_pair.move(
                motor_pair.PAIR_1,
                0,
                velocity = velocidadeatual
            )
            await runloop.sleep_ms(200)
    motor_pair.stop(motor_pair.PAIR_1)
    time.sleep(2)
    await runloop.until(lambda: not obstaculo())
    await motor_pair.move_tank_for_degrees(
        motor_pair.PAIR_1,
        360,
        +600,
        -600
    )
    motor_pair.move(motor_pair.PAIR_1, 0)
    await runloop.until(vermelho)
    motor_pair.stop(motor_pair.PAIR_1)
    light_matrix.show_image(light_matrix.IMAGE_HAPPY)
    await sound.beep(400, 250)
    await sound.beep(600, 250)
    await sound.beep(800, 250)
    await sound.beep(1000, 250)

runloop.run(main())
