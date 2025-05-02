from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import cart_view

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('search/', views.search, name='search'),


    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Cart

    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),



    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.popup_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Account
    path('account/profile/', views.account_details, name='account_details'),

    #path('account/update-details/', views.update_profile_details, name='update_profile_details'),
    path('account/update-picture/', views.update_profile_picture, name='update_profile_picture'),
    #path('account/change-password/', views.change_password, name='change_password'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Category and Product
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Orders
    path('order-now/<int:product_id>/', views.order_now, name='order_now'),
    path('order-summary/', views.order_summary_view, name='order_summary'),  # For cart flow
    path('order-summary/<int:order_id>/', views.order_summary_view, name='order_summary'),  # For order-now flow
    
    
    path('confirm-order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    path('cancelled-orders/', views.cancelled_orders, name='cancelled_orders'),


    # Reviews
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),


    #Blog
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),





]
