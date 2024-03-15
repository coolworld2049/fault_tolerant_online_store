import os

from locust import FastHttpUser, task


class ApiClient(FastHttpUser):
    host = os.getenv("API_URL", "http://localhost:8000/api")

    connection_timeout = 60.0
    network_timeout = 60.0
    insecure = True
    max_redirects = 3
    max_retries = 1

    @task
    def read_users(self):
        self.client.get("/users")
