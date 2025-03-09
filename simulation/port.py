class Port:
    def __init__(self, name: str = None, port_code: str = None, berth:int = 1):
        self.port_name: str = name
        self.port_code: str = port_code
        self.berth: int = berth

    def __repr__(self) -> str:
        return self.port_code

    def __add__(self, other) -> str: 
        if type(other) in [str]:
            return self.port_code + other

        if type(other) == Port: 
            return self.port_code + other.port_code

        if type(other) in [int]:
            return self.port_code + str(other)

        assert False, "Failed"