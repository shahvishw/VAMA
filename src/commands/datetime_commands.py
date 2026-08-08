from datetime import datetime,date

def handle_datetime(intent):

    if intent == 'time':
        current_time  = datetime.now().strftime("%I:%M %p")
        return f'Current Time is {current_time}'
    elif intent == 'date':
        today = date.today().isoformat()
        return f"Today's Date is {today}"

    return "I don't understand that command."