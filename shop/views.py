from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from .models import Product, Category, Cart, Wishlist, Order, Review, Profile, OrderItem
from .forms import ProfileForm
from .models import Blog
from django.db.models import Q
from .models import Product



def home(request):
    products = Product.objects.filter(best_deal=True, availability=True)
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'home.html', {'products': products, 'categories': categories})






def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else []
    return render(request, 'search_results.html', {'products': products, 'query': query})




def popup_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
        else:
            messages.error(request, 'Invalid username or password.')
        return redirect('home')
    return redirect('home')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = request.POST
        if data.get('password1') != data.get('password2'):
            messages.error(request, 'Passwords do not match.')
            return redirect('home')

        if User.objects.filter(username=data['username']).exists():
            messages.error(request, 'Username already exists.')
            return redirect('home')

        user = User.objects.create_user(
            username=data['username'],
            email=data.get('email'),
            password=data['password1'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('home')
    return redirect('home')


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def account_details(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handling profile form
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        # Handling password change form
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'profile' in request.POST and form.is_valid():
            # Save the profile form data
            form.save()
            full_name = request.POST.get('full_name', '').strip()
            name_parts = full_name.split(' ', 1)
            request.user.first_name = name_parts[0]
            request.user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            request.user.email = request.POST.get('email', '')
            request.user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('account_details')
        
        elif 'password' in request.POST and password_form.is_valid():
            # Change password if the form is valid
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('account_details')

        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        form = ProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {
        'form': form,
        'password_form': password_form,
        'full_name': f"{request.user.first_name} {request.user.last_name}",
        'email': request.user.email,
    })


@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile = request.user.profile
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        messages.success(request, 'Profile picture updated.')
    return redirect('account_details')




def logout_view(request):
    logout(request)
    return redirect('home')


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.filter(parent__isnull=True)
    subcategories = Category.objects.filter(parent=category)
    products = None if subcategories.exists() else Product.objects.filter(category=category)
    return render(request, 'category_products.html', {
        'category': category,
        'categories': categories,
        'subcategories': subcategories if subcategories.exists() else None,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is available and in stock
    if not product.availability or product.stock < 1:
        messages.error(request, "This product is out of stock and cannot be added to the cart.")
        return redirect('product_detail', slug=product.slug)

    # Add to cart if not already added
    Cart.objects.get_or_create(user=request.user, product=product)
    return redirect('cart')


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    sub_total = sum(item.sub_total() for item in cart_items)
    total = sub_total

    order = Order.objects.filter(user=request.user, status='Pending').order_by('-id').first()
    if not order:
        order = Order.objects.create(user=request.user, status='Pending')

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'total': total,
        'order': order,
    })


@login_required
def update_cart_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if request.method == "POST":
        cart_item.delete()
    return redirect('cart')





@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')


@login_required
def order_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is available and in stock
    if not product.availability or product.stock < 1:
        messages.error(request, "This product is out of stock and cannot be ordered.")
        return redirect('product_detail', slug=product.slug)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Check if the requested quantity is available
        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} items are available in stock.")
            return redirect('product_detail', slug=product.slug)
            

        # Create an order and add the order item
        order = Order.objects.create(user=request.user)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return redirect('order_summary', order_id=order.id)

    return redirect('product_detail', slug=product.slug)



@login_required
def order_summary_view(request, order_id=None):
    
    # If order_id is provided (for single product orders), use it
    if order_id:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        # Get related items for this order
        order_items = order.items.all()

    else:
        cart = Cart.objects.filter(user=request.user)

        # Otherwise, try to get the pending order (from cart flow)
        # order = Order.objects.filter(user=request.user, status='Pending').order_by('-id').first()
        # if not order:
        order = Order.objects.create(user=request.user, status='Pending')

        # Get related items for this order
        # order_items = OrderItem.objects.create(order_id=order.id)
        for item in cart:
            # print(item)
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        
        cart.delete()

        order_items = order.items.all()
    
    print("🔍 Viewing Order Summary for Order ID:", order.id)
    print("📦 Order Items Count:", order.items.count())

    # Handle address form submission (update shipping address)
    if request.method == 'POST' and 'shipping_address' in request.POST:
        address = request.POST.get('shipping_address')
        order.shipping_address = address
        order.save()
        return redirect('order_summary', order_id=order.id if order_id else None)

    
    # Also pass user profile if needed
    profile = request.user.profile

    context = {
        'order': order,
        'order_items': order_items,
        'profile': profile,
    }
    return render(request, 'order_summary.html', context)


@require_POST
@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'Confirmed':
        return redirect('order_success')

    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        product = item.product
        if product.stock >= item.quantity:
            product.stock -= item.quantity
            if product.stock == 0:
                product.availability = False
            product.save()

    order.status = 'Confirmed'
    order.save()
    return redirect('order_success')


@login_required
def order_success(request):
    return render(request, 'order_success.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).exclude(status="Cancelled").order_by('-order_date')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != "Cancelled":
        order.status = "Cancelled"
        order.save()
        messages.success(request, "Your order has been cancelled.")
    else:
        messages.warning(request, "This order was already cancelled.")
    return redirect('my_orders')



@login_required
def cancelled_orders(request):
    cancelled_orders = Order.objects.filter(user=request.user, status='Cancelled')
    return render(request, 'cancelled_orders.html', {'orders': cancelled_orders})

    


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        Review.objects.create(
            user=request.user,
            product=product,
            rating=int(request.POST.get('rating')),
            comment=request.POST.get('comment')
        )
        messages.success(request, "Review submitted successfully!")
    return redirect('product_detail', slug=product.slug)




@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, 'my_reviews.html', {'reviews': reviews})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    messages.success(request, "Review deleted successfully.")
    return redirect('my_reviews')




def blog(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request, 'blog.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})
