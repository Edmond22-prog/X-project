from enum import Enum

from utils.common import build_tuple_types


class ServiceRequestStatus(str, Enum):
    """
    Enum for Service Request Status.
    """
    ACTIVE = "active"
    ARCHIVED = "archived"
    CLOSED = "closed"


SERVICE_REQUEST_STATUS = build_tuple_types(ServiceRequestStatus)
