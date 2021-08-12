class HTTPException(Exception):
    def __init__(self, json, code: int):
        self.json = json
        self.code = code


class HTTP400Exception(HTTPException):
    def __init__(self, json):
        super().__init__(json, 400)


class HTTP401Exception(HTTPException):
    def __init__(self, json):
        super().__init__(json, 401)


class InputError(Exception):
    def __init__(self, message):
        self.message = message
        super(InputError, self).__init__(message)


class InvalidEmail(InputError):
    def __init__(self, message):
        super(InvalidEmail, self).__init__(message)
        self.__name__ = "invalid_email"


class InvalidValueError(InputError):
    def __init__(self, error: ValueError):
        self.message = f"{error.args[0]}"
        super(InvalidValueError, self).__init__(self.message)


class DoublePublishDatasetError(InputError):
    def __init__(self, dataset_version=None):
        if dataset_version:
            self.message = (
                f"Cannot publish {dataset_version.dataset.name} version {dataset_version.version_id}."
                "This dataset version already exists."
            )
        else:
            self.message = "Cannot duplicate a version of a dataset."
        super(DoublePublishDatasetError, self).__init__(self.message)


class InvalidTypeStructError(InputError):
    def __init__(self, declared_type):
        if declared_type == "DataFrame":
            self.message = "DataFrame: A pandas DataFrames are required to store the DataFrame dataset."
        elif declared_type == "GraphFrame":
            self.message = (
                "GraphFrame: Two pandas DataFrames are required to store the GraphFrame dataset."
                "One containing node data and one containing edge data"
            )
        else:
            self.message = f"{declared_type} is not a valid type. Only 'DataFrame' and 'GraphFrame' are permitted types."
        super(InvalidTypeStructError, self).__init__(self.message)


class InvalidDatasetTypeError(InputError):
    def __init__(self, declared_type):
        self.message = f"{declared_type} is not a valid type. Only 'DataFrame' and 'GraphFrame' are permitted types."
        super(InvalidDatasetTypeError, self).__init__(self.message)


class InvalidDataset(InputError):
    def __init__(self, name, info=None):
        info = info if type(info) != int else {"type": "version", "version": info}
        if not info:
            self.message = f"Dataset {name} does not exist"
        else:
            id_key = "version" if info.get("type") == "version" else "session_id"
            self.message = f"Dataset {name} with {info.get('type')} {info.get(id_key)} does not exist"
        super(InvalidDataset, self).__init__(self.message)


class DatasetTypeMismatch(InputError):
    def __init__(self, actual_type):
        if actual_type == "DataFrame":
            self.message = "Tabular dataset must resolve type tabular"
        elif actual_type == "GraphFrame":
            self.message = "Graph dataset must resolve type edges or nodes"
        super(DatasetTypeMismatch, self).__init__(self.message)


class InvalidFileFormat(InputError):
    def __init__(self, format_):
        self.message = f"Invalid file format: {format_} is not a valid data format. Must be 'csv' or 'json'."
        super(InvalidFileFormat, self).__init__(self.message)


class FileFormatMismatch(InputError):
    def __init__(self, declared_format, file_content_type):
        self.message = f"File format mismatch: {declared_format} does not match content type {file_content_type}."
        super(FileFormatMismatch, self).__init__(self.message)


class MissingPropertyError(InputError):
    def __init__(self, object_, properties):
        self.message = f"Missing property error: {object_} requires properties: {', '.join(properties)}"
        super(MissingPropertyError, self).__init__(self.message)


class ReservedNameError(InputError):
    def __init__(self, name):
        self.message = f"Reserved name: {name} is reserved."
        super(ReservedNameError, self).__init__(self.message)


# ###### GENERAL EXCEPTIONS TO LOG ##########


class AthenaQueryError(Exception):
    def __init__(self, query, error):
        self.message = f"Query {query} failed with error {error}"
        super(AthenaQueryError, self).__init__(self.message)


class AthenaCreateTableError(Exception):
    def __init__(self, table_name, error):
        self.message = f"Creating table {table_name} failed, {error}"
        super(AthenaCreateTableError, self).__init__(self.message)


class AthenaCreateDatabaseError(Exception):
    def __init__(self, database_name, error):
        self.message = f"Creating database {database_name} failed, {error}"
        super(AthenaCreateDatabaseError, self).__init__(self.message)


class GrayWolfSessionDatasetError(Exception):
    def __init__(self, dataset):
        self.message = (
            f"Session datasets are not currently supported, can't query {dataset}"
        )
        super(GrayWolfSessionDatasetError, self).__init__(self.message)


class SessionWithoutInstancesError(Exception):
    def __init__(self, session_name):
        self.message = f"The session {session_name} is not linked to any remote cluster with a valid ec2 instance"
        super(SessionWithoutInstancesError, self).__init__(self.message)


class BadStorageType(Exception):
    def __init__(self, name, storage_type, submit_type, instance_id):
        self.message = (
            f"Dataset {name} {submit_type} {instance_id} was stored as type {storage_type}. "
            "This is not a valid type."
        )
        super(BadStorageType, self).__init__(self.message)


class NotAllowedError(HTTP400Exception):
    def __init__(self):
        super().__init__(
            {
                "status": "error",
                "code": "not_allowed",
                "message": "You do not have the permission to perform this action",
            }
        )
