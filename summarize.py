#!/bin/python3

import math
import os
import random
import re
import sys
import json


#
# Complete the 'summarize' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING inputJSON as parameter.
#

class Transaction:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount

        # pending = True, settled = False
        self.pending = True

        self.auth_time = -1
        self.settled_time = -1

        
def summarize(inputJSON):
    data = inputJSON
    # Write your code here
    # data = json.loads(inputJSON)
    summary = ""
    available_credit = data["creditLimit"]
    payable_balance = 0

    txns = []

    for event in data["events"]:

        event_type = event["eventType"]
        event_time = event["eventTime"]
        id = event["txnId"]

        if event_type == "TXN_AUTHED":
            amount = event["amount"]

            txn = Transaction(id, amount)
            txn.pending = True
            txn.auth_time = event_time


            if amount <= available_credit:
                available_credit -= amount
            else:
                summary += "Not enough available credit for this transaction"
                return summary
            
            txns.append(txn)
        
        elif event_type == "TXN_AUTH_CLEARED":

            txns_new = txns[:]

            for txn in txns:
                if txn.id == id:
                    available_credit += txn.amount
                    txns_new.remove(txn)
                    break
                    
            txns = txns_new

        elif event_type == "TXN_SETTLED":
            amount = event["amount"]

            for txn in txns:
                if txn.id == id:
                    available_credit += txn.amount
                    txn.amount = amount
                    available_credit -= txn.amount

                    payable_balance += txn.amount

                    txn.pending = False
                    txn.settled_time = event_time

                    break

        elif event_type == "PAYMENT_INITIATED":

            amount = event["amount"]

            txn = Transaction(id, amount)
            txn.auth_time = event_time
            txn.pending = True
            
            payable_balance += amount

            txns.append(txn)

        elif event_type == "PAYMENT_CANCELED":

            txns_new = txns[:]

            for txn in txns:
                if txn.id == id:
                    payable_balance -= txn.amount
                    txns_new.remove(txn)
                    break

            txns = txns_new

        elif event_type == "PAYMENT_POSTED":

            for txn in txns:
                if txn.id == id:
                    available_credit -= txn.amount

                    txn.pending = False
                    txn.settled_time = event_time                
                    
    pending_txns = [txn for txn in txns if txn.pending]
    settled_txns = [txn for txn in txns if not txn.pending]

    summary += "Available credit: $" + str(available_credit) + "\n"
    summary += "Payable balance: $" + str(payable_balance) + "\n" + "\n"
    summary += "Pending transactions:\n"


    pending_txns.sort(key= lambda x: int(x.auth_time), reverse=True)
    settled_txns.sort(key= lambda x: int(x.auth_time), reverse=True)


    for txn in pending_txns[::-1]:
        if txn.amount >= 0:
            s = "{}: ${} @ time {} \n".format(txn.id, txn.amount, txn.auth_time)
        else:
            s = "{}: -${} @ time {} \n".format(txn.id, -txn.amount, txn.auth_time)
        summary += s
    summary += "\n"
    summary += "Settled transactions:\n"
    for txn in settled_txns[0:3]:
        if txn.amount >= 0:
            s = "{}: ${} @ time {} (finalized @ time {}) \n".format(txn.id, txn.amount, txn.auth_time, txn.settled_time)
        else:
            s = "{}: -${} @ time {} (finalized @ time {}) \n".format(txn.id, -txn.amount, txn.auth_time, txn.settled_time)           
        summary += s
    
    summary = summary.strip()
    return summary

