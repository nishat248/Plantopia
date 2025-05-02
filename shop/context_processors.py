from .models import Category
from .models import Profile, AdminProfile


def categories_processor(request):
    # Only top-level categories (like "Plants", "Seeds", etc.)
    return {
        'categories': Category.objects.filter(parent__isnull=True)
    }



def profile_processor(request):
    user = request.user
    profile = None

    if user.is_authenticated:
        if user.is_staff:
            # Admin pages, client code can use profile.admin_title, etc.
            profile = getattr(user, 'adminprofile', None)
        else:
            # Your custom users—just as before
            profile = getattr(user, 'profile', None)

    return {'profile': profile}

