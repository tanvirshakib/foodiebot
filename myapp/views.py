from tkinter import Canvas
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def popular_menu(request):
    return render(request, 'popular_menu.html')


def order_placed(request):
    return render(request, 'order_placed.html')

def review(request):
    return render(request, 'review.html')


def admin_page(request):
    return render(request, 'admin.html')

def manager(request):
    return render(request, 'manager.html')

def staff(request):
    return render(request, 'staff.html')

def about_restaurant(request):
    return render(request, 'about_restaurant.html')

def location(request):
    return render(request, 'location.html')



import json

# myapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category

def menu(request, category=None):
    categories = Category.objects.all()

    if category is None:
        if categories.exists():
            current_category = categories.first()
        else:
            current_category = None
    else:
        current_category = get_object_or_404(Category, name=category)

    items = MenuItem.objects.filter(category=current_category) if current_category else []

    context = {
        'categories': categories,
        'items': items,
        'current_category': current_category.name if current_category else 'No Categories Available'
    }
    return render(request, 'menu.html', context)




from django.shortcuts import render, redirect
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cart(request):
    if request.method == 'POST':
        selected_items = json.loads(request.body).get('selected_items', [])
        request.session['selected_items'] = selected_items
        print(f"Selected Items in Session (POST): {request.session['selected_items']}")  # Debug statement
    else:
        selected_items = request.session.get('selected_items', [])
        print(f"Selected Items in Session (GET): {selected_items}")  # Debug statement

    cart_items = []
    subtotal = 0

    for item in selected_items:
        name = item['name']
        price = float(item['price'])
        quantity = int(item.get('quantity', 1))
        total = price * quantity
        cart_items.append({'name': name, 'price': price, 'quantity': quantity, 'total': total})
        subtotal += total

    sales_tax = subtotal * 0.1025
    grand_total = subtotal + sales_tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'sales_tax': sales_tax,
        'grand_total': grand_total
    }
    return render(request, 'cart.html', context)









# views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import SignUpForm

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid phone number or password.')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    # Clear session data on logout
    request.session.flush()
    logout(request)
    return redirect('login')







# views.py (Order View)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomerOrder, CustomerOrderItem
from .forms import CheckoutForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CustomerOrder


login_required
def order(request):

    if not request.user.is_authenticated:
        return render(request, 'order_anonymous.html')



    user_orders = CustomerOrder.objects.filter(user=request.user).prefetch_related('items')


    # Check for messages stored in the session
    user_messages = request.session.pop('_user_messages', {})
    user_message = user_messages.get(request.user.id, None)

    context = {
        'user_orders': user_orders,
        'user_message': user_message
    }
    return render(request, 'order.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomerOrder, CustomerOrderItem
from .forms import CheckoutForm

@login_required
def checkout(request):
    selected_items = request.session.get('selected_items', [])
    order_items = []
    subtotal = 0

    if not selected_items:
        print("No selected items in session.")  # Debug statement

    for item in selected_items:
        print(f"Selected item: {item}")  # Debug statement to check session data
        name = item['name']
        price = float(item['price'])
        quantity = int(item.get('quantity', 1))
        total = price * quantity
        order_items.append({'name': name, 'price': price, 'quantity': quantity, 'total': total})
        subtotal += total

    sales_tax = subtotal * 0.1025
    grand_total = subtotal + sales_tax

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_preference = form.cleaned_data['delivery_preference']
            delivery_time = form.cleaned_data['delivery_time']
            street = form.cleaned_data['street']
            apt_number = form.cleaned_data['apt_number']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            state = form.cleaned_data['state']
            card_number = form.cleaned_data['card_number']
            card_expiry = form.cleaned_data['card_expiry']
            card_cvc = form.cleaned_data['card_cvc']

            order = CustomerOrder.objects.create(
                user=request.user,
                delivery_preference=delivery_preference,
                delivery_time=delivery_time,
                street=street,
                apt_number=apt_number,
                city=city,
                zip_code=zip_code,
                state=state,
                card_number=card_number,
                card_expiry=card_expiry,
                card_cvc=card_cvc,
                subtotal=subtotal,
                sales_tax=sales_tax,
                grand_total=grand_total
            )

            for item in order_items:
                created_item = CustomerOrderItem.objects.create(
                    order=order,
                    name=item['name'],
                    price=item['price'],
                    quantity=item['quantity'],
                    total=item['total']
                )
                print(f"Created item: {created_item}")  # Debug statement

            print(f"Order Created: {order.id} by {order.user.username} with items: {list(order.items.all())}")

            return redirect('order_placed')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'order_items': order_items,
        'subtotal': subtotal,
        'sales_tax': sales_tax,
        'grand_total': grand_total,
    }
    return render(request, 'checkout.html', context)






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from .models import Reservation

def reserve_table(request):
    if not request.user.is_authenticated:
        return render(request, 'reservation_anonymous.html')
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            request.session['reservation_id'] = reservation.id
            return redirect('reservation_success')
    else:
        form = ReservationForm()
    
    return render(request, 'reservation.html', {'form': form})

@login_required
def user_reservations(request):
    user_reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_date')
    return render(request, 'user_reservations.html', {'user_reservations': user_reservations})

def manage_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'manage_reservations.html', {'reservations': reservations})

# views.py (Manage Orders View)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CustomerOrder


def manage_orders(request):
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'active':
        all_orders = CustomerOrder.objects.filter(status='new').order_by('-order_date')
    else:
        all_orders = CustomerOrder.objects.all().order_by('-order_date')

    context = {
        'all_orders': all_orders,
        'status_filter': status_filter,
    }
    return render(request, 'manage_orders.html', context)


def update_order_status(request, order_id, status):
    order = get_object_or_404(CustomerOrder, id=order_id)
    order.status = status
    order.save()

    if status == 'rejected':
        # Store message for the user
        user_messages = request.session.get('_user_messages', {})
        user_messages[order.user.id] = f"Your order #{order.id} has been canceled."
        request.session['_user_messages'] = user_messages

    elif status == 'ready':
        # Store message for the user
        user_messages = request.session.get('_user_messages', {})
        user_messages[order.user.id] = f"Your order #{order.id} is ready for pickup."
        request.session['_user_messages'] = user_messages

    messages.success(request, f"Order #{order.id} status updated to {status}.")
    return redirect('manage_orders')

def manage_staff(request):
    return render(request, 'manage_staff.html')

@login_required
def reservation_success(request):
    reservation_id = request.session.get('reservation_id')
    if reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        return render(request, 'reservation_success.html', {'reservation': reservation})
    else:
        return redirect('reserve_table')




def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('manage_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'edit_reservation.html', {'form': form})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == "POST":
        reservation.delete()
        return redirect('manage_reservations')
    return render(request, 'confirm_delete.html', {'reservation': reservation})



# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MyUser  # Import your custom user model


def manage_users(request):
    main_admins = MyUser.objects.filter(username='tanvir_shakib')
    customer_users = MyUser.objects.exclude(username='tanvir_shakib').filter(groups__name='Customer')
    staff_users = MyUser.objects.exclude(username='tanvir_shakib').filter(groups__name__in=['Manager', 'Staff', 'Admin'])
    
    # If any user doesn't belong to any of the above groups, classify them as regular users
    regular_users = MyUser.objects.exclude(id__in=main_admins).exclude(id__in=customer_users).exclude(id__in=staff_users)

    context = {
        'main_admins': main_admins,
        'customer_users': customer_users,
        'staff_users': staff_users,
        'regular_users': regular_users,
    }
    return render(request, 'manage_users.html', context)


def edit_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.name = request.POST.get('name')
        user.phone_number = request.POST.get('phone')
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
        user.save()
        return redirect('manage_users')
    return redirect('manage_users')

def delete_user(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('manage_users')
    return redirect('manage_users')


def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = MyUser.objects.create_user(username=username, password=password)
        user.name = name
        user.phone_number = phone
        user.save()
        return redirect('manage_users')
    return redirect('manage_users')




# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Category
from .forms import MenuItemForm, CategoryForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

def admin_login(request):
    if request.method == "POST":
        password = request.POST.get('password')
        if password == "Admin12345":
            return redirect('custom_admin')
        else:
            return HttpResponse("Invalid password", status=401)
    return render(request, 'admin_login.html')


def manage_menu(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()

    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = MenuItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('manage_menu')
        elif 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('manage_menu')
    else:
        form = MenuItemForm()
        category_form = CategoryForm()

    context = {
        'categories': categories,
        'menu_items': menu_items,
        'form': form,
        'category_form': category_form
    }
    return render(request, 'manage_menu.html', context)


def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm(instance=item)

    context = {'form': form, 'item_id': item_id}
    return render(request, 'edit_menu_item.html', context)


def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('manage_menu')

    context = {'item': item}
    return render(request, 'delete_menu_item.html', context)


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = CategoryForm(instance=category)

    context = {'form': form, 'category_id': category_id}
    return render(request, 'edit_category.html', context)


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_menu')

    context = {'category': category}
    return render(request, 'delete_category.html', context)








from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, MenuItemForm, PopularMenuItemForm
from .models import Category, MenuItem, PopularMenuItem

def popular_menu(request):
    popular_items = PopularMenuItem.objects.all()
    return render(request, 'popular_menu.html', {'popular_items': popular_items})


def manage_popular_menu(request):
    popular_items = PopularMenuItem.objects.all()

    if request.method == 'POST':
        form = PopularMenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_popular_menu')
    else:
        form = PopularMenuItemForm()

    context = {
        'popular_items': popular_items,
        'form': form,
    }
    return render(request, 'manage_popular_menu.html', context)


def delete_popular_menu_item(request, item_id):
    item = get_object_or_404(PopularMenuItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('manage_popular_menu')

    context = {'item': item}
    return render(request, 'delete_popular_menu_item.html', context)




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Review
from .forms import ReviewForm

def review_list(request):
    reviews = Review.objects.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is None:
        average_rating = 0
    context = {
        'reviews': reviews,
        'average_rating': average_rating,
    }
    return render(request, 'review.html', context)

@login_required
def post_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'review_form.html', {'form': form})


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }






from django.shortcuts import render

def chatbot_view(request):
    return render(request, 'chatbot.html')
