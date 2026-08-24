from hub import port 
from hub import sound
from hub import light_matrix
import runloop, motor_pair, distance_sensor, color_sensor, color, force_sensor
#Função retorna verdadeiro (True) se um obstáculo for encontrado a 5cm
CM_PER_ROT = 17.6
def deg_for_cm(cm):
    return int(cm / CM_PER_ROT * 360)
def obstacle_found():
    distance = distance_sensor.distance(port.F)
    # distância tem que ser válida e inferior a 5cm (50mm)
    return distance > 0 and distance < 50
def color_found():
    return color_sensor.color(port.A) == color.BLACK
def force_sensor_pressed():
    return force_sensor.pressed(port.B)
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)
async def main():
    while True:
        # Seta o par de motores e inicia o movimento
        motor_pair.move(motor_pair.PAIR_1, 0)
        # aguarda até que o obstáculo seja encontrado
        await runloop.until(obstacle_found)
        # para os motores e encerra a execução do programa
        motor_pair.stop(motor_pair.PAIR_1)
        print("Obstáculo encontrado!!")
        #####################
        # Direita
        TURN_DEG_MOT = 200
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1,
            TURN_DEG_MOT,
            +600,
            -600
        )
        motor_pair.move(motor_pair.PAIR_1, 0)
        # wait until color found
        await runloop.until(color_found)
        # stop and exit
        motor_pair.stop(motor_pair.PAIR_1)
        print("Leu a cor PRETA!!!!")
        #####################
        dist_cm = 20# distância de cada segmento
        dist_deg = deg_for_cm(dist_cm)
        # 1) Curva para a direita (esq 20%, dir 70%)
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1,
            dist_deg,
            200,# esquerdo
            700# direito
        )
        # 2) Curva para a esquerda (esq 70%, dir 20%)
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1,
            dist_deg,
            700,
            200
        )
        # 3) Curva para a esquerda (esq 70%, dir 20%)
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1,
            dist_deg,
            700,
            200
        )
        # 4) Curva para a direita (esq 20%, dir 70%)
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1,
            dist_deg,
            200,
            700
        )
        await runloop.until(force_sensor_pressed)
        print("Sensor pressionado!!")
        await motor_pair.move_for_degrees(
            motor_pair.PAIR_1,
            deg_for_cm(30),
            0, # steering reto
            velocity=600 # ajuste se quiser (deg/s)
        )
        # Trás 30 cm
        await motor_pair.move_for_degrees(
            motor_pair.PAIR_1,
            -deg_for_cm(30),# negativo = trás
            0,
            velocity=600
        )
        sound.volume(75)
        for i in range (4):
            light_matrix.show_image(light_matrix.IMAGE_HAPPY)
            await sound.beep(400, 250)
            light_matrix.show_image(light_matrix.IMAGE_SAD)
            await sound.beep(600, 250)
            light_matrix.show_image(light_matrix.IMAGE_ANGRY)
            await sound.beep(800, 250)
            light_matrix.show_image(light_matrix.IMAGE_HEART)
            await sound.beep(1000, 250)
        print("Sons emitidos com sucesso!!!")
runloop.run(main())
