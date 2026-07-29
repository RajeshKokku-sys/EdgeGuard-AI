# events/event_rules.py

class EventRules:
    """
    Determines security severity
    """

    @staticmethod
    def evaluate(

        authentication,

        zone_type

    ):


        # Unknown person
        # inside restricted area

        if (

            authentication
            ==
            "UNAUTHORIZED"

            and

            zone_type
            ==
            "RESTRICTED"

        ):

            return {

                "event_type":
                    "ZONE_INTRUSION",

                "severity":
                    "CRITICAL"

            }



        # Employee entering restricted area

        if (

            authentication
            ==
            "AUTHORIZED"

            and

            zone_type
            ==
            "RESTRICTED"

        ):

            return {

                "event_type":
                    "AUTHORIZED_ENTRY",

                "severity":
                    "LOW"

            }



        return {

            "event_type":
                "PERSON_DETECTED",

            "severity":
                "INFO"

        }