import time


class EventDeduplicationManager:
    """
    Prevents duplicate events
    """


    def __init__(
        self,
        cooldown_seconds=10
    ):

        self.cooldown = cooldown_seconds

        self.events = {}



    def should_create_event(

        self,

        track_id

    ):


        current_time = time.time()


        if track_id not in self.events:

            self.events[track_id] = current_time

            return True



        previous_time = self.events[track_id]



        if (

            current_time
            -
            previous_time

            >
            self.cooldown

        ):


            self.events[track_id] = current_time

            return True



        return False