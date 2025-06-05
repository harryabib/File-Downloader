import json
from unittest.mock import patch


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_api_files_empty_directory(client):
    with patch("os.path.exists", return_value=True), patch(
        "os.listdir", return_value=[]
    ):

        response = client.get("/api/files")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0


@patch("app.get_files")
def test_api_files_with_data(mock_get_files, client):
    mock_files = [
        {
            "name": "test.txt",
            "size": "1,2 Ko",
            "modified": "2023-01-01 10:00:00",
            "type": "text/plain",
        }
    ]
    mock_get_files.return_value = mock_files

    response = client.get("/api/files")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "test.txt"


def test_download_file_not_found(client):
    response = client.get("/download/nonexistent.txt")
    assert response.status_code == 404
    assert b"File not found" in response.data


@patch("os.path.exists")
@patch("app.send_file")
def test_download_existing_file(mock_send_file, mock_exists, client):
    mock_exists.return_value = True
    mock_send_file.return_value = "file_content"

    response = client.get("/download/test.txt")
    mock_exists.assert_called_once()
    mock_send_file.assert_called_once()


@patch("os.path.exists")
@patch("os.makedirs")
@patch("os.listdir")
def test_get_files_creates_directory(mock_listdir, mock_makedirs, mock_exists, client):
    from app import get_files

    mock_exists.return_value = False
    mock_listdir.return_value = []

    get_files()

    mock_makedirs.assert_called_once_with("files")


def test_home_page(client):
    with patch("app.get_files", return_value=[]):
        response = client.get("/")
        assert response.status_code in [200]
