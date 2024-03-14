import os

from locust import FastHttpUser, task, between


class ApiClient(FastHttpUser):
    host = os.getenv("API_URL", "http://127.0.0.1:8000/api")

    # connection_timeout = 60.0
    # network_timeout = 60.0
    insecure = True
    # max_redirects = 5
    max_retries = 1
    wait_time = between(3, 10)

    @task
    def read_users(self):
        self.client.get("/users")
