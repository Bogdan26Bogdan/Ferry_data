class Port:
    def __init__(self, name: str = None, port_code: str = None, berth:int = 1):
        self.port_name: str = name
        self.port_code: str = port_code
        self.berth: int = berth