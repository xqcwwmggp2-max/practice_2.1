class JSONError(Exception):
    pass


def serialize(obj, indent=0):
    return _serialize(obj, indent, 0)


def _serialize(obj, indent, level):
    sp = " " * indent
    cur = sp * level

    if obj is None:
        return "null"
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return '"' + obj.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(obj, list):
        if not obj:
            return "[]"
        parts = [_serialize(x, indent, level + 1) for x in obj]
        if indent:
            return "[\n" + ",\n".join((sp * (level + 1) + p for p in parts)) + "\n" + cur + "]"
        return "[" + ", ".join(parts) + "]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            key = _serialize(str(k), indent, 0)
            val = _serialize(v, indent, level + 1)
            if indent:
                items.append(f"{sp * (level + 1)}{key}: {val}")
            else:
                items.append(f"{key}: {val}")
        if indent:
            return "{\n" + ",\n".join(items) + "\n" + cur + "}"
        return "{" + ", ".join(items) + "}"
    raise JSONError(f"Неподдерживаемый тип: {type(obj)}")

def deserialize(text):
    parser = JSONParser(text)
    value = parser.parse_value()
    parser.skip_ws()
    if not parser.eof():
        parser.error("Лишние данные после JSON")
    return value


class JSONParser:
    def __init__(self, text):
        self.text = text
        self.i = 0
        self.line = 1

    def eof(self):
        return self.i >= len(self.text)

    def peek(self):
        return self.text[self.i] if not self.eof() else ""

    def get(self):
        ch = self.peek()
        self.i += 1
        if ch == "\n":
            self.line += 1
        return ch

    def skip_ws(self):
        while not self.eof() and self.peek() in " \t\r\n":
            self.get()

    def error(self, msg):
        raise JSONError(f"{msg} в строке {self.line}")

    def parse_value(self):
        self.skip_ws()
        if self.eof():
            self.error("Неожиданный конец данных")

        ch = self.peek()

        if ch == '"':
            return self.parse_string()
        if ch == "{":
            return self.parse_object()
        if ch == "[":
            return self.parse_array()
        if ch == "t":
            return self.parse_true()
        if ch == "f":
            return self.parse_false()
        if ch == "n":
            return self.parse_null()
        if ch == "-" or ch.isdigit():
            return self.parse_number()

        self.error(f"Неожиданный символ '{ch}'")

    def parse_string(self):
        if self.get() != '"':
            self.error("Ожидалась строка")
        result = []
        while not self.eof():
            ch = self.get()
            if ch == '"':
                return "".join(result)
            if ch == "\\":
                if self.eof():
                    self.error("Неверное экранирование")
                esc = self.get()
                if esc == '"':
                    result.append('"')
                elif esc == "\\":
                    result.append("\\")
                elif esc == "n":
                    result.append("\n")
                elif esc == "t":
                    result.append("\t")
                elif esc == "r":
                    result.append("\r")
                else:
                    self.error("Неподдерживаемая escape-последовательность")
            else:
                result.append(ch)
        self.error("Строка не закрыта")

    def parse_number(self):
        start = self.i
        if self.peek() == "-":
            self.get()
        while not self.eof() and self.peek().isdigit():
            self.get()
        if not self.eof() and self.peek() == ".":
            self.get()
            while not self.eof() and self.peek().isdigit():
                self.get()
            return float(self.text[start:self.i])
        return int(self.text[start:self.i])

    def parse_true(self):
        if self.text[self.i:self.i+4] != "true":
            self.error("Неверный литерал")
        self.i += 4
        return True

    def parse_false(self):
        if self.text[self.i:self.i+5] != "false":
            self.error("Неверный литерал")
        self.i += 5
        return False

    def parse_null(self):
        if self.text[self.i:self.i+4] != "null":
            self.error("Неверный литерал")
        self.i += 4
        return None

    def parse_array(self):
        if self.get() != "[":
            self.error("Ожидался символ [")
        arr = []
        self.skip_ws()
        if self.peek() == "]":
            self.get()
            return arr
        while True:
            arr.append(self.parse_value())
            self.skip_ws()
            if self.peek() == ",":
                self.get()
                continue
            if self.peek() == "]":
                self.get()
                return arr
            self.error("Ожидалась , или ]")

    def parse_object(self):
        if self.get() != "{":
            self.error("Ожидался символ {")
        obj = {}
        self.skip_ws()
        if self.peek() == "}":
            self.get()
            return obj
        while True:
            self.skip_ws()
            if self.peek() != '"':
                self.error("Ожидался строковый ключ")
            key = self.parse_string()
            self.skip_ws()
            if self.get() != ":":
                self.error("Ожидался символ :")
            value = self.parse_value()
            obj[key] = value
            self.skip_ws()
            if self.peek() == ",":
                self.get()
                continue
            if self.peek() == "}":
                self.get()
                return obj
            self.error("Ожидалась , или }")
            
def pretty_print(obj, indent=2):
    print(serialize(obj, indent))

def validate_json(text):
    try:
        deserialize(text)
        return True, "JSON корректен"
    except JSONError as e:
        return False, str(e)


if __name__ == "__main__":
    data = {
            "users": [
                {
                "id": 1,
                "name": "Alice",
                "friends": [2, 3],
                "posts": [
                    {
                    "postId": "p1",
                    "content": "Hello world",
                    "likes": [2, 3],
                    "comments": [
                        {
                        "userId": 2,
                        "text": "Hi!",
                        "timestamp": "2026-04-05T10:00:00Z"
                        }
                    ]
                    }
                ]
                },
                {
                "id": 2,
                "name": "Bob",
                "friends": [1],
                "posts": []
                }
            ]
    }

    s = serialize(data, indent=2)
    print("Серилизация:")
    print(s)

    obj = deserialize(s)
    print("\Десериализация:")
    print(obj)

    ok, msg = validate_json(s)
    print("\Валидация:")
    print(ok, msg)