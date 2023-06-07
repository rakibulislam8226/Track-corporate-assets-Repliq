## REPLIQ Jr. Django Practical Challenge

* python 3.10
* PostgreSQL

---
#### Clone the repo
```
git clone git@github.com:rakibulislam8226/Track-corporate-assets-Repliq.git
```
**Go to the directory file**
```
cd Track-corporate-assets-Repliq/
```
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
##### Fill the .env with proper data
---
### Install the requirements file.
```
pip install -r requirements.txt
```
#### Go the the src directory
```
cd src/
```

  ###### Migrate the project
 ```shell
python manage.py migrate
  ```
  ###### If needed create superuser with proper data
  ```
  python manage.py createsuperuser
  ```
  ###### Run the server
 ```shell
python manage.py runserver
  ```
---

## Project Structure
```
├── README.md
├── requirements.txt
├── src
│   ├── config
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   └── TimeStampMixin.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── corporate_assets
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── manage.py
└── sslcommerz_payment.txt
```