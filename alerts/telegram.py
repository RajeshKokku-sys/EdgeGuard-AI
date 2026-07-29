import requests

from alerts.notification import NotificationService

from config.settings import Settings



class TelegramNotifier(
    NotificationService
):


    def send(

        self,

        event,

        image_path=None

    ):


        message = f"""

🚨 EDGEGUARD AI ALERT


Event:
{event.event_type}


Person:
{event.person_name}


Zone:
{event.zone_name}


Camera:
{event.camera}


Severity:
{event.severity}


Confidence:
{event.confidence}

"""


        url = (

            f"https://api.telegram.org/"
            f"bot{Settings.TELEGRAM_TOKEN}/"
            f"sendMessage"

        )


        data = {

            "chat_id":
                Settings.TELEGRAM_CHAT_ID,

            "text":
                message

        }


        requests.post(

            url,

            data=data

        )


        if image_path:


            self.send_image(
                image_path
            )



    def send_image(

        self,

        image_path

    ):


        url = (

            f"https://api.telegram.org/"
            f"bot{Settings.TELEGRAM_TOKEN}/"
            f"sendPhoto"

        )


        with open(
            image_path,
            "rb"
        ) as image:


            requests.post(

                url,

                data={

                    "chat_id":
                    Settings.TELEGRAM_CHAT_ID

                },

                files={

                    "photo":
                    image

                }

            )