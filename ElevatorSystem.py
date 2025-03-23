from Elevator import Elevator
from States import MovingUpState
from States import MovingDownState

class ElevatorSystem:
    def __init__(self, floorForFirst, floorForSecond):
        self.elevators = [Elevator(floorForFirst), Elevator(floorForSecond)]

    def find_nearest_elevator(self, call_floor):
        def elevator_score(elevator):
            distance = abs(elevator.current_floor - call_floor)
            direction_penalty = {
                (True, False, True): 0,
                (True, False, False): 100,
                (False, True, True): 100,
                (False, True, False): 0,
                
                (False, False, True): 0,
                (False, False, False): 0
            }

            is_moving_up = isinstance(elevator.state, MovingUpState)
            is_moving_down = isinstance(elevator.state, MovingDownState)
            is_call_above = call_floor > elevator.current_floor

            penalty = direction_penalty[(is_moving_up, is_moving_down, is_call_above)]
            
            return distance + penalty

        return min(self.elevators, key=elevator_score)

    def process_calls(self, calls):
        for call_floor, target_floor in calls:
            elevator = self.find_nearest_elevator(call_floor)
            elevator.call_elevator(call_floor)
            elevator.close_doors()
            elevator.move(target_floor)
            elevator.close_doors()
            print("")

        