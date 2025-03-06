import ferryFile
import port
import numpy as np
import heapq


PORT_CODES = ["SWB", "TSA", "SGI", "HSB", "NAN", "LNG"]
SEEDS = [234,4234,324,325543,2]

if __name__ == "__main__":
    for seed_value in SEEDS:
        np.random.seed(seed_value)

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
        QNW = ferryFile.Ferry()
        QNW.ferry_name = "Queen of New Westminster"
        QNW.ferry_code = "QNW"
        QNW.ferry_capacity = 150
        QNW.ferry_route = [TSA.port_code, SWB.port_code, SGI.port_code, TSA.port_code]
        QNW.ferry_trip_time = {TSA.port_code + SWB.port_code: 17 + int(np.random.exponential(3)), 
                                SWB.port_code + SGI.port_code: 13 + int(np.random.exponential(2)), 
                                SGI.port_code + TSA.port_code: 20 + int(np.random.exponential(5))}
        QNW.set_expected_departure_times([0, 25, 70, 90])
        QNW.set_expected_arrival_times([0, 15, 45, 80])
        QNW.loading_unloading_time = {SWB.port_code + "0": int(np.random.exponential(15)),
                                        SGI.port_code + "0" : int(np.random.exponential(10)),
                                        TSA.port_code + "0": int(np.random.exponential(20))}
        QNW.trips_required = 1
        
        QNW.trips_completed = 0
        QNW.ferry_current_port_index = 0
        QNW.next_function = QNW.start_route
        QNW.validate_arrival_and_departure_times()


        current_time =0
        event_queue = []
        heapq.heapify(event_queue)
        heapq.heappush(event_queue, (current_time, QNW))
        

        current_event = heapq.heappop(event_queue)
        while current_event[1].next_function != None:
            current_time = current_event[0]

            next_event_time = current_event[1].next_function(current_time)
            heapq.heappush(event_queue, (next_event_time, current_event[1]))

            current_event = heapq.heappop(event_queue)

        print(f"Arrival times [scheduled, actual]: {QNW.ferry_arrival_time}")
        print(f"Departure times [scheduled, actual]: {QNW.ferry_departure_time}")


    



