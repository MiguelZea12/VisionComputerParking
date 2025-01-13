from threading import Lock

class ParkingState:
    def __init__(self):
        self.occupied_spaces = 0
        self.free_spaces = 12
        self.historical_data = []
        self.area_status = {f"A{i+1}": False for i in range(12)} 
        self.lock = Lock()

    def update_state(self, occupied, free, area_status):
        with self.lock:
            self.occupied_spaces = occupied
            self.free_spaces = free
            self.historical_data.append(occupied)
            if len(self.historical_data) > 10:
                self.historical_data.pop(0)
            self.area_status = area_status

    def get_state(self):
        with self.lock:
            return {
                "occupied": self.occupied_spaces,
                "free": self.free_spaces,
                "historical": self.historical_data,
                "area_status": self.area_status,
            }

