class ElevatorState:
    def call_elevator(self, elevator, call_floor):
        raise NotImplementedError

    def open_doors(self, elevator):
        raise NotImplementedError

    def close_doors(self, elevator):
        raise NotImplementedError

    def move(self, elevator, target_floor):
        raise NotImplementedError


class IdleState(ElevatorState):
    def call_elevator(self, elevator, call_floor):
        elevator.requests.append(call_floor)
        print(f"Лифт вызван на этаж {call_floor}.")
        elevator.state = MovingState()
        elevator.move(call_floor)

    def open_doors(self, elevator):
        elevator.state = DoorsOpenState()
        elevator.open_doors()

    def close_doors(self, elevator):
        print("Двери уже закрыты.")

    def move(self, elevator, target_floor):
        elevator.move(target_floor)


class MovingState(ElevatorState):
    def call_elevator(self, elevator, call_floor):
        print("Лифт уже в движении.")

    def open_doors(self, elevator):
        print("Двери не могут быть открыты во время движения.")

    def close_doors(self, elevator):
        elevator.state = IdleState()
        elevator.close_doors()

    def move(self, elevator, target_floor):
        elevator.move(target_floor)


class DoorsOpenState(ElevatorState):
    def call_elevator(self, elevator, call_floor):
        print("Двери открыты. Пассажиры могут входить и выходить.")

    def open_doors(self, elevator):
        print("Двери уже открыты.")

    def close_doors(self, elevator):
        elevator.state = IdleState()
        elevator.close_doors()

    def move(self, elevator, target_floor):
        print("Двери должны быть закрыты перед движением.")
