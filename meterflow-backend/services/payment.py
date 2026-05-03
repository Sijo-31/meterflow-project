import razorpay

RAZORPAY_KEY_ID = "rzp_test_Skp6fS43Arrgof"
RAZORPAY_KEY_SECRET = "i5rg6jctdTdshAos7AaYHqmR"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
def create_order(amount : int):
    """
    Create a Razorpay order
    amount in INR - convert to paise
    """
    order =  client.order.create({
        "amount": amount * 100,  # Amount in paise
        "currency": "INR",
        "payment_capture": 1
    })
    return order
