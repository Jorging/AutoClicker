import tkinter as tk
import pyautogui
import time
import threading

# Variável de controle global
parar = False

def iniciar_autoclick():
    global parar
    parar = False

    try:
        total = int(entry_qtd.get())
        intervalo = float(entry_intervalo.get())
    except ValueError:
        status_label.config(text="Insira valores válidos!")
        return

    def clickar():
        status_label.config(text="Começando em 3 segundos...")
        time.sleep(3)
        status_label.config(text="Clicando...")

        for i in range(total):
            if parar:
                status_label.config(text="Interrompido!")
                return
            pyautogui.click()
            time.sleep(intervalo)

        status_label.config(text="Finalizado!")

    threading.Thread(target=clickar).start()

def parar_autoclick():
    global parar
    parar = True

# Criando a interface
janela = tk.Tk()
janela.title("AutoClicker")
janela.geometry("300x250")

# Título
titulo = tk.Label(janela, text="AutoClicker", font=("Arial", 16))
titulo.pack(pady=10)

# Entrada: Quantidade de cliques
tk.Label(janela, text="Quantidade de cliques:").pack()
entry_qtd = tk.Entry(janela)
entry_qtd.insert(0, "10")
entry_qtd.pack()

# Entrada: Intervalo entre cliques
tk.Label(janela, text="Intervalo (segundos):").pack()
entry_intervalo = tk.Entry(janela)
entry_intervalo.insert(0, "0.1")
entry_intervalo.pack()

# Botões
btn_iniciar = tk.Button(janela, text="Iniciar", command=iniciar_autoclick, bg="green", fg="white")
btn_iniciar.pack(pady=10)

btn_parar = tk.Button(janela, text="Parar", command=parar_autoclick, bg="red", fg="white")
btn_parar.pack()

# Status
status_label = tk.Label(janela, text="")
status_label.pack(pady=10)

# Loop da interface
janela.mainloop()
