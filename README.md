**<span style="color:red;"> Attention: Don't use this code on production! </span>**

## Overview

Cloud Storage Boilerplate RestApi with django-restframework, drf-simplejwt, drf-spectacular

### Features

* authorization with JWT
* storage size limit per user
* file upload
* enable public access for file

## Installation & running

### Installation

```shell
# (optional) create and activate venv
python3 -m venv ./venv
source venv/bin/activate

# install packages
pip install requirements.txt

```

### Running

#### Prod version

```shell
# run app
python manage.py runserver
```


#### Dev version
```shell
DJANGO_SETTINGS_MODULE=cloud_storage.settings.dev python manage.py runserver
```

#### Run testing

```shell
DJANGO_SETTINGS_MODULE=cloud_storage.settings.test python manage.py test
```


## TODO

* create directories & subdirectories as file entity
* superuser (admin) api

### Fix warning for drf-spectacular

```
Warning #0: UserFileList: UserFileSerializer: could not resolve field on model <class 'files.models.UserFile'> with path "owner.username". This is likely a custom field that does some unknown magic. Maybe consider annotating the field/property? Defaulting to "string". (Exception: UserProfile has no field named 'username')
Warning #1: UserFileDetail: UserFileSerializer: could not resolve field on model <class 'files.models.UserFile'> with path "owner.username". This is likely a custom field that does some unknown magic. Maybe consider annotating the field/property? Defaulting to "string". (Exception: UserProfile has no field named 'username')
```

https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#updating-our-serializer
https://github.com/tfranzel/drf-spectacular/issues/68#issuecomment-633741787

