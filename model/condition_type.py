import enum


class ConditionType(enum.Enum):
    REQUIRED = 'REQUIRED'
    PREFERRED = 'PREFERRED'
    UNKNOWN = 'UNKNOWN'
