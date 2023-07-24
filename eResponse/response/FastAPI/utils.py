from asgiref.sync import sync_to_async
from django.contrib.auth.models import Group
from eResponse.response.models import Emergency, Brief
from eResponse.user.models import User


@sync_to_async
def start_emergency_sync(schema: dict):
    _new = {}
    emergency_type = respondents = briefs = None

    for field in schema:
        if field == "emergency_type":
            emergency_type = Group.objects.get(name=schema.get(field))
        elif field == "respondents":
            respondents = [User.objects.get(id=respondent.get(id))
                           for respondent in schema.get(field)]
        elif field == "briefs":
            briefs = [Brief.objects.get(id=brief.get(id))
                      for brief in schema.get(field)]
        else:
            _new.update(dict([(field, schema.get(field))]))

    emergency = Emergency(**_new)
    emergency.save()
    emergency.emergency_type.add(emergency_type)
    emergency.respondents.add(*respondents)
    emergency.briefs.add(*briefs)


@sync_to_async
def create_brief():
    pass
