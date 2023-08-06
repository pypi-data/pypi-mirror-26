# Porper (Portable Permission Controller)

https://pypi.python.org/pypi/porper

Overview
=================

![porper][porper-image]

This is a library to provide the permission control on resources in serverless environment.

When implementing applications using existing frameworks, you can manage permissions on resources using the module they provide, but they are not available when you implement applications using serverless computing like AWS Lambda.

This is a very simple RBAC (Role Based Access Controller) library to manage permissions based on their privileges.

## Installation

NOTE: Python 2.7

```python
pip install porper
```

Database Initialization
```
$ mysql -h <db_host> -u <db_user> -p <db_name> < porper_initial.sql
```

## How to use Google+ and Github Authentication

If you plan to use Google+ and/or GitHub authentications, set related values either as an environment variables or in a config.json. (Please see next section, 'How to provide related info')

Please see these 2 sites to find out how to setup OpenID connect

Google+ : https://developers.google.com/identity/protocols/OpenIDConnect

GitHut : https://developer.github.com/v3/oauth/

## How to provide related info

There are 2 ways to set necessary information

Using Environment Variables
```
export MYSQL_HOST=<db_host>
export MYSQL_USER=<db_user>
export MYSQL_PASSWORD=<db_password>
export MYSQL_DATABASE=<db_name>

export GOOGLE_TOKENINFO_ENDPOINT=https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=

export GITHUB_AUTH_ENDPOINT=https://github.com/login/oauth
export GITHUB_API_ENDPOINT=https://api.github.com
export GITHUB_CLIENT_ID=<client_id>
export GITHUB_CLIENT_SECRET=<secret_id>
```

Using 'config.json' that needs to be placed in the root of porper library
```
{
  "mysql": {
    "host": "<db_host>",
    "username": "<db_user>",
    "password": "<db_password>",
    "database": "<db_name>"
  },
  "google": {
    "tokeninfo_endpoint": "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="
  },
  "github": {
    "auth_endpoint": "https://github.com/login/oauth",
    "api_endpoint": "https://api.github.com",
    "client_id": "<client_id>",
    "client_secret": "<secret_id>"
  }
}
```

## How to get mysql connection to the Porper database

```
from porper.models.connection import mysql_connection
connection = mysql_connection()
```

## How to authenticate

```
# For Google+ Auth
from porper.controllers.google_auth_controller import GoogleAuthController
googleAuthController = GoogleAuthController(connection)
user_info = googleAuthController.authenticate(id_token)

# For GitHub Auth
from porper.controllers.github_auth_controller import GithubAuthController
githubAuthController = GithubAuthController(connection)
user_info = githubAuthController.authenticate(code, state)

# 'access_token' is used when sending following requests
access_token = user_info['access_token']
```

## How to manage roles

### A couple of roles will be created during the database initialization
```
('435a6417-6c1f-4d7c-87dd-e8f6c0effc7a','public')
('ffffffff-ffff-ffff-ffff-ffffffffffff','admin')
```

### To create a new role
You must be the admin.
```
params = {
  "name": "<name_of_the_role>"
}
from porper.controllers.role_controller import RoleController
roleController = RoleController(connection)
roleController.create(access_token, params)
```

### To find roles
```
roleController.find_all(access_token)
```
> if you're the admin, it will return all roles

> otherwise, return all roles where you're belong


## How to manage users

The first user logging into the system will be added as an admin automatically

### To invite users
You have to invite them first and you must be either the admin or the role admin of the role where the new user will belong
```
params = {
  "email": "<email_address>",
  "role_id": "<role_id>",
  "is_admin": "<0_or_1>"
}
from porper.controllers.invited_user_controller import InvitedUserController
invited_user_controller = InvitedUserController(connection)
invited_user_controller.create(access_token, params)
```

### To find invited users
```
params = {}
invited_user_controller.find_all(access_token, params)
```
> if you're the admin, it will return all invited users

> if you're the role admin of one or more roles, it will return all invited users of the roles where you're the role admin

> otherwise, it will raise an exception of 'not permitted'

```
params = {
  "role_id": "<role_id>"
}
invited_user_controller.find_all(access_token, params)
```
> if you're the admin or a role admin of the given role, it will return all invited users of the given role

> otherwise, it will raise an exception of 'not permitted'

Once the invited users log in successfully for the first time, they will be automatically registered and added to the roles specified during invitation


### To find registered user
```
params = {}
from porper.controllers.user_controller import UserController
userController = UserController(connection)
userController.find_all(access_token, params)
```
> if you're the admin, it will return all users

> if you're the role admin of one or more roles, it will return all users of the roles where you're the role admin

> otherwise, it will return yourself

```
params = {
  "role_id": "<role_id>"
}
userController.find_all(access_token, params)
```
> if you're the admin or a member of the given role, it will return all users of the given role

> otherwise, it will raise an exception of 'not permitted'

```
params = {
  "id": "<id>",
  "email": "<email_address>"
}
userController.find_all(access_token, params)
```
> It will return a specific user with the given id or email address


### To assign a user to a role
You must be either the admin or the role admin.

```
params = {
  "user_id": "<user_id>",
  "role_id": "<role_id>",
  "is_admin": "<0 or 1>"
}
from porper.controllers.user_controller import UserController
userController = UserController(connection)
userController.create(access_token, params)
```


## How to create a controller & model for a custom resource

### Controller
```
from porper.controllers.resource_controller import ResourceController

class DemoController(ResourceController):

    def __init__(self, permission_connection):
        ResourceController.__init__(self, None, None, permission_connection)
        self.resource = 'demo'

        from demo import Demo
        self.model = Demo(permission_connection)

    # redefine this method if necessary
    def create(self, access_token, params):
        return ResourceController.create(self, access_token, params)

    # redefine this method if necessary
    def update(self, access_token, params):
        return ResourceController.update(self, access_token, params)

    # redefine this method if necessary
    def delete(self, access_token, params):
        return ResourceController.delete(self, access_token, params)

    # redefine this method if necessary
    def find_all(self, access_token, params):
        return ResourceController.find_all(self, access_token, params)

    # redefine this method if necessary
    def find_one(self, access_token, params):
        return ResourceController.find_one(self, access_token, params)
```

### Model
```
class Demo:

    def __init__(self, connection):
        self.connection = connection

    # implement how to create a new instance
    def create(self, params):
        pass

    # implement how to update an instance
    def update(self, params):
        pass

    # implement how to delete an instance
    def delete(self, params):
        pass

    # implement how to find a specific instance(s)
    def find(self, params):
        pass

```

## How to manage permissions

### To gran permissions
```
from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(connection)
permitted_user_id = "<admin or user_id_who_has_create_permission_on_the_target_resource>"

# by user_id
permission_params = {
    "user_id": "<user_id>",
    "resource": "<resource_name>",
    "value": "<* or resource_id>",
    "action": "<create|read|update|delete>"
}
permission_controller.create(None, permission_params, permitted_user_id)

# by role_id
permission_params = {
    "role_id": "<role_id>",
    "resource": "<resource_name>",
    "value": "<* or resource_id>",
    "action": "<create|read|update|delete>"
}
permission_controller.create(None, permission_params, permitted_user_id)
```

### To revoke permissions
```
from porper.controllers.permission_controller import PermissionController
permission_controller = PermissionController(connection)
permitted_user_id = "<admin or user_id_who_has_create_permission_on_the_target_resource>"

# by permission id
permission_params_by_id = {
    "id": "<permission_id>"
}
permission_controller.delete(None, permission_params, permitted_user_id)

# by user_id
permission_params_by_user_id = {
    "user_id": "<user_id>",
    "resource": "<resource_name>",
    "value": "<* or resource_id>",
    "action": "<create|read|update|delete>"
}
permission_controller.delete(None, permission_params, permitted_user_id)

# by role_id
permission_params_by_user_id = {
    "role_id": "<role_id>",
    "resource": "<resource_name>",
    "value": "<* or resource_id>",
    "action": "<create|read|update|delete>"
}
permission_controller.delete(None, permission_params, permitted_user_id)
```

## Sungard Availability Services | Labs
[![Sungard Availability Services | Labs][labs-image]][labs-github-url]

This project is maintained by the Labs team at [Sungard Availability
Services][sungardas-url]

GitHub: [https://sungardas.github.io][sungardas-github-url]

Blog: [http://blog.sungardas.com/CTOLabs/][sungardaslabs-blog-url]

[porper-image]: ./docs/images/logo.png?raw=true
[convoy-ebs-url]: https://github.com/rancher/convoy/blob/master/docs/ebs.md
[docker-zookeeper-url]: https://hub.docker.com/r/_/zookeeper
[labs-github-url]: https://sungardas.github.io
[labs-image]: https://raw.githubusercontent.com/SungardAS/repo-assets/master/images/logos/sungardas-labs-logo-small.png
[sungardas-github-url]: https://sungardas.github.io
[sungardas-url]: http://sungardas.com
[sungardaslabs-blog-url]: http://blog.sungardas.com/CTOLabs/


