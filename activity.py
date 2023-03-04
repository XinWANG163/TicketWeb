from models import Ticket
import random

class ticketNumber():
    def getNumber():
        while True:
            suffix = ""
            for i in range(16):
                suffix = suffix + str(random.randint(0,9))
            test = Ticket.query.filter_by(ticketCode=suffix).all()
            if not test:
                break
        return suffix    
            