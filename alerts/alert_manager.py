from alerts.alarm import AlarmManager

from alerts.telegram import TelegramNotifier



class AlertManager:
    """
    Central alert controller
    """


    def __init__(self):


        self.alarm = AlarmManager()


        self.telegram = TelegramNotifier()



    def process_alert(

        self,

        event,

        image_path=None

    ):


        if event.severity == "CRITICAL":


            # Local Alarm

            self.alarm.trigger(
                event
            )


            # Remote Notification

            self.telegram.send(

                event,

                image_path

            )



        elif event.severity == "LOW":


            print(

                "Authorized entry"

            )



        else:


            print(

                "Informational event"

            )