import replit
import typing
import abc
def to_primitive(o: typing.Any) -> typing.Any:
    """If object is an observed object, converts to primitve, otherwise returns it.
    Args:
        o (Any): Any object.
    Returns:
        Any: The primitive equivalent if o is Observed
            otherwise o.
    """
    try:
        return o.value
    except:
        return o
def item_to_observed(on_mutate: typing.Callable[[typing.Any], None], item: typing.Any) -> typing.Any:
    """Takes a JSON value and recursively converts it into an Observed value."""
    if isinstance(item, dict):
        # no-op handler so we don't call on_mutate in the loop below
        observed_dict = replit.ObservedDict((lambda _: None), item)
        cb = replit._get_on_mutate_cb(observed_dict)

        for k, v in item.items():
            observed_dict[k] = item_to_observed(cb, v)

        observed_dict._on_mutate_handler = on_mutate
        return observed_dict
    elif isinstance(item, list):
        # no-op handler so we don't call on_mutate in the loop below
        observed_list = replit.ObservedList((lambda _: None), item)
        cb = replit._get_on_mutate_cb(observed_list)

        for i, v in enumerate(item):
            observed_list[i] = item_to_observed(cb, v)

        observed_list._on_mutate_handler = on_mutate
        return observed_list
    else:
        if type(item).__OBSERVED__:
            observed_item = type(item).__OBSERVED__(item)
            cb = replit._get_on_mutate_cb(observed_item)
            for k, v in item.items():
                observed_item.SET_FROM_UNOBSERVED(item_to_observed(cb, v))
            observed_item._on_mutate_handler = on_mutate
            return observed_item
        else:
            return item
class Observed(abc.MutableMapping):
    """A class to extend when you want a class that calls a function every time it is mutated.
    Attributes:
        value (Any): The underlying data.
    """

    __slots__ = ("_on_mutate_handler", "value")
    type = str

    def __init__(
        self, on_mutate: typing.Callable[[typing.Dict], None], value: typing.Optional[typing.Dict] = None
    ) -> None:
        self._on_mutate_handler = on_mutate
        if value is None:
            self.value = type(self).type
        else:
            self.value = value
    def on_mutate(self) -> None:
        """Calls the mutation handler with the underlying dict as an argument."""
        self._on_mutate_handler(self.value)
    def __contains__(self, k: typing.Any) -> bool:
        return self.value.__contains__(k)

    def __getitem__(self, k: typing.Any) -> typing.Any:
        return self.value[k]

    # This should be posititional only but flake8 doesn't like that
    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        """Return the value for key if key is in the dictionary, else default."""
        return self.value.get(
            key, item_to_observed(replit._get_set_cb(db=self, k=key), default)
        )

    def __setitem__(self, k: typing.Any, v: typing.Any) -> None:
        self.value[k] = v
        self.on_mutate()

    def __delitem__(self, k: typing.Any) -> None:
        del self.value[k]
        self.on_mutate()

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return iter(self.value)

    def __len__(self) -> int:
        return len(self.value)

    def __eq__(self, rhs: typing.Any) -> bool:
        return self.value.__eq__(rhs)

    def __imul__(self, rhs: typing.Any) -> typing.Any:
        self.value *= rhs
        self.on_mutate()
        return self.value

    def set_value(self, value: typing.Dict) -> None:
        """Sets the value attribute and triggers the mutation function."""
        self.value = value
        self.on_mutate()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(value={self.value!r})"

from replit import *
database.to_primitive = to_primitive
database.item_to_observed = item_to_observed