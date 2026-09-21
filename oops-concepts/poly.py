class EmailNotifier:
    def notify(self, message: str):
        print(f"Sending Email: {message}")

class SMSNotifier:
    def notify(self, message: str):
        print(f"Sending SMS: {message}")

def send_alert(notifier, message: str):
    # Polymorphic call: accepts any object that has a notify() method
    notifier.notify(message)

send_alert(EmailNotifier(), "System rebooting")
send_alert(SMSNotifier(), "System rebooting")