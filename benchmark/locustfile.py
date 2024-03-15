import os

from locust import FastHttpUser, task


class ApiClient(FastHttpUser):
    host = os.getenv("API_URL", "http://localhost:8000/api")

    @task
    def read_users(self):
        resp = self.client.get("/users")
        print(f"status: {resp.status}")