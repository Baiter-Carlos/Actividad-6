import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog


def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + '\n')
                text_area.config(state=tk.DISABLED)
                text_area.yview(tk.END)
        except:
            print("Error al recibir el mensaje.")
            client_socket.close()
            break


def send_message(client_socket, message_entry, text_area, name):
    message = message_entry.get()
    if message:
        try:
            
            client_socket.send(f"{name}: {message}".encode('utf-8'))
            message_entry.delete(0, tk.END)
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"Tú: {message}\n")
            text_area.config(state=tk.DISABLED)
            text_area.yview(tk.END)
        except:
            print("Error al enviar el mensaje.")
            client_socket.close()


def start_client_gui():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5555))
    window = tk.Tk()
    window.withdraw()
    name = simpledialog.askstring("Nombre", "Por favor, introduce tu nombre:")
    window.deiconify()

    window.title(f"Chat Cliente - {name}")

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, width=50, height=15)
    text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

    message_entry = tk.Entry(window, width=40)
    message_entry.grid(column=0, row=1, padx=10, pady=10)

    send_button = tk.Button(window, text="Enviar", command=lambda: send_message(client, message_entry, text_area, name))
    send_button.grid(column=1, row=1, padx=10, pady=10)

    receive_thread = threading.Thread(target=receive_messages, args=(client, text_area))
    receive_thread.start()

    window.mainloop()

if __name__ == "__main__":
    start_client_gui()