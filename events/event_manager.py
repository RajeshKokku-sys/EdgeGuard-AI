from events.event_model import SecurityEvent

from events.event_rules import EventRules


class EventManager:
    """
    Creates intelligent security events
    """


    def __init__(self):

        self.rules = EventRules()



    def create_event(

        self,

        camera,

        person,

        zone,

        confidence,

        track_id

    ):


        authentication = (

            "AUTHORIZED"

            if

            person["identity"]["authorized"]

            else

            "UNAUTHORIZED"

        )



        decision = EventRules.evaluate(

            authentication,

            zone["zone_type"]

        )



        event = SecurityEvent(

            camera=camera,

            track_id=track_id,

            person_name=

                person["identity"]["name"],


            authentication=

                authentication,


            zone_name=

                zone["zone_name"],


            event_type=

                decision["event_type"],


            confidence=

                confidence,


            severity=

                decision["severity"]

        )


        return event