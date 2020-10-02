# TASK MANAGER API

**User registration**
----
Takes username and password, returns json data with username and password of new user.

* **URL:**
  /api/users/

* **Method:**
  `POST`
  
*  **URL Params:** 
  None

* **Data Params:**

  `{ "username" : "some_user_name", "password" : "some_password" }`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ "username" : "some_user_name", "password" : "pbkdf2_sha256$216000$OWZ5pnbgfXd7$gk4HPQSz8pFQ1ruzQ2dO71VpWvmT9quY5b+KoaMVEVs=" }`

 **Getting a token**
----
  Takes username and password, returns json data with JWT token.

* **URL:**
  /api-token-auth/

* **Method:**
  `POST`
  
*  **URL Params:**
  None

* **Data Params:**
  None

* **Success Response:**

  * **Code:** 200 OK <br />
    **Content:** `{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjAxNjI3NDY1LCJlbWFpbCI6IiJ9.uKlXhKU4x5NNnh2Yn39RJ_Qg_6XPLw5ADS5mZlXW_jw" }`
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "non_field_errors": [ "Unable to log in with provided credentials." ] }`

**Get all user tasks**
----
  Returns json data with details about tasks.

* **URL:**
  /api/tasks/

* **Method:**
  `GET`
  
*  **URL Params:**

   `status=[string]`
   
   `planned_completion_date=[string]`

   possible status values:
   `new` | `planned` | `in progress` | `completed`
   
   date format: `YYYY-MM-DD`
   
* **Data Params:**
  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[ { "title":"some_title",
    "description":"some_description",
    "date_of_creation":"2020-09-30",
    "status":"new",
    "planned_completion_date":"2020-10-30",
    "user":1 }
     { "title":"another_title",
    "description":"another_description",
    "date_of_creation":"2020-08-20",
    "status":"in progress",
    "planned_completion_date":"2020-10-10",
    "user":1 }]`
    
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{"detail":"Signature has expired."}`
    
  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ "non_field_errors": [ "Unable to log in with provided credentials." ] }`

**Get one user task**
----
  Returns json data with details about one task.

* **URL:**
  /api/tasks/`[task_id]`

* **Method:**
  `GET`
  
*  **URL Params:**
  None
   
* **Data Params:**
  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{ "title":"some_title",
    "description":"some_description",
    "date_of_creation":"2020-09-30",
    "status":"new",
    "planned_completion_date":"2020-10-30",
    "user":1 }]`
    
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{"detail":"Signature has expired."}`
    
  OR

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ "detail": "Not found." }`
  
**Create a task**
----
  Takes json data with: title, description, status and planned completion date. 
  Returns json data with details created task.

* **URL:**
  /api/tasks/

* **Methods:**
  `POST`
  
*  **URL Params:**
  None
   
* **Data Params:**
  `[{ "title":"some_title",
    "description":"some_description",
    "status":"new",
    "planned_completion_date":"2020-10-30",
    }]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{ "title":"some_title",
    "description":"some_description",
    "date_of_creation":"2020-09-30",
    "status":"new",
    "planned_completion_date":"2020-10-30",
    "user":1 }]`
    
* **Error Response:**
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{"detail":"Signature has expired."}`

**Update the task**
----
  Takes json data with one or more of this: title, description, status, planned completion date. 
  Returns json data with details about this task.

* **URL:**
  /api/tasks/`[task_id]`

* **Methods:**
  `PUT` `PATCH`
  
*  **URL Params:**
  None
   
* **Data Params:**
  `[{ "title":"some_title",
    "description":"some_description",
    "status":"new",
    "planned_completion_date":"2020-10-30",
    }]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{ "title":"some_title",
    "description":"some_description",
    "date_of_creation":"2020-09-30",
    "status":"new",
    "planned_completion_date":"2020-10-30",
    "user":1 }]`
    
* **Error Response:**
  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{"detail":"Signature has expired."}`

  OR
  
  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ "detail": "Not found." }`

