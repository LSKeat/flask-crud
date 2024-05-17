
## Instruction

1. Clone the project
```
git clone https://github.com/LSKeat/flask-crud.git
```
<br />

2. Create a database and use the provided `test.sql` file to create a table and insert some dummy data

<br />

3. Edit your details at the top of `app.py`
```
# MySQL configuration
config = {
    'host': 'localhost',
    'user': 'YOUR_USER_NAME',
    'password': 'YOUR_PASSWORD',  
    'database': 'DATABASE_NAME'
}
```
<br />

4. Test your API using [POSTMAN](https://www.postman.com/)

Replace {{baseUrl}} to your local host url or set in the postman

```bash
GET {{baseUrl}}/status
# return 200 status code - if successful
GET {{baseUrl}}/data
# return list of the data
PUT {{baseUrl}}/update_data/1
# Sample
{
    "name": "Admin 1",
    "email": "1_admin@test.com",
    "status": 1
}
POST {{baseUrl}}/insert_data
# Sample
{
    "name": "Admin 6",
    "email": "admin6@test.com",
    "status": 1
}
DELETE {{baseUrl}}/delete_data/3

```
