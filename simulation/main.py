import ferry
import port
import random
import heapq


PORT_CODES = ["SWB", "TSA", "SGI", "HSB", "NAN", "LNG"]


if __name__ == "__main__":
    #Create a port object
    TSA = port.Port()
    TSA.port_code = "TSA"

    SWB = port.Port()
    SWB.port_code = "SWB"

    SGI = port.Port()
    SGI.port_code = "SGI"

    HSB = port.Port()
    HSB.port_code = "HSB"

    NAN = port.Port()
    NAN.port_code = "NAN"


    #Create a ferry object
    ferry = ferry.Ferry()
    ferry.ferry_name = "Queen of New Westminster"
    ferry.ferry_code = "QNW"
    ferry.ferry_capacity = 150
    ferry.ferry_route = [TSA.port_code, SWB.port_code, SGI.port_code, TSA.port_code]
    ferry.ferry_trip_time = {TSA.port_code + SWB.port_code: 20, 
                             SWB.port_code + SGI.port_code: 15, 
                             SGI.port_code + TSA.port_code: 25}
    ferry.ferry_departure_time = [[0, 0], [25, 0], [70, 0], [90, 0]]
    ferry.ferry_arrival_time = [[0, 0], [15, 0], [45, 0], [80, 0]]
    ferry.loading_unloading_time = {SWB.port_code + "0": 15,
                                    SGI.port_code + "0" : 10,
                                    TSA.port_code + "0": 10}
    ferry.trips_required = 1
    ferry.trips_completed = 0
    ferry.ferry_current_port_index = 0
    ferry.next_function = ferry.start_route


    current_time =0
    event_queue = []
    heapq.heapify(event_queue)
    heapq.heappush(event_queue, (current_time, ferry))
    

    current_event = heapq.heappop(event_queue)
    while current_event[1].next_function != None:
        current_time = current_event[0]

        next_event_time = current_event[1].next_function(current_time)
        heapq.heappush(event_queue, (next_event_time, current_event[1]))

        current_event = heapq.heappop(event_queue)






    



