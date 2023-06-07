## REPLIQ Jr. Django Practical Challenge

* python 3.10
* PostgreSQL

---
**Create virtual environment based on your operating system**
 * **For ubuntu**
 ```shell
python3.10 -m venv venv
  ```

  ###### Activate the virtual environment
 ```shell
source venv/bin/activate
  ```
 * **For windows**
 ```shell
python -m venv venv
  ```

---
**Copy .example.env file to .env:**

  * For linux
    ```shell
    cp .example.env .env
    ```
  * For windows
    ```shell
    copy .example.env .env
    ```
### Fill the .env with proper data
---

  ###### Migrate and run the project
 ```shell
python manage.py migrate
  ```
 ```shell
python manage.py runserver
  ```
  