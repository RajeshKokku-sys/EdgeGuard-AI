class AlarmManager:

    def __init__(self):

        self.alarm_active = False

    def trigger(self, event):

        if not self.alarm_active:

            self.alarm_active = True

            print(
                f"🚨 Alarm Triggered - "
                f"{event['camera']}"
            )

    def reset(self):

        self.alarm_active = False

        print("Alarm Reset")