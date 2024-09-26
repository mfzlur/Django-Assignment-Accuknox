"""Question 1: Are Django signals executed synchronously or asynchronously by default?

Answer: Django signals are executed synchronously by default. This means that the code in the signal handlers runs immediately after the signal is triggered, and the calling function will wait until the signal handlers have completed before continuing.
Code Snippet:

Here’s a simple example that demonstrates synchronous execution:"""

import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Define a signal handler that introduces a delay
@receiver(post_save, sender=User)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal handler started.")
    time.sleep(5)  # Simulate a delay (blocking for 5 seconds)
    print("Signal handler finished.")

# Simulate saving a user (which triggers the signal)
def create_user():
    print("Creating user...")
    user = User(username="test_user")
    user.save()  # This triggers the post_save signal
    print("User created.")

if __name__ == "__main__":
    create_user()

"""Output Explanation:

    When create_user() is called, it saves the user and triggers the post_save signal.
    The signal handler my_signal_handler runs synchronously, causing the entire process to block for 5 seconds before printing "User created.""""
