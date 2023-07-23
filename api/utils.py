
import random
from datetime import datetime


class conversion(dict):

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def generate_receipt_num(batch_id):       
    today = datetime.now()
    serial_no = random.choice(range(00,100)) 
    print(batch_id)
    receipt_no = f'{today.year}{today.strftime("%m")}{batch_id}{serial_no}'   
    return receipt_no