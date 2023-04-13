import pytest
import requests


from Config.PropReader import propfile, PropReader
prpreader = PropReader()

'''
to run
pytest -v -s --html=reports/report.html --self-contained-html
'''


class TestDemo:
    @pytest.fixture()
    def pretest(self):
        self.key = PropReader.readProp("key")
        self.secret = PropReader.readProp("secret")

        self.discog_url = PropReader.readProp("url")
        self.auth = "Discogs key={}, secret={}".format(self.key, self.secret)
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": self.auth
        }

    @pytest.mark.usefixtures("pretest")
    def test_authorize_search(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)
        assert res.status_code == 200
        assert "results" in res.json()

    @pytest.mark.usefixtures("pretest")
    def test_bad_credentials(self):
        bad_auth = "Discogs key=BAD_KEY, secret=BAD_SECRET"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": bad_auth
        }
        res = requests.get("{}/search".format(self.discog_url), headers=headers)
        assert res.status_code != 200

    @pytest.mark.usefixtures("pretest")
    def test_default_pagination(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)
        assert res.status_code == 200
        assert len(res.json()["results"]) == 50

    @pytest.mark.usefixtures("pretest")
    def test_specific_pagination(self):
        params = {
            "q": "Vinyl",
            "per_page": 10
        }
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers, params=params)
        assert res.status_code == 200
        assert len(res.json()["results"]) == 10

    @pytest.mark.usefixtures("pretest")
    def test_max_pagination(self):
        params = {
            "q": "Vinyl",
            "per_page": 10000
        }
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers, params=params)
        assert res.status_code == 200
        assert len(res.json()["results"]) <= 1000
