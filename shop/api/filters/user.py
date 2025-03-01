from typing import Optional

from django.db.models import QuerySet
from django_filters import NumberFilter, OrderingFilter, BaseInFilter, CharFilter
from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import FilterSet

from shop.models import User


class CharInFilter(BaseInFilter, CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        query = qs.none()
        for val in value:
            query |= super().filter(qs, val)
        return query


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


def char_to_bool(value: str) -> Optional[bool]:
    """Перевод значения фильтра в bool"""
    if value in (True, 'true', 'True', '1'):
        return True
    if value in (False, 'false', 'False', '0'):
        return False
    if value == 1:
        return True
    if value == 0:
        return False
    return None


class BoolFilter(CharFilter):

    def filter(self, qs, value):
        """
        Булевый фильтр, который может принимать на вход 0, 1, True/false и преобразует значения в bool.

        Взято из django_filters.filters.Filter.filter

        Args:
            qs: Объект запроса
            value: Значение фильтра
        """
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        value = char_to_bool(value)
        qs = self.get_method(qs)(**{self.field_name: value})
        return qs


class UserListFilter(FilterSet):
    is_sealer = BoolFilter(method='filter_is_sealer')

    class Meta:
        model = User
        fields = {
            'id': ['in'],
        }

    order_by_field = 'ordering'
    ordering = OrderingFilter(
        fields=(
            ('username', 'username'),
        )
    )

    @staticmethod
    def filter_is_sealer(queryset: QuerySet[User], name: str, value: str) -> QuerySet[User]:
        """
        Фильтрация по пользователям, которые являются начальниками.

        Args:
            name: Название параметра
            queryset: Объект запроса
            value: Значение фильтра
        """
        value = char_to_bool(value)
        if value in EMPTY_VALUES:
            return queryset

        queryset = queryset.filter(is_sealer=value)
        return queryset
