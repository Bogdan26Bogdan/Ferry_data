from typing import List, Dict, Callable, Type 
from port import Port

class Ferry:
    AT_PORT = 1
    ON_ROUTE = 2

    def __init__(self):
        self.ferry_name:str = None
        self.ferry_code:str = None
        self.ferry_capacity:int = None
        self.ferry_route:List[Type[Port]] = None  # [Port, Port, ...] ; home port is the first port
        self.ferry_current_port_index:int = 0  # The index of the last port the ferry was at
        self.ferry_trip_time:Dict[str,int] = None  # {port_code + port_code: trip time}
        self.ferry_departure_time:List[List[int]] = None  # [[scheduled, actual], [scheduled, actual], ...]
        self.ferry_arrival_time:List[List[int]] = None  # [[scheduled, actual], [scheduled, actual], ...]
        self.loading_unloading_time:Dict[str, int] = None  # {port_code + trip number: loading and loading time}
        self.trips_required:int = None
        self.trips_completed:int = None
        self.next_function:Callable[[int],int] = self.start_route

    def leave_port(self, current_time: int) -> int:
        # Check if the ferry is early and should wait until
        # the scheduled departure time
        if current_time < self.ferry_departure_time[self.ferry_current_port_index + (self.trips_completed * (len(self.ferry_route) - 1))][
            0
        ]:
            self.next_function = self.leave_port
            return self.ferry_departure_time[self.ferry_current_port_index + (self.trips_completed * (len(self.ferry_route) - 1))][0]

        # set the actual time the ferry leaves
        self.ferry_departure_time[self.ferry_current_port_index + (self.trips_completed * (len(self.ferry_route) - 1))][
            1
        ] = current_time

        self.next_function = self.arrive_port
        return current_time + self.ferry_trip_time[
            self.ferry_route[self.ferry_current_port_index].port_code + self.ferry_route[self.ferry_current_port_index + 1].port_code
        ]

    def arrive_port(self, current_time: int) -> int:
        # increment the current port
        self.ferry_current_port_index += 1

        # check if the ferry has completed a trip
        if self.ferry_route[self.ferry_current_port_index] == self.ferry_route[0]:
            self.trips_completed += 1
            self.ferry_current_port_index = 0

        # Set the actual time the ferry arrives
        self.ferry_arrival_time[self.ferry_current_port_index + ((len(self.ferry_route) - 1) * self.trips_completed)][
            1
        ] = current_time

        # check if the ferry has completed all trips
        if self.trips_completed == self.trips_required:
            self.next_function = self.end_route
        else:
            self.next_function = self.load_and_unload_ferry


        return current_time

    def load_and_unload_ferry(self, current_time) -> int:
        # Load and unload the ferry
        self.next_function = self.leave_port
        return (
            current_time
            + self.loading_unloading_time[self.ferry_route[self.ferry_current_port_index].port_code + str(self.trips_completed)]
        )

    def start_route(self, current_time) -> int:
        assert current_time <= self.ferry_departure_time[0][0]

        self.next_function = self.leave_port
        return self.ferry_departure_time[0][0]  # Leave at the scheduled time

    def end_route(self, current_time) -> None:
        assert self.trips_completed == self.trips_required
        print(f"{self.ferry_code} has completed their trip at time {current_time}.")
        self.print_and_calculate_stats()
        self.next_function = None
        return

    def print_and_calculate_stats(self) -> None:
        # Combined late time on arrivals and departures
        late_time = self.sum_late(self.ferry_arrival_time)
        print(f"Total time with the ferry being late to arrive: {late_time}")

        late_time = self.sum_late(self.ferry_departure_time)
        print(f"Total time with the ferry being late to depart: {late_time}")

    def sum_late(self, time_array: List[List[int]]) -> int:
        # Combined late time
        late_time = 0
        for i in range(len(time_array)):
            late_time += max(time_array[i][1] - time_array[i][0], 0)
        return late_time

    def set_expected_departure_times(self, departure_times: List[int]) -> None:
        self.ferry_departure_time = []
        for i in range(len(departure_times)):
            self.ferry_departure_time.append([departure_times[i], 0])

    def set_expected_arrival_times(self, arrival_times: List[int]) -> None:
        self.ferry_arrival_time = []
        for i in range(len(arrival_times)):
            self.ferry_arrival_time.append([arrival_times[i], 0])

    def validate_arrival_and_departure_times(self) -> bool:
        if (self.trips_required <= 0):
            print("The ferry must make at least one trip.")
            return False     
        
        if (len(self.ferry_departure_time) != len(self.ferry_arrival_time)):
            print("The ferry must have the same number of departure and arrival times.")
            return False
        
        if (len(self.ferry_departure_time) != (len(self.ferry_route) - 1) * self.trips_required + 1):
            print("The ferry must have the same number of departure times as the number of legs * trips.")
            return False
