from db.models import Ticket, Order, MovieSession
from typing import Optional
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        dt = parse_datetime(date)
        if dt is None:
            raise ValueError(f"Invalid date format: {date}")

        order = Order(user=user, created_at=dt)

        field = Order._meta.get_field("created_at")
        old_auto_now_add = field.auto_now_add
        field.auto_now_add = False

        order.save(force_insert=True)

        field.auto_now_add = old_auto_now_add
    else:
        order = Order.objects.create(user=user)

    Ticket.objects.bulk_create([
        Ticket(
            movie_session=MovieSession.objects.get(id=t["movie_session"]),
            order=order,
            row=t["row"],
            seat=t["seat"],
        )
        for t in tickets
    ])

    return order


def get_orders(
    username: Optional[str] = None
) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
