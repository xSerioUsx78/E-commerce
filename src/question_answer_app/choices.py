from model_utils import Choices


class Status:
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    choices = Choices(
        PENDING,
        APPROVED,
        REJECTED
    )
