from db.models import Ticket, Order
from typing import Optional
from django.db import transaction
from django.db.models import QuerySet

def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            dt = parse_datetime(date)
            if dt is None:
                raise ValueError(f"Invalid date format: {date}")
            order.created_at = dt
            order.save(update_fields=["created_at"])

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
