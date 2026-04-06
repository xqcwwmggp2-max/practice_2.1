def rotl8(x, n=2):
    x &= 0xFF
    return ((x << n) | (x >> (8 - n))) & 0xFF

def rotr8(x, n=2):
    x &= 0xFF
    return ((x >> n) | (x << (8 - n))) & 0xFF

def encrypt_file(input_file, output_file, key):
    key &= 0xFF
    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        data = fin.read()
        encrypted = bytes([rotl8(byte, 2) ^ key for byte in data])
        fout.write(encrypted)

def decrypt_file(input_file, output_file, key):
    key &= 0xFF
    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        data = fin.read()
        decrypted = bytes([rotr8(byte ^ key, 2) for byte in data])
        fout.write(decrypted)

def main():
    print("1 - Шифровать")
    print("2 - Дешифровать")
    choice = input("Выбери действие: ").strip()

    input_file = "practice_2.1/resource/input.bin"
    output_file = "practice_2.1/resource/output.bin"

    key = int(input("Введи ключ (0-255): ").strip())

    if choice == "1":
        encrypt_file(input_file, output_file, key)
        print("Файл зашифрован.")
    elif choice == "2":
        decrypt_file(input_file, output_file, key)
        print("Файл расшифрован.")
    else:
        print("Неверный выбор.")

if __name__ == "__main__":
    main()