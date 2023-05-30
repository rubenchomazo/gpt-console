import openai
import typer
from colorama import Fore, Style, Back
from rich import print
from rich.table import Table

import conf


def main():
    openai.api_key = conf.config.apiKey
    print("[bold green]ChatGPT API en Python[/bold green]")
    table = Table("Comando", "Descripcion")
    table.add_row("exit", "Salir de la aplicacion")
    table.add_row("new", "Crear una nueva conversacion")
    print(table)
    # Contexto del asistente
    context = {"role": "system",
               "content": "Eres un asistente de progamación muy util, siempre das ejemplos a mis soluciones"}
    messages = [context]
    while True:
        content = __prompt()
        if content == "new":
            print("Nueva conversacion creada")
            messages = [context]
            content = __prompt()
        messages.append({"role": "user", "content": content})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)
        response_content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_content})
        generateResponse(response_content)


def generateResponse(response_content):
    if response_content.find("```"):
        print(Back.LIGHTBLACK_EX + Fore.CYAN + Style.DIM + response_content)
        # typer.secho(response_content, fg=typer.colors.BRIGHT_CYAN)
    else:
        print(f"[bold green]-> {response_content}[/bold green]")


def __prompt() -> str:
    prompt = typer.prompt("\n Sobre que quieres hablar? ")
    if prompt == "exit":
        exit = typer.confirm("Estas seguro?")
        if exit:
            print("Hasta luego!")
            raise typer.Abort()
        return __prompt()
    return prompt


if __name__ == "__main__":
    typer.run(main)
    print(" [bold green]ChatGPT API en Python[/bold green]")
