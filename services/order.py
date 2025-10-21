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

    dt = None
    if date:
        dt = parse_datetime(date)
        if dt is None:
            raise ValueError(f"Invalid date format: {date}")

    order = Order.objects.create(
        user=user,
        created_at=dt if dt else None
    )

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(
    username: Optional[str] = None
) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
