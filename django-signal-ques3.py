"""
Question 3: 
    By default, do Django signals run in the same database transaction as the caller?

Answer: 
    Yes, by default, Django signals run in the same database transaction as the caller. This means that any changes made in 
    the signal handler will be part of the same transaction initiated by the calling function. If the transaction is committed 
    or rolled back, it affects both the caller and the signal handler.

    To prove this, we can modify the existing pizza ordering code to create a database transaction. We will demonstrate that 
    if an error occurs in the signal handler, it will roll back any changes made in the caller.
"""

# models.py file to store pizza-order data in database
from django.db import models

class PizzaOrder(models.Model):
    order_id = models.IntegerField()
    status = models.CharField(max_length=50)


import threading
from django.http import HttpResponse
from django.db import transaction
from django.dispatch import Signal, receiver
from .models import PizzaOrder

# Step 1: Define the custom signal
pizza_ordered = Signal()

# Step 2: Define the signal handler (receiver)
@receiver(pizza_ordered)
def pizza_ordered_handler(sender, **kwargs):
    order_id = kwargs.get('order_id')
    
    # Simulate an error to trigger rollback
    if order_id == 1234:
        raise Exception("Simulated error in signal handler.")
    
    # Normally, you'd process the order here
    print(f"Order {order_id} processed successfully.")

# Step 3: Define the view that sends the signal
def order_pizza(request):
    order_id = 1234  # Example order ID
    
    with transaction.atomic():  # Start a database transaction
        print(f"Placing pizza order in thread ID: {threading.get_ident()}")
        
        # Save the order to the database
        PizzaOrder.objects.create(order_id=order_id, status="Pending")
        
        # Send the custom signal (this will trigger the handler)
        pizza_ordered.send(sender=None, order_id=order_id)

    return HttpResponse("Pizza order attempted.")


"""
Output Explanation:

    here database commit is done before the signal handler
    signal handler throws an error 
    
    since they are on the same database transaction the database transaction will be rolled back when signal handler throws an error
    
    
"""
