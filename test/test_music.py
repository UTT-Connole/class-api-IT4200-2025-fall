from pathlib import Path

def test_audio_file_path():
    project_root = Path(__file__).resolve().parent.parent
    audio_path = project_root / "static" / "wip.m4a"
    assert audio_path.is_file(), f"Missing file: {audio_path}"

def test_play_audio(client):
    response = client.get('/music')
    assert response.status_code == 200
    assert response.mimetype == 'audio/mp4'
    assert len(response.data) > 0