from samj.models import CallForwardingRecords
def getDestination(query):
    try:
        dest = CallForwardingRecords.objects.values('destination_id').get(calledNumber=query)
        return dest["destination_id"]
    except CallForwardingRecords.DoesNotExist:
        dest = "Error"
        return dest