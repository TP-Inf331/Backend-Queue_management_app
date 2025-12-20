# Testing the API with Postman

## 1. Prerequisites (Fixing the Crash)
The server was previously crashing because of a missing dependency (`bcrypt`). You **MUST** rebuild the container for the fix to apply.

Run this in your terminal:
```bash
sudo docker compose up --build -d
```

## 2. Authentication (Login)
FastAPI's security uses `OAuth2` form data, not JSON.

- **Method**: `POST`
- **URL**: `http://localhost:8000/auth/token`
- **Body Type**: `x-www-form-urlencoded` (or `form-data`)
- **Key-Value Pairs**:
  - `username`: `admin@admin.com`
  - `password`: `adminpassword`

**Response**: You will receive an `access_token`. Copy this string!

## 3. Creating Data (e.g., Create Queue)
This endpoint requires the token you just got.

- **Method**: `POST`
- **URL**: `http://localhost:8000/queues/`
- **Authorization Tab**:
  - **Type**: Bearer Token
  - **Token**: Paste your access token here
- **Body Tab**:
  - **Type**: Raw -> JSON
  - **Content**:
    ```json
    {
        "nom": "Consultation",
        "institution": "Hospital",
        "max_capacity": 50
    }
    ```

## 4. Common Errors
- **401 Unauthorized**: You didn't provide the Bearer Token in the Authorization header.
- **422 Unprocessable Entity**: 
    - You sent JSON to the `/auth/token` endpoint instead of Form Data.
    - Or your JSON body in other requests is malformed.
- **Connection Refused**: The server is not running. Run the rebuild command above.
