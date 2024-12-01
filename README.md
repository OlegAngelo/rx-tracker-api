# [RX Tracker API](https://github.com/mcdylanb/medAlert)

This is the documentation for the RX Tracker application (*which is also known as Medical Alert application*), which is a simple and easy-to-use API for managing prescription and medication details data. The API has a number of endpoints for creating, retrieving, and updating prescription and medication details data.

**Note:** Project is ongoing and is not open-source, thus, project is currently in private.

## Table of Contents

---

- [Features](#features)
- [Technology](#technology)
- [Endpoints](#endpoints)

<a id="features"/>

## Features

---
- Admin page
- Create admin
- Create user
- Generate API token
- Get Prescriptions with medical details
- Add Prescriptions with medical details

<a id="technology"/>

## Technology

---
This API uses a number of open source projects to work properly:

- [Django](https://www.djangoproject.com/) for the backend framework
- [Django Rest Framework](https://www.django-rest-framework.org/) for authentication & authorization
- [SQLite](https://www.sqlitetutorial.net/) for the database

<a id="endpoints"/>

## Endpoints

---


### Generate API token

```
POST /api/token-auth
```

**Request:**
```json
{
  "username": "user1",
  "password": "W3lc0M3!@#$"
}
```

1. Create a user under admin page.
2. Generate token in admin page, or you can `run curl` command in terminal to get api key using the created user's credentials.
```
curl -X POST http://127.0.0.1:8000/api/token-auth/ -H "Content-Type: application/json" -d '{"username": "user1", "password": "W3lc0M3!@#$"}'
```

**Response:**
```
{ "token": "4b62e76d5d614f55a4558a1a6a18445b2d69f60e" }
```

<br />

### Add Prescriptions with Medical Details

```
POST /api/prescriptions/add
```
**Request:**
```
Authorization: Token 29675fd5e1bbff8c9a444683757fce0377736505
```
```json
{
    "user": 2,
    "start_date": "2024-12-05",
    "duration": 2,
    "is_completed": false,
    "medication_details": [
        {
            "medication_name": "Biogesic",
            "dosage_measurement": "500mg",
            "frequency": 3,
            "intake_time": "08:00",
            "instructions": "Take with meals."
        }
    ]
}
```

**Response:**
`201 Created`

```json
{
    "id": 3,
    "user": 2,
    "start_date": "2024-12-05",
    "duration": 2,
    "end_date": "2024-12-07",
    "completed_date": null,
    "is_completed": false,
    "medication_details": [
        {
            "id": 9,
            "medication_name": "Biogesic",
            "dosage_measurement": "500mg",
            "frequency": 3,
            "instructions": "Take with meals.",
            "intake_time": "08:00:00",
            "intake_date": "2024-12-05",
            "is_completed": false
        },
        {
            "id": 9,
            "medication_name": "Biogesic",
            "dosage_measurement": "500mg",
            "frequency": 3,
            "instructions": "Take with meals.",
            "intake_time": "08:00:00",
            "intake_date": "2024-12-06",
            "is_completed": false
        }
    ]
}
```
Response is grouped by `prescription`.

<br />

### Get Prescriptions with Medical Details

```
GET /api/prescriptions
```

**Request:**
```
Authorization: Token 29675fd5e1bbff8c9a444683757fce0377736505
```

**Response:**
`200 OK`

```json
[
    {
        "intake_date": "2024-12-05",
        "medication_details": [
            {
                "medication_name": "Biogesic",
                "frequency": 3,
                "dosage_measurement": "500mg",
                "prescription": 3,
                "instructions": "Take with meals."
            }
        ]
    },
    {
        "intake_date": "2024-12-06",
        "medication_details": [
            {
                "medication_name": "Biogesic",
                "frequency": 3,
                "dosage_measurement": "500mg",
                "prescription": 3,
                "instructions": "Take with meals."
            }
        ]
    }
]
```
Response is grouped by `intake_date` and logged-in `user_id`
