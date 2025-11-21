from .models import Wishlist 


def wishlist_count(request):
    wishlist_total = 0
    if request.user.is_authenticated:
        try:
            wishlist_total = Wishlist.objects.filter(user=request.user).count()
        except Exception as e:
            print(f"Error calculating wishlist count: {e}") 
    return {
        'wishlist_total': wishlist_total
    }