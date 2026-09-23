# Secure File Upload API

## 1. Description
A beginner-friendly REST API built with FastAPI that lets clients upload
files securely. It validates the file type and size, generates a safe
random filename for every upload, and stores files only inside a
dedicated `uploads/` directory.

## 2. Objective
To practice building a REST API in Python while applying core file
upload security practices: type validation, size limits, safe filename
handling, and path traversal protection.

## 3. Technologies Used
- Python 3
- FastAPI
- Uvicorn (ASGI server)
- python-multipart (for form/file parsing)

## 4. Features
- Single endpoint to upload a file
- Whitelist-based file type validation
- Configurable maximum file size (default 5 MB)
- Randomly generated, safe stored filenames
- Path traversal protection
- Clear JSON success and error responses
- No internal filesystem paths exposed to the client

## 5. Project Structure
```
Secure-File-Upload-API/
├── main.py
├── test_main.py
├── README.md
├── requirements.txt
├── sample_output.txt
└── uploads/
    └── .gitkeep
```

## 6. API Endpoint
| Method | Endpoint  | Description                 |
|--------|-----------|------------------------------|
| GET    | `/`       | API status check             |
| POST   | `/upload` | Upload a file                |

## 7. Allowed File Types
- `.txt`
- `.csv`
- `.pdf`
- `.jpg`
- `.jpeg`
- `.png`

Any other file extension is rejected with a `400 Bad Request`.

## 8. File Size Restriction
Maximum upload size is **5 MB**. Files larger than this are rejected
with a `413 Payload Too Large` response.

## 9. Safe Filename Handling
The original filename is **never** used to build the file's stored
path. Instead, a new filename is generated using `uuid4()`, combined
with the validated file extension. This removes any risk from unusual
characters, unicode tricks, or crafted filenames.

## 10. Storage Security
- Uploaded files are written only inside the project's `uploads/`
  directory.
- The final destination path is resolved and checked to confirm it
  stays inside `uploads/` before the file is written, as an extra
  safeguard.
- No original filename input is ever concatenated directly into a
  file path, so `../` sequences and absolute paths cannot escape the
  upload directory.

## 11. Error Handling
- Invalid file type → `400 Bad Request`
- File too large → `413 Payload Too Large`
- Missing filename → `400 Bad Request`
- Unexpected server errors → `500 Internal Server Error` with a
  generic message (no internal paths or stack traces are exposed)

## 12. Installation
```bash
pip install -r requirements.txt
```

## 13. How to Run
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

Interactive docs are available at `http://127.0.0.1:8000/docs`.

## 14. API Usage
Example using `curl`:
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
     -F "file=@example.txt"
```

## 15. Testing
Run the included unittest suite:
```bash
python -m unittest test_main.py
```
The tests cover:
- API status check
- Successful upload
- Rejected file type
- Rejected oversized file
- Path traversal filename handling

## 16. Sample Response
See `sample_output.txt` for full example requests and responses,
including success, invalid type, oversized file, and path traversal
cases.

## 17. Security Considerations
- File extension validation alone is **not** complete security. A
  malicious file can still be crafted with an allowed extension. In a
  production system, this should be combined with content/MIME
  sniffing, antivirus scanning, and storage isolation (e.g. serving
  uploads from a separate domain or object storage with no execute
  permissions).
- This project is intended as a learning exercise and demonstrates
  foundational upload security practices, not a production-hardened
  system.

## 18. Concepts Learned
- Building REST API endpoints with FastAPI
- Handling file uploads with `UploadFile`
- Input validation and meaningful HTTP status codes
- Safe filename generation and path traversal prevention
- Structuring code into small, testable helper functions
- Writing basic unit tests with `unittest` and `TestClient`

## 19. Future Improvements
- Add authentication before allowing uploads
- Scan uploaded files for viruses/malware
- Store files in cloud storage (e.g. S3) instead of local disk
- Save file metadata in a database
- Add automated CI testing
- Expand the API with endpoints to list, download, and delete files

## 20. Conclusion
This project demonstrates a simple but security-conscious file upload
API built with FastAPI, covering type validation, size limits, safe
filename handling, and path traversal protection — core practices for
any application that accepts user-uploaded files.
