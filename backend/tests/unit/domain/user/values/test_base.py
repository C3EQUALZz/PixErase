from dataclasses import FrozenInstanceError, dataclass, field, fields
from typing import ClassVar

import pytest

from pix_erase.domain.common.errors.base import DomainFieldError
from pix_erase.domain.common.values.base import BaseValueObject
from tests.unit.factories.value_objects import (
    create_multi_field_vo,
    create_single_field_vo,
)


def test_child_cannot_init_with_no_instance_fields() -> None:
    # Arrange
    @dataclass(frozen=True)
    class EmptyVO(BaseValueObject):
        def _validate(self) -> None: ...

        def __str__(self) -> str:
            return ""

    # Act & Assert
    with pytest.raises(DomainFieldError):
        EmptyVO()


def test_child_cannot_init_with_only_class_fields() -> None:
    # Arrange
    @dataclass(frozen=True)
    class ClassFieldsVO(BaseValueObject):
        foo: ClassVar[int] = 0
        bar: ClassVar[str] = "baz"

        def _validate(self) -> None: ...

        def __str__(self) -> str:
            return ""

    # Act & Assert
    with pytest.raises(DomainFieldError):
        ClassFieldsVO()


def test_class_field_not_in_dataclass_fields() -> None:
    # Arrange
    @dataclass(frozen=True)
    class MixedFieldsVO(BaseValueObject):
        foo: ClassVar[int] = 0
        bar: str

        def _validate(self) -> None: ...

        def __str__(self) -> str: ...

    sut = MixedFieldsVO(bar="baz")

    # Act
    sut_fields = fields(sut)

    # Assert
    assert len(sut_fields) == 1
    assert sut_fields[0].name == "bar"
    assert sut_fields[0].type is str
    assert getattr(sut, sut_fields[0].name) == "baz"


def test_class_field_not_broken_by_slots() -> None:
    # Arrange
    @dataclass(frozen=True, slots=True)
    class MixedFieldsVO(BaseValueObject):
        foo: ClassVar[int] = 0
        bar: str

        def _validate(self) -> None: ...

        def __str__(self) -> str:
            return ""

    # Assert
    assert MixedFieldsVO.foo == 0


def test_class_field_final_equivalence() -> None:
    # Arrange
    @dataclass(frozen=True)
    class MixedFieldsVO:
        a: ClassVar[int] = 1
        b: ClassVar[str] = "bar"
        c: str = "baz"

    # Act
    sut_field_names = [f.name for f in fields(MixedFieldsVO)]

    # Assert
    assert sut_field_names == ["c"]


def test_is_immutable() -> None:
    # Arrange
    vo_value = 123
    sut = create_single_field_vo(vo_value)

    # Act & Assert
    with pytest.raises(FrozenInstanceError):
        # noinspection PyDataclass
        sut.value = vo_value + 1  # type: ignore[misc]


def test_equality() -> None:
    # Arrange
    vo1 = create_multi_field_vo()
    vo2 = create_multi_field_vo()

    # Assert
    assert vo1 == vo2


def test_inequality() -> None:
    # Arrange
    vo1 = create_multi_field_vo(value2="one")
    vo2 = create_multi_field_vo(value2="two")

    # Assert
    assert vo1 != vo2


def test_class_field_not_in_repr() -> None:
    # Arrange
    @dataclass(frozen=True, repr=False)
    class MixedFieldsVO(BaseValueObject):
        baz: int
        foo: ClassVar[int] = 0
        bar: ClassVar[str] = "baz"

        def _validate(self) -> None: ...

        def __str__(self) -> str:
            return "baz"

    sut = MixedFieldsVO(baz=1)
    sut2 = MixedFieldsVO(baz=1)

    # Act
    result = repr(sut)
    result2 = repr(sut2)

    # Assert
    assert result == result2


def test_hidden_field_not_in_repr() -> None:
    # Arrange
    @dataclass(frozen=True, repr=False)
    class HiddenFieldVO(BaseValueObject):
        visible: int
        hidden: int = field(repr=False)

        def _validate(self) -> None: ...

        def __str__(self) -> str:
            return str(self.hidden)

    sut = HiddenFieldVO(123, 456)
    sut2 = HiddenFieldVO(123, 123123)

    # Act
    result = repr(sut)
    result2 = repr(sut2)

    # Assert
    assert result == result2


def test_all_fields_hidden_repr() -> None:
    # Arrange
    @dataclass(frozen=True, repr=False)
    class HiddenFieldVO(BaseValueObject):
        hidden_1: int = field(repr=False)
        hidden_2: int = field(repr=False)

        def _validate(self) -> None: ...

        def __str__(self) -> str:
            return str(self.hidden_1) + str(self.hidden_2)

    sut = HiddenFieldVO(123, 456)
    an_sut = HiddenFieldVO(256, 123)

    # Act
    result = repr(sut)
    result2 = repr(an_sut)

    # Assert
    assert result == result2
