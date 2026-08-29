from locust import HttpUser, task


class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/account/api/v1/jwt/create/",
            json={"email": "newadmin@admin.com", "password": "newstring123"},
        )
        token = response.json().get("access", None)
        self.client.headers = {"Authorization": f"Bearer {token}"}

    @task
    def post_list(self):
        self.client.get("/blog/api/v1/posts/", name="/blog")
