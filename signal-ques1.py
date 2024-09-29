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


