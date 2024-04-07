## DRF API for trainers.

### Install.
Clone project:
```bash 
git clone https://github.com/AxmetES/DRF_apis_for_trainers.git
```
create docker image:
```bash
docker build -t my-django-app .
```

create and run container:
```bash
docker run -d -p 8000:8000 --name my-django-container my-django-app
```

## swagger:
```
http://127.0.0.1:8000/swagger/
```
## get start.
requests:

#### GET______________________
gyms list API by trainer, user should be login.
work only for trainers GROUP.
```
GET request:
http://127.0.0.1:8000/trainerapi/getgymlist/
```
response:
```
[
  {
    "name": "Iron Man",
    "address": "Orynbor 10"
  },
  {
    "name": "Genesice",
    "address": "Москва, пл. Киевского Вокзала, 2"
  }
]
```
#### GET______________________
all programs by trainer or client, depends on login.
```
GET request:
http://127.0.0.1:8000/trainerapi/getprogramlist/
```
response:
```
[
  {
    "id": 11,
    "client": {
      "first_name": "Хосэ"
    },
    "trainer": {
      "first_name": "Баур"
    },
    "gym": {
      "name": "Gold Gym",
      "address": "Сабыр Ракымова 12"
    },
    "start_at": "2024-04-07T11:00:00Z",
    "end_at": "2024-04-07T12:00:00Z"
  },
  {
    "id": 12,
    "client": {
      "first_name": "Хосэ"
    },
    "trainer": {
      "first_name": "Баур"
    },
    "gym": {
      "name": "Gold Gym",
      "address": "Сабыр Ракымова 12"
    },
    "start_at": "2024-04-07T11:00:00Z",
    "end_at": "2024-04-07T12:00:00Z"
  }
]
```

#### GET______________________
all programs by trainer or client, depends on login.
```
GET request:
http://127.0.0.1:8000/trainerapi/getschedulelist/
```
response:
```
[
  {
    "trainer": "Баур",
    "gym_address": "Iron Man Orynbor 10",
    "start_at": "2024-04-04T10:00:00Z",
    "end_at": "2024-04-04T11:00:00Z"
  },
  {
    "trainer": "Баур",
    "gym_address": "Genesice Москва, пл. Киевского Вокзала, 2",
    "start_at": "2024-04-04T11:00:00Z",
    "end_at": "2024-04-04T12:00:00Z"
  },
  {
    "trainer": "Баур",
    "gym_address": "Gold Gym Сабыр Ракымова 12",
    "start_at": "2024-04-04T11:40:00Z",
    "end_at": "2024-04-04T13:00:00Z"
  }
]
```

#### POST______________________
all programs by trainer or client, depends on login.
```
POST request:
http://127.0.0.1:8000/trainerapi/makeprogram/
```
body:
```
{
    "client_email": "hos@gmail.com",
    "date": "07.04.2024",
    "start_time": "11:00:00",
    "end_time": "12:00:00",
    "gym": "Gold Gym",
    "trainer_email": "bake@gmail.com"
}
```
response:
```
{
  "id": 21,
  "client": {
    "first_name": "Хосэ"
  },
  "trainer": {
    "first_name": "Баур"
  },
  "gym": {
    "name": "Gold Gym",
    "address": "Сабыр Ракымова 12"
  },
  "start_at": "2024-04-07T11:00:00Z",
  "end_at": "2024-04-07T12:00:00Z"
}
```