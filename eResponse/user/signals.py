from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from .models import User


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner


@receiver([m2m_changed, post_save], sender=User)
@on_transaction_commit
def group_signal(sender, instance: User, **kwargs):
    """
    group_signal gets or create >Group and adds it to
    model instance
    m2m field is only effective after the parent instance is saved
    post_save signal ensures m2m_changed is called by emitting done
    :return: None
    """
    experts: QuerySet = Group.objects.filter(name='experts')

    if not experts.exists():

        experts: QuerySet = Group.objects.filter(
            name=Group.objects.create(name='experts').name)

    instance.groups.add(experts.get())
