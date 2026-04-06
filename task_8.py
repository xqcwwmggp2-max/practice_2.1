from pathlib import Path

def process_file(input_path, output_path):
    denom = 73 ** 2 + 29  # 5368

    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:

        for line in fin:
            parts = line.split()
            new_parts = []

            for item in parts:
                if item.lstrip("-").isdigit():
                    x = int(item)
                    if x % 7 == 0:
                        x = x * 100 / denom
                        new_parts.append(f"{x:.6f}")
                    else:
                        new_parts.append(item)
                else:
                    new_parts.append(item)

            fout.write(" ".join(new_parts) + "\n")

def find_multiples_of_7(input_path):
    multiples = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            for item in line.split():
                if item.lstrip("-").isdigit():
                    x = int(item)
                    if x % 7 == 0:
                        multiples.append(x)

    return multiples

def main():
    input_path = input("Введи путь к входному файлу: ").strip()
    output_path = input("Введи путь к выходному файлу: ").strip()

    multiples = find_multiples_of_7(input_path)
    print("Числа, кратные 7:", multiples)

    process_file(input_path, output_path)
    print("Файл обработан и сохранён.")

if __name__ == "__main__":
    main()