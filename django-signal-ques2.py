"""
Question 2: 
    Do Django signals run in the same thread as the caller?

Answer: 
    Yes, by default, Django signals run in the same thread as the caller. This means the thread that sends the signal will be 
    the same one that runs the signal handler (receiver).

    To conclusively prove this, we can modify the existing pizza ordering code to check if the thread IDs of the view (caller) 
    and the signal handler (receiver) are the same. This will confirm that they run in the same thread


Here’s an example that demonstrates this:

"""

import time
import threading
from django.http import HttpResponse
from django.dispatch import Signal, receiver
from random import randint

# Step 1: Define the custom signal
pizza_ordered = Signal()

# Step 2: Define the signal handler (receiver)
@receiver(pizza_ordered)
def pizza_ordered_handler(sender, **kwargs):
    # Get the thread ID for the signal handler (receiver)
    handler_thread_id = threading.get_ident()
    print(f"Signal handler started in thread ID: {handler_thread_id}")
    
    time.sleep(10)  # Simulate some processing delay
    
    order_id = kwargs.get('order_id')
    print(f"Signal handler finished. Order {order_id} is complete.")

# Step 3: Define the view that sends the signal
def order_pizza(request):
    # Get the thread ID for the caller (view)
    caller_thread_id = threading.get_ident()
    print(f"Placing pizza order in thread ID: {caller_thread_id}")
    
    start_time = time.time()  # Start timing to measure total time

    # Send the custom signal (this will trigger the handler synchronously in the same thread)
    pizza_ordered.send(sender=None, order_id=randint(0,1000))

    end_time = time.time()  # Stop timing after the signal handler finishes

    total_time = end_time - start_time
    return HttpResponse(f"Pizza order completed in {total_time:.2f} seconds.")

"""
Output Explanation:

    same behaviour as ques1 and handler_thread_id, caller_thread_id printed on the console should be same
    
"""
