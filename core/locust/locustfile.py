from locust import HttpUser, task


class BasicUser(HttpUser):
    def on_start(self):
        data = {"email": "admin@admin.com", "password": "123"}
        url = "/accounts/api/v1/jwt/create/"
        response = self.client.post(url, data).json()
        self.client.headers = {
            "Authorization": f"Bearer {response.get('access', None)}"
        }

    @task
    def post_list(self):
        url = "blog/api/v1/"
        self.client.get(url)

    @task
    def category(self):
        url = "blog/api/v1/category/"
        self.client.get(url)
