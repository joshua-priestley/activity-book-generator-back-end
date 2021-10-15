from activitygen import create_app

def test_config():
  # App from default config should not be in testing mode
  assert not create_app().testing
  # App from config TESTING=True should be in testing mode
  assert create_app({"TESTING": True}).testing
