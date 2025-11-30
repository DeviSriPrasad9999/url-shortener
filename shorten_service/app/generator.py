import random
import string

def generate_code(length: int=7):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
