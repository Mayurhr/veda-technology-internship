"""
Basic unittest tests for the Secure File Upload API.

Run with:
    python -m unittest test_main.py
"""

import io
import shutil
import unittest

from fastapi.testclient import TestClient

from main import app, UPLOAD_DIR

client = TestClient(app)


class TestSecureFileUploadAPI(unittest.TestCase):

    def test_root_status(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    def test_valid_upload(self):
        file_content = b"hello world"
        response = client.post(
            "/upload",
            files={"file": ("hello.txt", io.BytesIO(file_content), "text/plain")},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["original_filename"], "hello.txt")
        self.assertTrue(data["stored_filename"].endswith(".txt"))

    def test_invalid_file_type(self):
        response = client.post(
            "/upload",
            files={"file": ("malware.exe", io.BytesIO(b"bad"), "application/octet-stream")},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "File type not allowed")

    def test_oversized_file(self):
        big_content = b"0" * (5 * 1024 * 1024 + 1)  # 1 byte over the 5 MB limit
        response = client.post(
            "/upload",
            files={"file": ("big.txt", io.BytesIO(big_content), "text/plain")},
        )
        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.json()["detail"], "File size exceeds the allowed limit")

    def test_path_traversal_filename(self):
        response = client.post(
            "/upload",
            files={"file": ("../../test.txt", io.BytesIO(b"data"), "text/plain")},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # The stored filename must never contain path traversal characters,
        # regardless of what the original filename looked like.
        self.assertNotIn("..", data["stored_filename"])
        self.assertNotIn("/", data["stored_filename"])

    @classmethod
    def tearDownClass(cls):
        # Clean up any files created during testing.
        for item in UPLOAD_DIR.iterdir():
            if item.name != ".gitkeep":
                item.unlink()


if __name__ == "__main__":
    unittest.main()
