import json



class PointsData():
    def __init__(self, usr_id: int, group_id: int):
        self.usr_id = usr_id
        self.group_id = group_id
        self.data = {}
        
    def update_points(self, points: int):
        """Update the points for the given user and group."""
        with open("/home/sa/points_data.json", "r") as f:
            self.data = json.load(f)
        with open("/home/sa/bread_data.json", "r") as f:
            bread_data = json.load(f)
        if str(self.usr_id) not in bread_data[group_id].keys(): # type: ignore
            raw = 1
        else:
            raw = 1 + bread_data[group_id][str(self.usr_id)]["level"]/20 # type: ignore
        key = (self.usr_id, self.group_id)
        if key in self.data:
            self.data[key] += points*raw
        else:
            self.data[key] = points*raw
        with open("/home/sa/points_data.json", "w") as f:
            json.dump(self.data, f)
            
    def get_points(self) -> float:
        """Retrieve the points for the given user and group."""
        with open("/home/sa/points_data.json", "r") as f:
            self.data = json.load(f)
        key = (self.usr_id, self.group_id)
        if key not in self.data:
            self.data[key] = 0
        with open("/home/sa/points_data.json", "w") as f:
            json.dump(self.data, f)
        return self.data[key]