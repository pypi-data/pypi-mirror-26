from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils import FieldTracker

from nodeconductor.core import fields as core_fields
from nodeconductor.core import models as core_models
from nodeconductor.structure import models as structure_models
from nodeconductor_assembly_waldur.support import models as support_models
from nodeconductor_assembly_waldur.common import mixins as common_mixins

from . import managers


@python_2_unicode_compatible
class ExpertProvider(core_models.UuidMixin,
                     structure_models.TimeStampedModel):
    customer = models.OneToOneField(structure_models.Customer, related_name='+', on_delete=models.CASCADE)

    class Meta(object):
        verbose_name = _('Expert providers')

    def __str__(self):
        return str(self.customer)

    @classmethod
    def get_url_name(cls):
        return 'expert-provider'


class PriceMixin(models.Model):
    class Meta(object):
        abstract = True

    price = models.DecimalField(max_digits=22, decimal_places=7,
                                validators=[MinValueValidator(Decimal('0'))],
                                default=0)


@python_2_unicode_compatible
class ExpertRequest(core_models.UuidMixin,
                    core_models.NameMixin,
                    core_models.DescribableMixin,
                    PriceMixin,
                    common_mixins.ProductCodeMixin,
                    structure_models.StructureLoggableMixin,
                    structure_models.TimeStampedModel):
    class States(object):
        PENDING = 'pending'
        ACTIVE = 'active'
        CANCELLED = 'cancelled'
        COMPLETED = 'completed'

        CHOICES = (
            (PENDING, _('Pending')),
            (ACTIVE, _('Active')),
            (CANCELLED, _('Cancelled')),
            (COMPLETED, _('Completed'))
        )

    user = models.ForeignKey(core_models.User, related_name='+', on_delete=models.CASCADE,
                             help_text=_('The user which has created this request.'))
    project = models.ForeignKey(structure_models.Project, related_name='+', on_delete=models.CASCADE)
    state = models.CharField(default=States.PENDING, max_length=30, choices=States.CHOICES)
    type = models.CharField(max_length=255)
    extra = core_fields.JSONField(default={})
    issue = models.ForeignKey(support_models.Issue, null=True, on_delete=models.SET_NULL)
    recurring_billing = models.BooleanField(
        default=False, help_text=_('Defines whether expert request has to be billed every month or only once'))
    objectives = models.TextField(blank=True)
    milestones = models.TextField(blank=True)
    contract_methodology = models.TextField(blank=True)
    out_of_scope = models.TextField(
        blank=True, help_text=_('Elements that are explicitly excluded from the contract'))
    common_tos = models.TextField(blank=True)

    tracker = FieldTracker()
    objects = managers.ExpertRequestManager()

    class Meta:
        ordering = ['-created']

    def get_log_fields(self):
        return super(ExpertRequest, self).get_log_fields() + ('state', 'project', 'user')

    @classmethod
    def get_url_name(cls):
        return 'expert-request'

    @property
    def type_label(self):
        offerings = settings.WALDUR_SUPPORT.get('CONTRACT', {}).get('offerings', {})
        type_settings = offerings.get(self.type, {})
        return type_settings.get('label', None)

    @property
    def link(self):
        return settings.WALDUR_EXPERTS['REQUEST_LINK_TEMPLATE'].format(uuid=self.uuid.hex)

    def __str__(self):
        return '{} / {}'.format(self.project.name, self.project.customer.name)


class ExpertBid(core_models.UuidMixin,
                core_models.DescribableMixin,
                PriceMixin,
                structure_models.StructureLoggableMixin,
                structure_models.TimeStampedModel):
    user = models.ForeignKey(core_models.User, related_name='+', on_delete=models.CASCADE,
                             help_text=_('The user which has created this bid.'))
    request = models.ForeignKey(ExpertRequest, on_delete=models.CASCADE, related_name='bids')
    team = models.ForeignKey(structure_models.Project, related_name='+')
    objects = managers.ExpertBidManager()
    tracker = FieldTracker()

    class Meta:
        ordering = ['-created']

    class Permissions(object):
        customer_path = 'request__project__customer'

    def get_log_fields(self):
        return super(ExpertBid, self).get_log_fields() + ('request', 'user', 'price')

    @classmethod
    def get_url_name(cls):
        return 'expert-bid'


class ExpertContract(PriceMixin, core_models.DescribableMixin, structure_models.TimeStampedModel):
    request = models.OneToOneField(ExpertRequest, on_delete=models.CASCADE, related_name='contract')
    team = models.ForeignKey(structure_models.Project, related_name='+', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created']
