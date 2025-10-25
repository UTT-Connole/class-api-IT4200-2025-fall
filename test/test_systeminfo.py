from app import app

def test_system_info_status_code():
    with app.test_client() as client:
        resp = client.get("/system-info")
        assert resp.status_code == 200, f"GET /system-info returned {resp.status_code}: {resp.get_data(as_text=True)}"

def test_system_info_keys_and_types():
    with app.test_client() as client:
        resp = client.get("/system-info")
        data = resp.get_json()
        assert isinstance(data, dict), f"Response JSON is not an object: {resp.get_data(as_text=True)}"

        expected_keys = [
            "hostname",
            "os",
            "os_release",
            "architecture",
            "python_version",
            "cpu_count",
            "disk_total_gb",
            "disk_free_gb",
        ]
        for k in expected_keys:
            assert k in data, f"Missing key: {k}"

        assert isinstance(data["hostname"], str)
        assert isinstance(data["os"], str)
        assert isinstance(data["architecture"], str)
        assert isinstance(data["python_version"], str)
        assert isinstance(data["cpu_count"], int) and data["cpu_count"] > 0

        for dk in ("disk_total_gb", "disk_free_gb"):
            v = data.get(dk)
            assert v is None or isinstance(v, (int, float))
            if v is not None:
                assert v >= 0