import socket
import threading
import random
import string
import pygame
import sys

# Vigenère Cipher Function
def vigenere_cipher(text, key, encrypt=True):
    vige = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    key_index = 0

    for char in text:
        if char == " ":
            result += " "
        elif char in vige:
            shift = vige.index(key[key_index % len(key)])
            shift = shift if encrypt else -shift
            new_index = (vige.index(char) + shift) % 26
            result += vige[new_index]
            key_index += 1
        else:
            result += char

    return result

# Function to receive messages
def receive_messages(client_socket, chat_messages):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            key, encrypted_msg = msg.split("#", 1)
            decrypt_msg = vigenere_cipher(encrypted_msg, key, encrypt=False)
            chat_messages.append(f"Received: {decrypt_msg}")
        except:
            break

# Function to start the client
def start_client(host='127.0.0.1', port=1111):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

# Pygame Initialization
def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Vigenère Cipher Client")
    font = pygame.font.Font(None, 36)

    input_box = pygame.Rect(150, 700, 800, 40)
    send_button = pygame.Rect(750, 700, 100, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    button_color = pygame.Color('gray')
    color = color_inactive
    active = False
    text = ''
    chat_messages = []

    client_socket = start_client()
    threading.Thread(target=receive_messages, args=(client_socket, chat_messages)).start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif send_button.collidepoint(event.pos):
                    if text:
                        key = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
                        encrypted_msg = vigenere_cipher(text, key)
                        to_send = f"{key}#{encrypted_msg}"
                        client_socket.send(to_send.encode())
                        chat_messages.append(f"Sent: {text}")
                        text = ''
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        key = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
                        encrypted_msg = vigenere_cipher(text, key)
                        to_send = f"{key}#{encrypted_msg}"
                        client_socket.send(to_send.encode())
                        chat_messages.append(f"Sent: {text}")
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(650, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.draw.rect(screen, button_color, send_button)
        send_text = font.render("Send", True, (255, 255, 255))
        screen.blit(send_text, (send_button.x + 20, send_button.y + 5))

        y_offset = 50
        for msg in chat_messages:
            msg_surface = font.render(msg, True, (255, 255, 255))
            screen.blit(msg_surface, (50, y_offset))
            y_offset += 30

        pygame.display.flip()

if __name__ == "__main__":
    main()

