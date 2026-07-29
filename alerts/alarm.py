import logging


logger = logging.getLogger("EdgeGuard")


class AlarmManager:
    """
    Controls physical alarm system.

    Future:
    - GPIO
    - Relay
    - Siren
    """


    def __init__(self):

        self.active = False



    def trigger(
        self,
        event
    ):


        if event.severity == "CRITICAL":


            self.active = True


            logger.warning(
                f"""
                🚨 ALARM TRIGGERED

                Event:
                {event.event_type}

                Person:
                {event.person_name}

                Zone:
                {event.zone_name}
                """
            )



    def reset(self):

        self.active = False


        logger.info(
            "Alarm reset"
        )