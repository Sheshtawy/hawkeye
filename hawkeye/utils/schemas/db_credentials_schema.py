DB_CREDENTIALS_SCHEMA = {
    "type": "object",
    "properties": {
        "host": {
            "type": "string",
            "minLength": 1
        },
        "port": {
            "type": "number"
        },
        "username": {
            "type": "string",
            "minLength": 1
        },
        "password": {
            "type": "string",
            "minLength": 1
        },
    },
}
