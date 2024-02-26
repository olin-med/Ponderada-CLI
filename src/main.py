# main.py
import typer
import inquirer
from yaspin import yaspin
import time

# Cria uma instância da aplicação
app = typer.Typer()

# Cria um comando do CLI
@app.command()
def soma(a: int, b: int = 0):
    print(a + b)

# Cria um segundo comando do CLI
@app.command()
def subtracao(a: int, b: int = 0):
    print(a - b)

# Cria um terceiro comando do CLI
@app.command()
def soma_interativa():
    continuar = True
    while continuar:
        a = typer.prompt("Digite o primeiro número")
        b = typer.prompt("Digite o segundo número")
        print(int(a) + int(b))
        continuar = typer.confirm("Deseja continuar?")

# Cria um quarto comando do CLI
@app.command()
def calculadora():
    # realiza lista de perguntas para o usuário
    perguntas = [
        inquirer.List("operacao", message="Qual operação deseja realizar?", choices=["soma", "subtração","multiplicacao","divisao"]),
        inquirer.Text("a", message="Digite o primeiro número"),
        inquirer.Text("b", message="Digite o segundo número")
    ]
    # realiza a leitura das respostas
    respostas = inquirer.prompt(perguntas)
    # chama a funcao que processa a operação e exibe uma spinner para o usuário
    spinner = yaspin(text="Processando...", color="yellow")
    # inicia o spinner
    spinner.start()
    # realiza a operação
    saida = processar(respostas)
    # para o spinner
    spinner.stop()
    # exibe o resultado
    print(saida)

# Função que processa a operação
def processar(dados):
    time.sleep(5)
    operacao = dados["operacao"]
    a = float(dados["a"])
    b = float(dados["b"])
    if operacao == "soma":
        return (a + b)
    elif operacao == "subtração":
        return (a - b)
    elif operacao == "multiplicacao":
        return (a * b)
    elif operacao == "divisao":
        return (a / b)
    
# Executa a aplicação
if __name__ == "__main__":
    app()
