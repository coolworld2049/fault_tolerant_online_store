import os

from locust import FastHttpUser, task


class ApiClient(FastHttpUser):
    host = os.getenv("API_URL", "http://localhost:8000/api")

    insecure = True
    max_retries = 1

    @task
    def read_users(self):
        self.client.get("/users")
