from cerberus import Validator, DocumentError
from setup import *


def data_validate():
    dbSchema = {
        "host": {'required': True, 'type': 'string', 'max': 15},
        "port": {'required': True, 'type': 'integer', 'max': 65535},
        "user": {'required': True, 'type': 'string', 'max': 15},
        "database": {'required': True, 'type': 'string', 'max': 15},
    }

    validate = Validator(dbSchema)
    log.info("Validating config...")
    try:
        validate.validate(dbData)
    except DocumentError as configError:
        log.error("Configuration error")
        log.error(configError)
        exit(3)
    finally:
        log.info("Validation successful")
