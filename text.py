cesar = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
decrypt_msg = []
msg = "test"
newmsg = ""
for i in range(len(msg)):
    for y in range(len(cesar)):
        if msg[i] == cesar[y]:
            newmsg += cesar[y+2]

print(str(newmsg))
