
def test_root(client):
  response = client.get("/")
  json_data = response.get_json()
  assert json_data == "Activity Book Generator back-end is running"
