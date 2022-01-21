from .models import *


def CalculateOfferPercentage(offerprice,actualprice):
    if offerprice==0 or actualprice==0:
        return 0
    offprice=actualprice-offerprice
    percentage=offprice*100/actualprice
    return str(int(percentage))+'%'