import time, json

class Time:
    def __init__(self, usr_id: int, group_id: int):
        self.usr_id = usr_id
        self.group_id = group_id
        self.timestamp = int(time.time())
    
    def check_time(self) -> bool:
        """Check if the given timestamp is on the same day as the stored timestamp."""
        local_time = time.localtime(self.timestamp)
        ckid = CheckInData(self.usr_id, self.group_id)
        user_local_time = time.localtime(ckid.get_user_data())
        
        return (local_time.tm_year == user_local_time.tm_year and
                local_time.tm_yday == user_local_time.tm_yday)
    
        
class CheckInData:
    def __init__(self, usr_id: int, group_id: int):
        self.usr_id = usr_id
        self.group_id = group_id
        self.timestamp = int(time.time())
        self.data = {}
    
    def get_user_data(self) -> int:
        """Retrieve or create a Time object for the given user and group."""
        with open("/home/sa/check_in_data.json", "r") as f:
            self.data = json.load(f)
        key = (self.usr_id, self.group_id)
        if key not in self.data:
            self.data[key] = 0
        return self.data[key]
    
    def update_check_in(self):
        """Update the check-in timestamp for the given user and group."""
        with open("/home/sa/check_in_data.json", "r") as f:
            self.data = json.load(f)
        t = Time(self.usr_id, self.group_id)
        key = (self.usr_id, self.group_id)
        if key in self.data:
            self.data[key] = self.timestamp
        else:
            self.data[key] = self.timestamp
        with open("/home/sa/check_in_data.json", "w") as f:
            json.dump(self.data, f)
        
        