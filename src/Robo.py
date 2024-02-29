import inquirer
import typer
import sys
from pydobot import Dobot
from serial.tools import list_ports
from yaspin import yaspin

spinner = yaspin(text="Processando...", color="green")
app = typer.Typer()
available_ports = list_ports.comports()

# Prompts user to select a port
chosen_port = inquirer.prompt([
    inquirer.List("porta", message="Escolha uma porta", choices=[x.device for x in available_ports])
])["porta"]
print(f"Porta escolhida: {chosen_port}")


class Robot:
    # Initializes robot
    def __init__(self):
        self.port = chosen_port
        self.robo = Dobot(port=self.port, verbose=False)
        self.robo.speed(200, 200)

    # Gets current position
    def current_position(self):
        return self.robo.pose()

    # Moves to a specific position
    def move_to(self, x, y, z, r, wait=True):
        self.robo.move_to(x, y, z, r)

    # Turns actuator on
    def actuator_on(self):
        self.robo.suck(True)
    
    # Shuts actuator down
    def actuator_off(self):
        self.robo.suck(False)   
        
    
    
# Creates the CLI
@app.command(name="interface")
def interface():
    robo = Robot()
    starting_pose = robo.current_position()
    choices = ["Posição atual",  "Movimentar", "Ligar atuador", "Sair"]

    while True:
        prompts = [
            inquirer.List("interface", message="Escolha um comando:", choices=choices),
        ]

        respostas = inquirer.prompt(prompts)
        choices = process(respostas, robo, starting_pose, choices)

# Processes the choices from the CLI
def process(data, robo, starting_pose, choices):
    command = data["interface"]

    # Outputs current position
    if command == "Posição atual":
        spinner.start()	
        posicao_atual = robo.current_position()
        spinner.stop()
        print(f"Posição atual: {posicao_atual}")

    # Moves by imputed distance
    if command == "Movimentar":
            distance_x = float(typer.prompt("Distância a ser movida no eixo X:"))
            distance_y = float(typer.prompt("Distância a ser movida no eixo Y:"))
            distance_z = float(typer.prompt("Distância a ser movida no eixo Z:"))
            distance_r = float(typer.prompt("Distância a ser movida na rotação:"))
            new_position_x = starting_pose[0] + distance_x
            new_position_y = starting_pose[1] + distance_y
            new_position_z = starting_pose[2] + distance_z
            new_position_r = starting_pose[3] + distance_r
            spinner.start()
            robo.move_to(new_position_x, new_position_y, new_position_z, new_position_r, wait=True)

            if "Posição inicial" not in choices:
                choices.insert(1, "Posição inicial")

            spinner.stop()
            print(f"X={new_position_x}, Y={new_position_y}, Z={new_position_z}, R={new_position_r}")

    # Turns actuator on
    if command == "Ligar atuador":
        spinner.start()
        robo.actuator_on()
        spinner.stop()

        if "Ligar atuador" in choices:
            choices.remove("Ligar atuador")
            choices.insert(2, "Desligar atuador")

    # Shuts down actuator
    if command == "Desligar atuador":
        spinner.start()
        robo.actuator_off()
        spinner.stop()

        if "Desligar atuador" in choices:
            choices.remove("Desligar atuador")
            choices.insert(2, "Ligar atuador")

    # Moves to starting position
    if command == "Posição inicial":
        spinner.start()
        robo.move_to(starting_pose[0], starting_pose[1], starting_pose[2], starting_pose[3], wait=True)
        spinner.stop()

        if "Posição inicial" in choices:
            choices.remove("Posição inicial")

    # Exits interface
    if command == "Sair": 
        sys.exit()

    return choices

# Starts app
if __name__ == "__main__":
    app()