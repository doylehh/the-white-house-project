from locust import HttpUser, task, between

HOST = "https://www.whitehouse.gov"


class GetRequestsUser(HttpUser):
    wait_time = between(1, 3)
    host = HOST

    @task(10)
    def get_home(self):
        self.client.get("/")

    @task(8)
    def get_news(self):
        self.client.get("/news/")

    @task(5)
    def get_gallery(self):
        self.client.get("/gallery/")

    @task(5)
    def get_contact(self):
        self.client.get("/contact/")

    @task(4)
    def get_live(self):
        self.client.get("/live/")

    @task(3)
    def get_investments(self):
        self.client.get("/investments/")

    @task(3)
    def get_releases(self):
        self.client.get("/releases/")

    @task(2)
    def get_briefings(self):
        self.client.get("/briefings-statements/")

    @task(2)
    def get_administration(self):
        self.client.get("/administration/")

    @task(2)
    def get_presidential_actions(self):
        self.client.get("/presidential-actions/")

    @task(1)
    def get_executive_orders(self):
        self.client.get("/presidential-actions/executive-orders/")

    @task(1)
    def get_remarks(self):
        self.client.get("/remarks/")

    @task(1)
    def get_videos(self):
        self.client.get("/videos/")

    @task(1)
    def get_crypto(self):
        self.client.get("/crypto/")

    @task(1)
    def get_wire(self):
        self.client.get("/wire/")

    @task(1)
    def get_fact_sheets(self):
        self.client.get("/fact-sheets/")


class PostRequestsUser(HttpUser):
    wait_time = between(2, 5)
    host = HOST

    @task(5)
    def post_contact(self):
        self.client.post("/contact/", name="/contact/ [POST]")

    @task(2)
    def post_news(self):
        self.client.post("/news/", name="/news/ [POST]")


class PutRequestsUser(HttpUser):
    wait_time = between(2, 5)
    host = HOST

    @task(5)
    def put_home(self):
        self.client.put("/", name="/ [PUT]")

    @task(3)
    def put_news(self):
        self.client.put("/news/", name="/news/ [PUT]")

    @task(1)
    def put_nonexistent(self):
        self.client.put("/api/test-endpoint/", name="/api/test-endpoint/ [PUT]")


class PatchRequestsUser(HttpUser):
    wait_time = between(2, 5)
    host = HOST

    @task(5)
    def patch_home(self):
        self.client.patch("/", name="/ [PATCH]")

    @task(3)
    def patch_news(self):
        self.client.patch("/news/", name="/news/ [PATCH]")

    @task(1)
    def patch_nonexistent(self):
        self.client.patch("/api/test-endpoint/", name="/api/test-endpoint/ [PATCH]")
