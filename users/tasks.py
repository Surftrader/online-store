from celery import shared_task
import time

@shared_task
def send_newsletter_email(email):
    # Simulate long-term work (for example, connecting to a mail server)
    print(f"--- Preparing to send newsletter email to {email}---")
    time.sleep(10)
    print(f"--- Newsletter email sent to {email}! ---")
    
    return f"Success: {email}"
