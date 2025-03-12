import socket
import threading
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

private_key, public_key = generate_keys()

def public_key_to_base64(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return base64.b64encode(pem).decode()

def encrypt_rsa(text, public_key):
    ciphertext = public_key.encrypt(
        text.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode()

def decrypt_rsa(ciphertext, private_key):
    ciphertext_bytes = base64.b64decode(ciphertext)
    plaintext = private_key.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()


def sign_message(text, private_key):
    signature = private_key.sign(
        text.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()

def verify_signature(text, signature, public_key):
    try:
        public_key.verify(
            base64.b64decode(signature),
            text.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

SENDER_PUBLIC = None

def receive_messages(client_socket):
    global SENDER_PUBLIC
    while True:
        try:
            msg = client_socket.recv(4096).decode()  
            if not msg:
                break

            if msg.startswith("PUBLIC_KEY:"):

                PKEY64 = base64.b64decode(msg.split("PUBLIC_KEY:")[1])
                SENDER_PUBLIC = serialization.load_pem_public_key(PKEY64)
                print("Clé publique reçue.")
            elif msg.startswith("SIG:"):
                try:
                    sig_part, msg_part = msg.split("||MSG:")
                    signature = sig_part.replace("SIG:", "")
                    encrypted_msg = msg_part
                    decrypted_msg = decrypt_rsa(encrypted_msg, private_key)
                    if SENDER_PUBLIC and verify_signature(decrypted_msg, signature, SENDER_PUBLIC):
                        print("\nMessage reçu et vérifié:", decrypted_msg)
                    else:
                        print("Échec de la vérification de la signature.")
                except Exception as e:
                    print("Erreur lors du traitement du message signé:", e)
            else:

                try:
                    decrypted_msg = decrypt_rsa(msg, private_key)
                    print("\nMessage reçu:", decrypted_msg)
                except Exception as e:
                    print("Erreur de déchiffrement:", e)

        except Exception as e:
            print(f"Erreur: {e}")
            break

def start_client(host='127.0.0.1', port=1111):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    choice = input("Press :\n1: Envoyer la clé publique.\n-> :")
    if choice == "1":
        pem = public_key_to_base64(public_key)
        client_socket.send(("PUBLIC_KEY:" + pem).encode())  # send public key

    while True:
        msg = input("Vous: ")
        if SENDER_PUBLIC:
            encrypted_msg = encrypt_rsa(msg, SENDER_PUBLIC)
            signature = sign_message(msg, private_key)
            payload = f"SIG:{signature}||MSG:{encrypted_msg}"
            client_socket.send(payload.encode())
        else:
            print("Clé publique du destinataire non reçue, en attente...")
            
if __name__ == "__main__":
    start_client()
