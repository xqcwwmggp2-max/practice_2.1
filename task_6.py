import struct

FILENAME = "practice_2.1/resource/data.bin"

HEADER_FORMAT = "<4sHI"
RECORD_FORMAT = "<QIhB"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)

def count_active_flags(flag_byte):
    return bin(flag_byte).count("1")

def create_test_file(filename):
    signature = b"DATA"
    version = 1
    records = [
        (1710000000, 1001, 2350, 0b00000011),
        (1710000600, 1002, 1875, 0b00000101),
        (1710001200, 1003, 3010, 0b00001111),
    ]

    with open(filename, "wb") as f:
        f.write(struct.pack(HEADER_FORMAT, signature, version, len(records)))
        for record in records:
            f.write(struct.pack(RECORD_FORMAT, *record))

def parse_file(filename):
    with open(filename, "rb") as f:
        header_data = f.read(HEADER_SIZE)
        if len(header_data) != HEADER_SIZE:
            print("Ошибка: файл слишком короткий.")
            return

        signature, version, record_count = struct.unpack(HEADER_FORMAT, header_data)

        if signature != b"DATA":
            print("Ошибка: неверная сигнатура файла.")
            return

        print("Сигнатура:", signature)
        print("Версия:", version)
        print("Кол-во записей:", record_count)

        temperatures = []
        active_flags_total = 0

        for i in range(record_count):
            record_data = f.read(RECORD_SIZE)
            if len(record_data) != RECORD_SIZE:
                print("Ошибка: файл обрывается на записи", i + 1)
                break

            timestamp, record_id, temp_raw, state_flag = struct.unpack(RECORD_FORMAT, record_data)
            temperature = temp_raw / 100

            temperatures.append(temperature)
            active_flags_total += count_active_flags(state_flag)

            print(
                f"Запись {i + 1}: "
                f"timestamp={timestamp}, id={record_id}, "
                f"temperature={temperature:.2f}°C, flag={state_flag:08b}"
            )

        if temperatures:
            avg_temp = sum(temperatures) / len(temperatures)
            print("\nСтатистика:")
            print(f"Ср. температура: {avg_temp:.2f}°C")
            print(f"Кол-во активных флагов: {active_flags_total}")

if __name__ == "__main__":
    create_test_file(FILENAME)
    parse_file(FILENAME)