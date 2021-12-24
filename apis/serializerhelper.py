from .models import *


def CalculateOfferPercentage(product):
    offer=Offer.objects.filter(product=product)
    if offer.exists():
        offPrice=product.price-offer.first().offerPrice
        percentage=(product.price-offPrice)*100/product.price
        return str(int(percentage))+'%'
    return 0