from .models import Cart

def cart_quantity(request):
  totalitem = 0
    
  if request.user.is_authenticated:
    user = request.user
    totalitem = len(Cart.objects.filter( user=user ))
    return {'totalitem':totalitem}
  else:
    return {}