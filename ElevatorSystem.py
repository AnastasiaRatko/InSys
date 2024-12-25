from Elevator import Elevator

class ElevatorSystem:
    def __init__(self, firstFloor, secondFloor):
        self.elevators = [Elevator(firstFloor), Elevator(secondFloor)]

    def find_nearest_elevator(self, call_floor):
        return min(self.elevators, key=lambda elevator: abs(elevator.current_floor - call_floor))

    def process_calls(self, calls):
        for call_floor, target_floor in calls:
            elevator = self.find_nearest_elevator(call_floor)
            elevator.call_elevator(call_floor)
            elevator.close_doors()
            elevator.move(target_floor)
            elevator.close_doors()
            print("")
