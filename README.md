# ProtectNote
REST API to implement protected notes sharing where an authenticated user can create protected notes to be shared among other uses. The user can also create private/public notes.

JWT authentication implemented with PostgreSQL used as database.

## Routes:

### Users

| Method     | URI                               | Description                                                  |
|------------|-----------------------------------|---------------------------------------------------------|
| `POST`     | `/users/register`                        |Send form-data to create a user |
| `POST` | `/users/giveuser`                        |Send token in `Authorization` header to get user info from said token |
| `POST`     | `/token`                        |Send form-data with username and password to get `Access` and `Refresh` JWT tokens |

### Notes (Send JWT Access token in `Authorization` header)
`Following routes require user to be authenticated`

| Method     | URI                               | Description                                                  |
|------------|-----------------------------------|---------------------------------------------------------|
| `POST`     | `/notes/create`                        |Send form-data to create a note |
| `GET` | `/notes/all`                        |Return all notes created by current user |
| `GET`| `notes/<slug:uniqueID>`                         |Retrieves note by uniqueID. If the note is *protected* then send `password` in form-data. If the note is *private* then authentication is enough. No need of JWT `Access` token if note is *public*|
| `PUT/DELETE` | `/notes/<slug:uniqueID>/edit`                        |Edit the note (provide relevant form-data) or else delete the note |
| `GET` | `/notes/<slug:uniqueID>/getpassword`                        |Return password to access the protected note which can be shared with other users. The note should be created by the  current authenticated user for this to work. |


## Database Schema

Notes
 - `uniqueID` (automatically generated UUID to be used as secondary key,
   unique)
 - `content` (Text field for contents in the note) 
 - `language` (Text field which can be used for syntax highlighting on the frontend) 
 - `author` (Foreign key to a Django User model) 
 - `public` (Boolean field for whether note is public or not) 
 -  `protected` (Boolean field to protect the note with password) 
 - `password` (Automatically generated password for protected notes. Shared among users)

## Syntax Highlighting Example:

![syntax-example](https://i.imgur.com/wiltgVs.jpg)

## Request Examples
- ### **`Access a protected note, insert password as form-data`**

```http
GET /notes/7e1a8ef1-8bd1-4bdd-a206-fe424ec8fc07 HTTP/1.1
Host: localhost:8000
Authorization: Bearer <insert_jwt_access_token>
Content-Length: 141
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="password"

<password>
----WebKitFormBoundary7MA4YWxkTrZu0gW
```
Response:
```json
{
    "uniqueID": "7e1a8ef1-8bd1-4bdd-a206-fe424ec8fc07",
    "content": "cout<<\"Hello World\";",
    "language": "cpp",
    "public": false,
    "protected": true
}
```

------------


- ### **`Create a note`**

```http
POST /notes/create HTTP/1.1
Host: localhost:8000
Authorization: Bearer <insert_jwt_access_token>
Content-Length: 780
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="content"

int main() {
  int first_number, second_number, sum;
  cout << "Enter two integers: ";
  cin >> first_number >> second_number;
  sum = first_number + second_number;
  cout << first_number << " + " <<  second_number << " = " << sum;     
  return 0;
}
----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="language"

cpp
----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="public"

False
----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="protected"

True
----WebKitFormBoundary7MA4YWxkTrZu0gW
```
Response:
```json
{
    "uniqueID": "1384bb02-810e-4ba6-8ad2-5eac35d2d511",
    "content": "int main() {\n\n  int first_number, second_number, sum;\n    \n  cout << \"Enter two integers: \";\n  cin >> first_number >> second_number;\n\n  sumOfTwoNumbers\n  sum = first_number + second_number;\n\n  \n  cout << first_number << \" + \" <<  second_number << \" = \" << sum;     \n\n  return 0;\n}",
    "language": "cpp",
    "public": false,
    "protected": true
}


```


------------




