
import random
import arrow
from json import dump

class TransactionFactory():

    def __init__(self):
        pass

    def mock_transactions(self):
        random.seed(42)
        transactions = []
        for i in range(-20, 0):
            value = round(random.uniform(5,100), 4)
            commission = round(value * random.uniform(0, 0.5), 4)
            
            transactions.append({
                'id': i + 21,
                'program_id': random.choice((1, 2)),
                'date': arrow.utcnow().replace(days=i).format('YYYY-MM-DD HH:mm:ss'),
                'value': value,
                'commission': commission
            })
        return transactions

    def get_mock_transactions(self):
        transactions = self.mock_transactions()
        with open('storage/transactions.json', 'w') as outfile:
            dump(transactions, outfile)