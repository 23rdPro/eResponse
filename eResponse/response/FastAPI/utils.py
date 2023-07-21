from asgiref.sync import sync_to_async


@sync_to_async
def start_emergency_sync(schema: dict):
    for field in schema:
        if isinstance(schema[field], list):
            pass

