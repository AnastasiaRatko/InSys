from States import IdleState, MovingDownState, MovingUpState

class Elevator:
    def __init__(self, floor):
        self.state = IdleState()
        self.current_floor = floor
        self.requests = []

    def call_elevator(self, call_floor):
        self.state.call_elevator(self, call_floor)

    def open_doors(self):
        print(f"Двери лифта открыты на этаже {self.current_floor}.")

    def close_doors(self):
        print(f"Двери лифта закрыты.")

    def move(self, target_floor):
        distance = abs(target_floor - self.current_floor)
        print(f"Лифт движется на этаж {target_floor}. Пройденное расстояние: {distance} этажей.")
        self.current_floor = target_floor
        self.open_doors()
        self.state = IdleState()

    def get_moving_state(self, call_floor):
        states = {
            True: MovingUpState(),
            False: MovingDownState()
        }
        return states[call_floor > self.current_floor]
