from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


# STATES FOR FSM FIELDS

class StateChoices(TextChoices):
    STATUS_DRAFT = 'DRAFT', _('DRAFT')
    STATUS_AW_APPROVAL = 'AWAITING_APPROVAL', _('AWAITING_APPROVAL')
    STATUS_AW_ACCEPT = 'AWAITING_ACCEPTANCE', _('AWAITING_ACCEPTANCE')
    STATUS_ACCEPTED = 'ACCEPTED', _('ACCEPTED')
    STATUS_APPROVED = 'APPROVED', _('APPROVED')
    STATUS_REJECTED = 'REJECTED', _('REJECTED')
    STATUS_FINANCE_REQUESTED = 'FINANCE_REQUESTED', _('FINANCE_REQUESTED')
    STATUS_FINANCED = 'FINANCED', _('FINANCED')
    STATUS_FINANCE_REJECTED = 'FINANCE_REJECTED', _('FINANCE_REJECTED')
    STATUS_SETTLED = 'SETTLED', _('SETTLED')
    STATUS_OVERDUE = 'OVERDUE', _('OVERDUE')
    STATUS_AWAITING_SIGN_A = 'AWAITING_SIGN_A', _('AWAITING_SIGN_A')
    STATUS_AWAITING_SIGN_B = 'AWAITING_SIGN_B', _('AWAITING_SIGN_B')
    STATUS_AWAITING_SIGN_C = 'AWAITING_SIGN_C', _('AWAITING_SIGN_C')
    STATUS_DELETED = 'DELETED', _('DELETED')
    SIGN_A = 'SIGN_A', _('SIGN_A')
    SIGN_B = 'SIGN_B', _('SIGN_B')
    SIGN_C = 'SIGN_C', _('SIGN_C')
    SUBMIT = 'SUBMIT', _('SUBMIT')
    MAKER = 'MAKER', _('MAKER')
    NONE = 'NONE', _('NONE')
    STATUS_COMPLETED = 'COMPLETED', _('COMPLETED')
    STATUS_APPROVED_BY_BUYER = 'APPROVED BY BUYER', _('APPROVED BY BUYER')
    STATUS_AWAITING_BUYER_APPROVAL = 'AWAITING BUYER APPROVAL', _(
        'AWAITING BUYER APPROVAL')
    STATUS_REJECTED_BY_BUYER = 'REJECTED BY BUYER', _('REJECTED BY BUYER')
    STATUS_ARCHIVED = 'ARCHIVED', _('ARCHIVED')
    STATUS_INITIAL_STATE = 'INITIAL_STATE', _('INITIAL_STATE')
