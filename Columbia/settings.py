# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

# Skip this block if your db has no auth. But it really should.
# MONGO_USERNAME = '<your username>'
# MONGO_PASSWORD = '<your password>'
# Name of the database on which the user can be authenticated,
# needed if --auth mode is enabled.
# MONGO_AUTH_SOURCE = '<dbname>'

MONGO_DBNAME = 'columbia'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# schema = {
#     # Schema definition, based on Cerberus grammar. Check the Cerberus project
#     # (https://github.com/pyeve/cerberus) for details.
#     'firstname': {
#         'type': 'string',
#         'minlength': 1,
#         'maxlength': 10,
#     },
#     'lastname': {
#         'type': 'string',
#         'minlength': 1,
#         'maxlength': 15,
#         'required': True,
#         # talk about hard constraints! For the purpose of the demo
#         # 'lastname' is an API entry-point, so we need it to be unique.
#         'unique': True,
#     },
#     # 'role' is a list, and can only contain values from 'allowed'.
#     'role': {
#         'type': 'list',
#         'allowed': ["author", "contributor", "copy"],
#     },
#     # An embedded 'strongly-typed' dictionary.
#     'location': {
#         'type': 'dict',
#         'schema': {
#             'address': {'type': 'string'},
#             'city': {'type': 'string'}
#         },
#     },
#     'born': {
#         'type': 'datetime',
#     },
# }

td = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'td',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': '@type'
    },

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': {
        '@type': {
            'type': 'string'
        }
    }
}

loc_to_url_schema = {
    'loc': {
        'type': 'string'
    },
    'url': {
        'type': 'string'
    }
}

loc_to_url = {
    'item_title': 'loc_to_url',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'loc'
    },
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'schema': loc_to_url_schema
}

type_to_targetLocs_schema = {
    'type': {
        'type': 'string'
    },
    'targetLocs': {
        'type': 'list'
    }
}

type_to_targetLocs = {
    'item_title': 'type_to_targetLocs',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'type'
    },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT'],
    'schema': type_to_targetLocs_schema
}

targetLoc_to_childLoc_schema = {
    'targetLoc': {
        'type': 'string'
    },
    'childLoc': {
        'type': 'string'
    }
}

targetLoc_to_childLoc = {
    'item_title': 'targetLoc_to_childLoc',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'targetLoc'
    },
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT'],
    'schema': targetLoc_to_childLoc_schema
}

DOMAIN = {
    'td': td,
    'loc_to_url': loc_to_url,
    'type_to_targetLocs': type_to_targetLocs,
    'targetLoc_to_childLoc': targetLoc_to_childLoc
}