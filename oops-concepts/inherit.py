class BaseWorker:
    def __init__(self, worker_id: str):
        self.worker_id = worker_id

    def execute(self):
        print(f"Worker {self.worker_id} executing...")

class HTTPWorker(BaseWorker):  # Inherits from BaseWorker
    def __init__(self, worker_id: str, endpoint: str):
        super().__init__(worker_id)  # Initialize parent class
        self.endpoint = endpoint

    def fetch(self):
        print(f"Fetching data from {self.endpoint}")

worker = HTTPWorker("W1", "https://api.example.com")
worker.execute()  # Inherited method
worker.fetch()    # Child method