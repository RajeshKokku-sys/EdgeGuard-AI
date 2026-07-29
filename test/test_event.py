from events.event_manager import EventManager


manager = EventManager()


person = {

    "identity":{

        "name":"Unknown",

        "authorized":False

    }

}


zone = {

    "zone_name":"Vault",

    "zone_type":"RESTRICTED"

}



event = manager.create_event(

    camera="Main Entrance",

    person=person,

    zone=zone,

    confidence=0.96,

    track_id=5

)


print(
    event.to_dict()
)