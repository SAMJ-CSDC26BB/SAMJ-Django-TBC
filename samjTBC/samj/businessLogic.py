import datetime
import logging
from samj.models import CallForwarding
def getDestination(query):
    try:
        logger = logging.getLogger("samj")
        timeNow = datetime.datetime.now()
        CallForwardingAll = CallForwarding.objects.all()
        
        filteredDateQuerySet = CallForwardingAll.filter(startDate__lt=timeNow, endDate__gt=timeNow, calledNumber=query)
        
        #wenn das set mehr oder weniger als eins hat -> stimmte was nicht deswegen Error -> ansonst send number
        if filteredDateQuerySet.count() == 1:
            filteredDateObject = filteredDateQuerySet[0]
            logger.debug(f"Object: {filteredDateObject}")
            logger.debug("calledNumber: " + filteredDateObject.calledNumber.number)
            logger.debug("destination: " + filteredDateObject.destination.number)
            return filteredDateObject.destination.number
        else:
            logger.error("No object or multiple objects found")
            logger.debug(f"Destination: {filteredDateQuerySet}")
            return "Error"

    except CallForwarding.DoesNotExist:
        dest = "Error"
        return dest