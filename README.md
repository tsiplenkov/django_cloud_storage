**<span style="color:red;"> Attention: Don't use this code on production. </span>**

## Overview

Cloud Storage Boilerplate RestApi with django-restframework, drf-simplejwt, drf-spectacular

### Features

* authorization with JWT
* storage size limit per user
* file upload
* enable public access for file

## Installation 

```shell

```

## TODO

* create directories
* superuser (admin) api

### Fix warning for drf-spectacular

```
Warning #0: UserFileList: UserFileSerializer: could not resolve field on model <class 'files.models.UserFile'> with path "owner.username". This is likely a custom field that does some unknown magic. Maybe consider annotating the field/property? Defaulting to "string". (Exception: UserProfile has no field named 'username')
Warning #1: UserFileDetail: UserFileSerializer: could not resolve field on model <class 'files.models.UserFile'> with path "owner.username". This is likely a custom field that does some unknown magic. Maybe consider annotating the field/property? Defaulting to "string". (Exception: UserProfile has no field named 'username')
```

https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#updating-our-serializer
https://github.com/tfranzel/drf-spectacular/issues/68#issuecomment-633741787

## Fix different fields for POST and PATCH /files/{file-id}

current fields:
```json
{
  "file_object": "string",
  "public_access": true
}
```

required fields POST:

```json
{
    "file_object": "string",
  "public_access": true
}
```

required fields PATCH:

```json
{
  "public_access": true
}

```