# eve-rights 0.0.2

Handle per-item rights in a python-eve application

## Description

Eve-Rights is allowing you to handle basics ACL on your eve application by adding two fields on your resource :

1. Who can read ?
2. Who can right ?

The only thing you need is to have an account resource named how you want.

## Configuration

For now, you should configure your Eve application by adding settings.

```python
# Eve-Rights
ACCOUNT_RESOURCE = "user" # The resource name associated to your users
RESOURCE_BLACKLIST = [] # The resource you want to blacklist from the restriction
ACL_FIELDS_READ = "w_reads" # Field name in the restricted resource. "Who can read ?"
ACL_FIELDS_WRITE = "w_writes"
RESTRICTED_RESOURCES = ['project'] # The resources you want to protect

# Domain configuration
DOMAIN = {
    'project': {
        'item_title': 'project',
        'authentication': MyTokenAuth(),
        'schema': {
            # Add those lines to each resources you want to protect
            'w_reads': { 'type': 'list', 'default': [], 'schema': { 'type': 'objectid', 'data_relation': { 'resource': ACCOUNT_RESOURCE, 'field': '_id', }, } },
            'w_writes': { 'type': 'list', 'default': [], 'schema': { 'type': 'objectid', 'data_relation': { 'resource': ACCOUNT_RESOURCE, 'field': '_id', }, } },
            'name': {
                'type': 'string',
                'required': True,
                'minlength': 1,
                'maxlength': 50,
            },
            'description': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 256,
            }
        },
        'description': "L'api projet permet de créer, éditer, chercher et supprimer un projet"
    },
    'user' : {
        'description': "Utilisateur de l'application",
        'authentication': MyTokenAuth(),
        'schema': {
            'email': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 10
            },
            'password': {
                'type': 'string',
            },
            'token': {
                'type': 'string',
            }
        }
    }
}
```

Then, don't forget to add the `set_request_auth_value` in your Authentication class.

```python
class MyTokenAuth(TokenAuth):

    def authorized(self, allowed_roles, resource, method):

        """ Validates the the current request is allowed to pass through.

        :param allowed_roles: allowed roles for the current request, can be a
                              string or a list of roles.
        :param resource: resource being requested.
        """

        auth = request.headers.get('Authorization')
        return auth and self.check_auth(auth, allowed_roles, resource, method)

    def check_auth(self, token, allowed_roles, resource, method):

        """ Called when a user try to access a resource """

        users = app.data.driver.db['user']
        user = users.find_one({'token': token})
        if user is not None:
            # Only this line is important
            self.set_request_auth_value(user.get('_id'))
        return user is not None
```
