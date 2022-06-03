import time


class BenchmarkTimer:
    def __init__(self) -> None:
        self.phases = {}

    def start_timer(self, phase: int) -> None:
        if phase in self.phases.keys():
            self.phases[phase]["start"] = time.perf_counter()
        else:
            self.phases[phase] = {
                "start": time.perf_counter(),
                "stop": 0,
                "label": f"Phase #{phase}",
                "frames": 0,
                "input_lag": 0.05,
            }

    def stop_timer(self, phase: int) -> None:
        self.phases[phase]["stop"] = time.perf_counter()

    def set_input_lag(self, phase: int, input_lag: float) -> None:
        self.phases[phase]["input_lag"] = input_lag

    def set_label(self, phase: int, label: str) -> None:
        if phase in self.phases.keys():
            self.phases[phase]["label"] = label
        else:
            self.phases[phase] = {"start": 0, "stop": 0, "label": label, "frames": 0}

    def count_frame(self, phase: int) -> None:
        self.phases[phase]["frames"] += 1


logo_positions = (
    # p
    [16, 46],
    [14, 46],
    [12, 46],
    [10, 46],
    [10, 51],
    [10, 53],
    [12, 53],
    [14, 53],
    [15, 52],
    [15, 50],
    [15, 47],
    # y
    [10, 57],
    [10, 65],
    [12, 59],
    [10, 64],
    [14, 63],
    [14, 60],
    [16, 61],
    # g
    [13, 75],
    [14, 73],
    [14, 70],
    [12, 68],
    [10, 70],
    [10, 74],
    [10, 77],
    [12, 77],
    [15, 77],
    [16, 75],
    [17, 72],
    [16, 69],
    # a
    [10, 82],
    [10, 85],
    [10, 87],
    [12, 88],
    [12, 84],
    [13, 82],
    [13, 88],
    [14, 80],
    [13, 88],
    [14, 83],
    [14, 86],
    [14, 88],
    [15, 90],
    # m
    [14, 93],
    [12, 93],
    [10, 93],
    [10, 96],
    [10, 100],
    [12, 100],
    [14, 100],
    [14, 101],
    [12, 101],
    [10, 102],
    [10, 105],
    [11, 107],
    [13, 107],
    [14, 107],
    # e
    [12, 110],
    [12, 112],
    [12, 114],
    [12, 116],
    [12, 118],
    [10, 118],
    [10, 115],
    [10, 113],
    [11, 111],
    [13, 111],
    [14, 113],
    [14, 115],
    [14, 117],
    [14, 119],
    # l
    [8, 123],
    [9, 123],
    [10, 123],
    [11, 123],
    [12, 123],
    [13, 124],
    [14, 124],
    [15, 126],
    # i
    [8, 129],
    [10, 129],
    [11, 130],
    [12, 129],
    [13, 130],
    [14, 129],
    # b
    [8, 135],
    [10, 136],
    [12, 135],
    [14, 136],
    [15, 137],
    [14, 139],
    [14, 141],
    [13, 143],
    [11, 143],
    [10, 141],
    [10, 139],
)
