# import builtins


# def test_skylands_wrong_answer(monkeypatch, client):
#     """When input isn't the secret, the route should return 'Wrong Answer'"""
#     monkeypatch.setattr(builtins, 'input', lambda prompt='': 'not the secret')
#     resp = client.get('/Skylands')
#     assert resp.status_code == 200
#     # The view returns plain text
#     assert resp.get_data(as_text=True) == 'Wrong Answer'


# def test_skylands_correct_answer(monkeypatch, client):
#     """When input equals 'Conquretron' the route should return the success string."""
#     monkeypatch.setattr(builtins, 'input', lambda prompt='': 'Conquretron')
#     resp = client.get('/Skylands')
#     assert resp.status_code == 200
#     assert resp.get_data(as_text=True) == 'K. A. O. S.'
