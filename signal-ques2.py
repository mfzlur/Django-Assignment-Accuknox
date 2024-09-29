"""
Question 1: 
    Are Django signals executed synchronously or asynchronously by default?

Answer: 
    Django signals are executed synchronously by default. This means that the code in the signal handlers runs immediately 
    after the signal is triggered, and the calling function will wait until the signal handlers have completed before continuing.
    Code Snippet:

Here’s a simple example that demonstrates synchronous execution for a pizza delivery
"""

# Step 1: Define the custom signal
pizza_ordered = Signal()

# Step 2: Define the signal handler (receiver)
@receiver(pizza_ordered)
def pizza_ordered_handler(sender, **kwargs):
    print("Signal handler started.")
    time.sleep(10)  # Simulate a delay to show the synchronous behavior
    order_id = kwargs.get('order_id')
    print(f"Signal handler finished. Order {order_id} is complete.")

# Step 3: Define the view that sends the signal
# this view is invoked when user goes to the url /order-pizza
def order_pizza(request):
    start_time = time.time()  # Start timing to measure total time

    print("Placing pizza order...")

    # Send the custom signal (this will trigger the handler synchronously)
    pizza_ordered.send(sender=None, order_id=randint(1,1000))

    end_time = time.time()  # Stop timing after the signal handler finishes

    total_time = end_time - start_time
    return HttpResponse(f"Pizza order completed in {total_time:.2f} seconds.")


# urls.py file

urlpatterns = [
    path('order-pizza/', order_pizza),
]



"""
Output Explanation:

    when order-pizza function is invoked fromt the browser
    custom signal pizza_ordered will be created by the signla handler pizza_ordered_handler
    the order-pizza view will have to wait for the signal handler to finish then only httpResponse will be returned
    as this runs asynchronously

so output should be
    Placing pizza order...
    Signal handler started.
    < time.sleep for 10s >
    Signal handler finished. Order <order_id> is complete.
    < HttpResponse(f"Pizza order completed in {total_time:.2f} seconds.") >

    
""""



"""
Question 2: 
    Do Django signals run in the same thread as the caller?

Answer: 
    Yes, Django signals run in the same thread as the caller by default. This means that the signal handlers execute in the 
    same thread that triggered the signal.


Here’s an example that demonstrates this:

"""

import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Define a signal handler that prints the current thread
@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal handler is running in thread: {threading.current_thread().name}")

# Simulate saving a user (which triggers the signal)
def create_user():
    print(f"Creating user in thread: {threading.current_thread().name}")
    user = User(username="test_user")
    user.save()  # This triggers the post_save signal

if __name__ == "__main__":
    create_user()

Output Explanation:

    The output will show that both the creation of the user and the signal handler are running in the same thread (e.g., MainThread), confirming that signals execute in the same thread as the caller.

Question 3: Do Django signals run in the same database transaction as the caller?

Answer: Yes, by default, Django signals run in the same database transaction as the caller. If the signal is triggered during a database transaction, the signal handlers will also be executed within that transaction.
Code Snippet:

Here’s an example that demonstrates this behavior:

python

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Define a signal handler that raises an exception
@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal handler started.")
    # Raise an exception to test transaction rollback
    raise ValueError("Intentional Error")

# Simulate saving a user (which triggers the signal)
def create_user():
    print("Creating user...")
    try:
        with transaction.atomic():  # Start a transaction
            user = User(username="test_user")
            user.save()  # This triggers the post_save signal
            print("User created.")
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    create_user()

Output Explanation:

    When the create_user() function is called, it tries to save a user and triggers the signal handler.
    The signal handler raises a ValueError, which causes the transaction to roll back, meaning the user will not be created.
    The output will show that the user was not created due to the exception raised in the signal handler.
