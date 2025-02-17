from model_utils import Choices


class Status:
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'

    choices = Choices(
        PENDING,
        SUCCESS,
        FAILED
    )
