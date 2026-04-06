class XMLError(Exception):
    pass


def escape_xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def unescape_xml(text):
    return (
        text.replace("&apos;", "'")
        .replace("&quot;", '"')
        .replace("&gt;", ">")
        .replace("&lt;", "<")
        .replace("&amp;", "&")
    )


def serialize_node(node, indent=2, level=0):
    tag = node["tag"]
    attrs = node.get("attrs", {})
    text = node.get("text", "")
    children = node.get("children", [])

    sp = " " * (indent * level)
    attr_str = "".join(f' {k}="{escape_xml(v)}"' for k, v in attrs.items())

    if not children and not str(text).strip():
        return f"{sp}<{tag}{attr_str}/>"

    lines = [f"{sp}<{tag}{attr_str}>"]

    if str(text).strip():
        lines[-1] += escape_xml(text)

    if children:
        for child in children:
            lines.append(serialize_node(child, indent, level + 1))
        lines.append(f"{sp}</{tag}>")
    else:
        lines[-1] += f"</{tag}>"

    return "\n".join(lines)


def serialize(data, indent=2):
    return serialize_node(data, indent, 0)


class XMLParser:
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
        while not self.eof() and self.peek().isspace():
            self.get()

    def error(self, msg):
        raise XMLError(f"{msg} в строке {self.line}")

    def parse_name(self):
        start = self.i
        if self.eof() or not (self.peek().isalpha() or self.peek() in "_:"):
            self.error("Ожидалось имя тега")
        while not self.eof() and (self.peek().isalnum() or self.peek() in "_:-."):
            self.get()
        return self.text[start:self.i]

    def parse_attr_value(self):
        self.skip_ws()
        if self.get() != '"':
            self.error("Ожидалась двойная кавычка для атрибута")
        start = self.i
        while not self.eof() and self.peek() != '"':
            self.get()
        if self.eof():
            self.error("Не закрыто значение атрибута")
        value = self.text[start:self.i]
        self.get()
        return unescape_xml(value)

    def parse_attributes(self):
        attrs = {}
        while True:
            self.skip_ws()
            ch = self.peek()
            if ch in [">", "/", ""]:
                break
            name = self.parse_name()
            self.skip_ws()
            if self.get() != "=":
                self.error("Ожидался символ =")
            value = self.parse_attr_value()
            attrs[name] = value
        return attrs

    def parse_text(self):
        start = self.i
        while not self.eof() and self.peek() != "<":
            self.get()
        return unescape_xml(self.text[start:self.i]).strip()

    def parse_element(self):
        self.skip_ws()
        if self.get() != "<":
            self.error("Ожидался символ <")

        if self.peek() == "/":
            self.error("Лишний закрывающий тег")

        tag = self.parse_name()
        attrs = self.parse_attributes()

        if self.peek() == "/":
            self.get()
            if self.get() != ">":
                self.error("Ожидался символ >")
            return {"tag": tag, "attrs": attrs, "text": "", "children": []}

        if self.get() != ">":
            self.error("Ожидался символ >")

        children = []
        text_parts = []

        while True:
            self.skip_ws()
            if self.eof():
                self.error("Тег не закрыт")

            if self.peek() == "<" and self.text[self.i:self.i+2] == "</":
                self.get()
                self.get()
                end_tag = self.parse_name()
                if end_tag != tag:
                    self.error(f"Несовпадение тега: ожидался </{tag}>")
                self.skip_ws()
                if self.get() != ">":
                    self.error("Ожидался символ >")
                break

            if self.peek() == "<":
                child = self.parse_element()
                children.append(child)
            else:
                txt = self.parse_text()
                if txt:
                    text_parts.append(txt)

        return {
            "tag": tag,
            "attrs": attrs,
            "text": " ".join(text_parts).strip(),
            "children": children
        }


def deserialize(xml_text):
    parser = XMLParser(xml_text)
    result = parser.parse_element()
    parser.skip_ws()
    if not parser.eof():
        parser.error("Лишние данные после XML")
    return result


def validate_xml(xml_text):
    try:
        deserialize(xml_text)
        return True, "XML корректен"
    except XMLError as e:
        return False, str(e)


if __name__ == "__main__":
    xml_text = """
<ecommercePlatform>
    <info>
        <name>ShopMaster</name>
        <version>2.5.1</version>
        <region>EU</region>
    </info>

    <users>
        <user id="u1" status="active">
            <name>John Doe</name>
            <email>john@example.com</email>
            <addresses>
                <address type="home">
                    <city>Berlin</city>
                    <street>Main Street 1</street>
                    <zip>10115</zip>
                </address>
                <address type="work">
                    <city>Munich</city>
                    <street>Office Park 5</street>
                    <zip>80331</zip>
                </address>
            </addresses>
        </user>

        <user id="u2" status="inactive">
            <name>Alice Smith</name>
            <email>alice@example.com</email>
            <addresses>
                <address type="home">
                    <city>Hamburg</city>
                    <street>Lake Road 12</street>
                    <zip>20095</zip>
                </address>
            </addresses>
        </user>
    </users>

    <products>
        <product id="p1" category="electronics">
            <name>Laptop</name>
            <price currency="EUR">1200</price>
            <stock>15</stock>
            <attributes>
                <attribute name="brand">BrandX</attribute>
                <attribute name="ram">16GB</attribute>
            </attributes>
        </product>

        <product id="p2" category="accessories">
            <name>Mouse</name>
            <price currency="EUR">25</price>
            <stock>150</stock>
            <attributes>
                <attribute name="brand">BrandY</attribute>
            </attributes>
        </product>
    </products>

    <orders>
        <order id="o1" userId="u1" status="shipped">
            <items>
                <item productId="p1" quantity="1"/>
                <item productId="p2" quantity="2"/>
            </items>
            <total currency="EUR">1250</total>
            <shipment>
                <carrier>DHL</carrier>
                <tracking>TRACK123</tracking>
                <status>in_transit</status>
            </shipment>
        </order>

        <order id="o2" userId="u2" status="processing">
            <items>
                <item productId="p2" quantity="1"/>
            </items>
            <total currency="EUR">25</total>
        </order>
    </orders>

    <payments>
        <payment id="pay1" orderId="o1" method="card">
            <amount currency="EUR">1250</amount>
            <status>completed</status>
        </payment>
    </payments>

    <warehouse>
        <locations>
            <location id="w1">
                <city>Frankfurt</city>
                <capacity>1000</capacity>
            </location>
        </locations>

        <inventory>
            <entry productId="p1" locationId="w1">
                <quantity>15</quantity>
            </entry>
            <entry productId="p2" locationId="w1">
                <quantity>150</quantity>
            </entry>
        </inventory>
    </warehouse>

    <logs>
        <log level="INFO" time="2026-04-05T12:00:00Z">
            Order o1 shipped
        </log>
        <log level="WARN" time="2026-04-05T12:10:00Z">
            Low stock for product p1
        </log>
    </logs>
</ecommercePlatform>
""".strip()

    print("=== Валидация ===")
    ok, msg = validate_xml(xml_text)
    print(ok, msg)

    print("\n=== Десериализация ===")
    data = deserialize(xml_text)
    print(data)

    print("\n=== Сериализация ===")
    print(serialize(data, indent=2))