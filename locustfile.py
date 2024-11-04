import base64
from locust import HttpUser, task
from random import randint, choice

class Web(HttpUser):
    @task
    def load(self):
        base64string = base64.b64encode(b'user:password').decode('utf-8')

        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization": "Basic %s" % base64string})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")
    
    # Define wait time
    wait_time = lambda self: randint(0, 0)
