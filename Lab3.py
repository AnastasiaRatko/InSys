from ElevatorSystem import ElevatorSystem

calls = [(5, 7), (3, 6), (2, 4), (1, 5), (7, 2), (4, 3), (6, 1), (2, 7)]
elevator_system = ElevatorSystem(1, 1)
elevator_system.process_calls(calls)
