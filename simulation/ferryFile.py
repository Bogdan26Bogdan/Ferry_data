from typing import List, Dict, Callable, Type
from port import Port
import numpy 

class Ferry:
    AT_PORT = 1
    ON_ROUTE = 2

    def __init__(self):
        self.ferry_name: str = None
        self.ferry_code: str = None
        self.ferry_capacity: int = None
        self.ferry_route: List[Type[Port]] = None  # [Port, Port, ...] ; home port is the first port
        self.ferry_current_port_index: int = 0  # The index of the last port the ferry was at
        self.ferry_trip_time: Dict[str, int] | numpy.array = None  # {port_code + port_code: trip time}
        self.ferry_departure_time: List[List[int]] | numpy.array = None  # [[scheduled, actual], [scheduled, actual], ...]
        self.ferry_arrival_time: List[List[int]] = None  # [[scheduled, actual], [scheduled, actual], ...]
        self.loading_unloading_time: Dict[str, int] = (
            None  # {port_code + (current time to the nearest 5): loading and loading time}
        )
        self.trips_required: int = None
        self.trips_completed: int = None
        self.next_function: Callable[[int], int] = self.start_route
        self.print_stats_at_end: bool = True

        # TODO: Implement these: just to pay special attention
        self.shift_change_trip: int = None  # Register a shift change to happen after n trips
        self.shift_change_time: List[float] = None  # [schdeuled shift change time, actual shift change time]

        #TODO: Seed for random so that way results can stay consistent across runs
        self.seed: int = None  # Seed for random number generation


    def get_sailing_time(self, current_time: int) -> int: 
        #TODO: implement current time into this maybe
        #Route code
        route_code = self.ferry_route[self.ferry_current_port_index].port_code + self.ferry_route[
            self.ferry_current_port_index + 1
        ].port_code
        if type(self.ferry_trip_time) is dict: 
            # Get the sailing time from the dictionary
            sailing_time = self.ferry_trip_time[route_code]
        else:
            # get the sailing time from the array according to which route we are taking
            sailing_time = numpy.random.choice(self.ferry_trip_time[route_code])

        return sailing_time 

    def get_loading_unloading_time(self, current_time: int) -> int:
        current_port = self.ferry_route[self.ferry_current_port_index].port_code

        if type(self.loading_unloading_time) is dict:
            # Get the loading and unloading time from the dictionary
            load_unload_time = self.loading_unloading_time[current_port + str(5 * round(current_time / 5))]
        else: 
            # Get a random loading and unloading time from the array
            load_unload_time = numpy.random.choice(self.loading_unloading_time[current_port])
        
        return load_unload_time


    def leave_port(self, current_time: int) -> int:
        # Check if the ferry is early and should wait until
        # the scheduled departure time
        if (
            current_time
            < self.ferry_departure_time[
                self.ferry_current_port_index + (self.trips_completed * (len(self.ferry_route) - 1))
            ][0]
        ):
            self.next_function = self.leave_port
            return self.ferry_departure_time[
                self.ferry_current_port_index + (self.trips_completed * (len(self.ferry_route) - 1))
            ][0]

        # set the actual time the ferry leaves
        self.ferry_departure_time[self.ferry_current_port_index + (self.trips_completed * (len(self.ferry_route) - 1))][
            1
        ] = current_time

        self.next_function = self.arrive_port
        return (
            current_time
            + self.get_sailing_time(current_time)  # sailing time to the next port
        )

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
        current_port = self.ferry_route[self.ferry_current_port_index]
        load_and_unload_time = self.get_loading_unloading_time(current_time)
        return current_time + load_and_unload_time

    def start_route(self, current_time) -> int:
        assert current_time <= self.ferry_departure_time[0][0]

        self.next_function = self.leave_port
        return self.ferry_departure_time[0][0]  # Leave at the scheduled time

    def end_route(self, current_time) -> None:
        assert self.trips_completed == self.trips_required
        self.print_and_calculate_stats(current_time)
        self.next_function = None
        return

    def print_and_calculate_stats(self, current_time=None) -> None:
        if self.print_stats_at_end:
            if current_time is not None:
                print(f"{self.ferry_code} has completed their trip at time {current_time}.")

            # Combined late time on arrivals and departures
            late_time = self.sum_late(self.ferry_arrival_time)
            print(f"Total time with the ferry being late to arrive: {late_time}")

            late_time = self.sum_late(self.ferry_departure_time)
            print(f"Total time with the ferry being late to depart: {late_time}")

            time_to_be_late = 10
            times_late_on_arrival = sum([1 for i in self.ferry_arrival_time if i[1] - i[0] > time_to_be_late])
            print(f"Total times more then {time_to_be_late} increments later then scheduled: {times_late_on_arrival}")

            # The total amount of times the ferry was late at all
            ferry_late_arrival = sum([1 for i in self.ferry_arrival_time if i[1] - i[0] > 0])
            print(f"The total amount of times the ferry was late at all: {ferry_late_arrival}")

    def total_times_late(self, time_to_qualify_as_late: int) -> List[int]:
        """Returns the total amount of times late to arrive and depart,
        a arrival or departure counts as late if they arrived or departed time_to_qualify_as_late
        later then the scheduled"""

        arrival_lates = sum([1 for i in self.ferry_arrival_time if i[1] - i[0] > time_to_qualify_as_late])
        departure_lates = sum([1 for i in self.ferry_departure_time if i[1] - i[0] > time_to_qualify_as_late])

        return [arrival_lates, departure_lates]

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
        if self.trips_required <= 0:
            print("The ferry must make at least one trip.")
            return False

        if len(self.ferry_departure_time) != len(self.ferry_arrival_time):
            print("The ferry must have the same number of departure and arrival times.")
            return False

        if len(self.ferry_departure_time) != (len(self.ferry_route) - 1) * self.trips_required + 1:
            print("The ferry must have the same number of departure times as the number of legs * trips.")
            return False
