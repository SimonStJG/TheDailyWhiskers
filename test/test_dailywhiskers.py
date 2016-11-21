import pytest
import random

from unittest.mock import call, mock_open, Mock

from dailywhiskers import dailywhiskers

def test_mainline(mock_requests, cat_picture, mailgun_config):

    dailywhiskers.main()
    assert mock_requests.post.mock_calls == [
        call(mailgun_config.url, 
            auth=('api', mailgun_config.api_key), 
            data={
                'html': '<h1 style="text-align: center;">dr fluffington of tunatown</h1>\n    <img style="display: block; margin: auto; width: 100%;" src="cid:cat_picxxxxxx">', 
                'subject': 'The Daily Whiskers',
                'from': mailgun_config.from_address, 
                'to': 'test_recipient1'
            }, 
            files=[("inline", ("cat_picxxxxxx", *cat_picture))]
        ),
        call().raise_for_status(),
        call(mailgun_config.url, 
            auth=('api', mailgun_config.api_key), 
            data={
                'html': '<h1 style="text-align: center;">dr fluffington of tunatown</h1>\n    <img style="display: block; margin: auto; width: 100%;" src="cid:cat_picxxxxxx">', 
                'subject': 'The Daily Whiskers',
                'from': mailgun_config.from_address, 
                'to': 'test_recipient2'
            }, 
            files=[("inline", ("cat_picxxxxxx", *cat_picture))]
        ),
        call().raise_for_status(),
    ]
    
    assert mock_requests.get.mock_calls == [
        call('https://www.reddit.com/r/cats/search.json?q=flair%3A%27default%27&restrict_sr=on&sort=top&t=day',
             headers={'user-agent': 'TheDailyWhiskersxxxxxx'}),
        call('https://i.redditmedia.com/vvovx9NCEv2KMxvRNI4B23PwCjAeAWehBYEiYmVhJ10.jpg?fit=crop&crop=faces%2Centropy&arh=2&w=216&s=e57e5b7130c7106b69b6eee3fc96727d',
             headers={'user-agent': 'TheDailyWhiskersxxxxxx'}),
        call('https://i.redditmedia.com/kIBDAr-elW5spIt8b8k06wdV-m7eLKempC9sLq6ZFLk.jpg?fit=crop&crop=faces%2Centropy&arh=2&w=216&s=9c0301fb3966b21c7a50eac5a1a292eb',
             headers={'user-agent': 'TheDailyWhiskersxxxxxx'})
    ]

@pytest.fixture(autouse=True)
def mock_requests(cat_picture, sample_cats_json):

    def mock_get(url, **kwargs):
        def build_mock_response(content, content_type):
            mock = Mock()
            mock.status_code = 200
            mock.content = content
            mock.headers = {"Content-Type": content_type}
            return mock

        if "reddit.com/r/cats/search.json" in url:
            return build_mock_response(sample_cats_json, "application/json")
        elif "https://i.redditmedia.com" in url:
            return build_mock_response(*cat_picture)

    mock = Mock()
    mock.get.side_effect = mock_get
    dailywhiskers.requests = mock
    return mock


@pytest.fixture()
def mailgun_config():
    return dailywhiskers.MailgunConfig(url="test_mailgun_url", 
                                    api_key="test_mailgun_apikey", 
                                    from_address="test_from_address")


@pytest.fixture()
def recipients():
    return ["test_recipient1", "test_recipient2"]


@pytest.fixture(autouse=True)
def config():
    config = """
    {
      "recipients": ["test_recipient1", "test_recipient2"],
      "mailgun": {
        "url": "test_mailgun_url",
        "api-key": "test_mailgun_apikey",
        "from_address": "test_from_address"
      }
    }
    """
    dailywhiskers.open = mock_open(mock=None, read_data=config)


@pytest.fixture(scope="function")
def cat_picture():
    return (bytes(random.getrandbits(8) for _ in range(100)), "image/jpeg")


@pytest.fixture(scope="session")
def sample_cats_json():
    with open("test/samplecatsearch.json") as f:
        return bytes(f.read().encode("UTF-8"))

@pytest.fixture(autouse=True)
def mock_random():
    dailywhiskers.generate_random_string = lambda length=6: "x" * length
    dailywhiskers.random.choice = lambda l: l[0] 
