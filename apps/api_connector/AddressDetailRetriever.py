import requests
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PresentableTransactions:
    @dataclass
    class Transaction:
        hash: str
        unixtime: int
        humanTime: datetime
        finalBalance: float
        amount: int
    
    totalTransactions: int
    address: str
    transactions: list[Transaction]
    
class AddressDetails:
    def __init__(self, hash160, address, n_tx, n_unredeemed, total_received, total_sent, final_balance, txs) -> None:
        self.hash160 = hash160
        self.address = address
        self.n_tx = n_tx
        self.n_unredeemed = n_unredeemed
        self.total_received = total_received
        self.total_sent = total_sent
        self.final_balance = final_balance
        self.txs = txs
    def __str__(self) -> str:
        return f"Hash160: {self.hash160}\n" \
                f"Address: {self.address}\n" \
                f"n_tx: {self.n_tx}\n" \
                f"n_unredeemed: {self.n_unredeemed}\n" \
                f"total_received: {self.total_received}\n" \
                f"total_send: {self.total_sent}\n" \
                f"final_balance: {self.final_balance}\n" \
                f"txs: {self.txs}\n"
    
    def toPresentableTransactions(self):
        transactions = []
        for tx in self.txs:
            delta = 0
            fromArray = filter(lambda input: input['prev_out']['addr'] == self.address , tx['inputs'])
            if fromArray:
                delta -= sum(map(lambda input: input['prev_out']['value'], fromArray))
            toArray = filter(lambda output: output['addr'] == self.address, tx['out'])
            if toArray:
                delta += sum(map(lambda output: output['value'], toArray))
            
            transactions.append(
                PresentableTransactions.Transaction(
                    hash=tx['hash'],
                    unixtime=tx['time'],
                    humanTime=datetime.fromtimestamp(tx['time']), 
                    finalBalance=tx['balance'],
                    amount=delta,
                )
            )
        return PresentableTransactions(address=self.address,
                                       totalTransactions=self.n_tx,
                                       transactions=transactions)

class AddressDetailRetriever:
    api_url = "https://blockchain.info/rawaddr/"

    @staticmethod
    def retrieve_address_details(addr, offset=0, limit=10):
        # Your API call logic here
        try:
            response = requests.get(f"{AddressDetailRetriever.api_url}/{addr}?offset={offset}&limit={limit}")
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            print(data)
            result = AddressDetails(**data)
            return result
        except requests.exceptions.RequestException as e:
            # could add retry logic
            print(f"Error retrieving balance: {e}")
            return None