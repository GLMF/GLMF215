class Timer:

    def __init__(self, start_time=0):
        self._time = start_time

    def get_elapsed_time(self, time):
        result = time - self._time 
        self._time = time
        return result

    def isDuration(self, seconds, time):
        if (time - self._time) >= (seconds * 1000):
            self._time = time
            return True
        return False
