class Port:
    def __init__(self, name: str = None, port_code: str = None, berth: int = 1):
        self.port_name: str = name
        self.port_code: str = port_code
        self.berth: int = berth
        self.berths_occupied: int = 0
        self.ferry_in_action: bool = False

        self.time_to_dock_or_undock: int = 0 #TODO: Implement time required to dock or undock

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

    def availble_to_dock(self) -> bool:
        return self.berths_occupied < self.berth

    def ferry_undocked(self) -> None:
        assert self.berths_occupied > 0, "No ferry to undock."
        assert self.ferry_in_action, "No ferry has said it was going to undock"
        self.ferry_in_action = False
        self.berths_occupied -= 1

    def ferry_undocking(self) -> int:
        assert self.berths_occupied > 0, "No ferry to undock."
        self.ferry_in_action = True
        return self.time_to_dock_or_undock

    def ferry_docked(self) -> None:
        assert self.berth - self.berths_occupied > 0, "No berths availble to dock at."
        assert self.ferry_in_action, "No ferry has said it was going to dock"
        self.ferry_in_action = False
        self.berths_occupied += 1

    def ferry_docking(self) -> int:
        assert self.availble_to_dock(), "No berths availble to dock at."
        self.ferry_in_action = True
        return self.time_to_dock_or_undock
        