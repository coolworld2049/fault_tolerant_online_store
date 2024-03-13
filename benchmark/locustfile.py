import os

from locust import FastHttpUser, task


class ApiClient(FastHttpUser):
    host = os.getenv("API_URL", "http://127.0.0.1:8000/api")

    # some things you can configure on FastHttpUser
    # connection_timeout = 60.0
    insecure = True
    # max_redirects = 5
    max_retries = 1

    # network_timeout = 60.0

    @task
    def users(self):
        self.client.get("/users")
