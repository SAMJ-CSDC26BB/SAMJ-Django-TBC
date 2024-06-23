import datetime
import logging
from samj.models import CallForwardingRecords
def getDestination(query):
    try:
        logger = logging.getLogger("samj")
        timeNow = datetime.datetime.now()
        CallForwardingRecordsAll = CallForwardingRecords.objects.all()

        filteredDateQuerySet = CallForwardingRecordsAll.filter(startDate__lt=timeNow, endDate__gt=timeNow, calledNumber=query)

        #wenn das set mehr oder weniger als eins hat -> stimmte was nicht deswegen Error -> ansonst send number
        if filteredDateQuerySet.count() == 1:
            filteredDateObject = filteredDateQuerySet[0]
            logger.debug(f"Object: {filteredDateObject}")
            return filteredDateObject.destination.destination
        else:
            logger.error("No object or multiple objects found")
            logger.debug(f"Destination: {filteredDateQuerySet}")
            return "Error"

    except CallForwardingRecords.DoesNotExist:
        dest = "Error"
        return dest