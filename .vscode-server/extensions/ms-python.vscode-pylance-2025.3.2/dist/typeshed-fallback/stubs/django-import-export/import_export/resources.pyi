import _typeshed
from collections import OrderedDict
from collections.abc import Iterator, Sequence
from functools import partial
from logging import Logger
from typing import Any, ClassVar, Generic, Literal, NoReturn, TypeVar, overload
from typing_extensions import TypeAlias, deprecated

from django.db.models import Field as DjangoField, Model, QuerySet
from django.utils.safestring import SafeString

from .declarative import DeclarativeMetaclass, ModelDeclarativeMetaclass
from .fields import Field
from .instance_loaders import BaseInstanceLoader
from .options import ResourceOptions
from .results import Error, Result, RowResult
from .widgets import ForeignKeyWidget, ManyToManyWidget, Widget

Dataset: TypeAlias = _typeshed.Incomplete  # tablib.Dataset
logger: Logger

def has_natural_foreign_key(model: Model) -> bool: ...

class Diff:
    left: list[str]
    right: list[str]
    new: bool
    def __init__(self, resource: Resource[_ModelT], instance: _ModelT, new: bool) -> None: ...
    def compare_with(self, resource: Resource[_ModelT], instance: _ModelT, dry_run: bool = False) -> None: ...
    def as_html(self) -> list[SafeString]: ...

_ModelT = TypeVar("_ModelT", bound=Model)

class Resource(Generic[_ModelT], metaclass=DeclarativeMetaclass):
    _meta: ResourceOptions[_ModelT]
    fields: OrderedDict[str, Field]
    create_instances: list[_ModelT]
    update_instances: list[_ModelT]
    delete_instances: list[_ModelT]
    def __init__(self, **kwargs: Any) -> None: ...
    @classmethod
    def get_result_class(self) -> type[Result]: ...
    @classmethod
    def get_row_result_class(self) -> type[RowResult]: ...
    @classmethod
    def get_error_result_class(self) -> type[Error]: ...
    @classmethod
    def get_diff_class(self) -> type[Diff]: ...
    @classmethod
    def get_db_connection_name(self) -> str: ...
    def get_use_transactions(self) -> bool: ...
    def get_chunk_size(self) -> int: ...
    @deprecated("The 'get_fields()' method is deprecated and will be removed in a future release.")
    def get_fields(self, **kwargs: Any) -> list[Field]: ...
    def get_field_name(self, field: Field) -> str: ...
    def init_instance(self, row: dict[str, Any] | None = None) -> _ModelT: ...
    def get_instance(self, instance_loader: BaseInstanceLoader, row: dict[str, Any]) -> _ModelT | None: ...
    def get_or_init_instance(self, instance_loader: BaseInstanceLoader, row: dict[str, Any]) -> tuple[_ModelT | None, bool]: ...
    def get_import_id_fields(self) -> Sequence[str]: ...
    def get_bulk_update_fields(self) -> list[str]: ...
    def bulk_create(
        self,
        using_transactions: bool,
        dry_run: bool,
        raise_errors: bool,
        batch_size: int | None = None,
        result: Result | None = None,
    ) -> None: ...
    def bulk_update(
        self,
        using_transactions: bool,
        dry_run: bool,
        raise_errors: bool,
        batch_size: int | None = None,
        result: Result | None = None,
    ) -> None: ...
    def bulk_delete(self, using_transactions: bool, dry_run: bool, raise_errors: bool, result: Result | None = None) -> None: ...
    def validate_instance(
        self, instance: _ModelT, import_validation_errors: dict[str, Any] | None = None, validate_unique: bool = True
    ) -> None: ...
    # For all the definitions below (from `save_instance()` to `import_row()`), `**kwargs` should contain:
    # dry_run: bool, use_transactions: bool, row_number: int, retain_instance_in_row_result: bool.
    # Users are free to pass extra arguments in `import_data()`so PEP 728 can probably be leveraged here.
    def save_instance(self, instance: _ModelT, is_create: bool, row: dict[str, Any], **kwargs: Any) -> None: ...
    def do_instance_save(self, instance: _ModelT) -> None: ...
    def before_save_instance(self, instance: _ModelT, row: dict[str, Any], **kwargs: Any) -> None: ...
    def after_save_instance(self, instance: _ModelT, row: dict[str, Any], **kwargs: Any) -> None: ...
    def delete_instance(self, instance: _ModelT, row: dict[str, Any], **kwargs: Any) -> None: ...
    def before_delete_instance(self, instance: _ModelT, row: dict[str, Any], **kwargs: Any) -> None: ...
    def after_delete_instance(self, instance: _ModelT, row: dict[str, Any], **kwargs: Any) -> None: ...
    def import_field(self, field: Field, instance: _ModelT, row: dict[str, Any], is_m2m: bool = False, **kwargs: Any) -> None: ...
    def get_import_fields(self) -> list[Field]: ...
    def import_instance(self, instance: _ModelT, row: dict[str, Any], **kwargs: Any) -> None: ...
    def save_m2m(self, instance: _ModelT, row: dict[str, Any], **kwargs: Any) -> None: ...
    def for_delete(self, row: dict[str, Any], instance: _ModelT) -> bool: ...
    def skip_row(
        self, instance: _ModelT, original: _ModelT, row: dict[str, Any], import_validation_errors: dict[str, Any] | None = None
    ) -> bool: ...
    def get_diff_headers(self) -> list[str]: ...
    def before_import(self, dataset: Dataset, **kwargs: Any) -> None: ...
    def after_import(self, dataset: Dataset, result: Result, **kwargs: Any) -> None: ...
    def before_import_row(self, row: dict[str, Any], **kwargs: Any) -> None: ...
    def after_import_row(self, row: dict[str, Any], row_result: RowResult, **kwargs: Any) -> None: ...
    def after_init_instance(self, instance: _ModelT, new: bool, row: dict[str, Any], **kwargs: Any) -> None: ...
    @overload
    def handle_import_error(self, result: Result, error: Exception, raise_errors: Literal[True]) -> NoReturn: ...
    @overload
    def handle_import_error(self, result: Result, error: Exception, raise_errors: Literal[False] = ...) -> None: ...
    def import_row(self, row: dict[str, Any], instance_loader: BaseInstanceLoader, **kwargs: Any) -> RowResult: ...
    def import_data(
        self,
        dataset: Dataset,
        dry_run: bool = False,
        raise_errors: bool = False,
        use_transactions: bool | None = None,
        collect_failed_rows: bool = False,
        rollback_on_validation_errors: bool = False,
        **kwargs: Any,
    ) -> Result: ...
    def import_data_inner(
        self,
        dataset: Dataset,
        dry_run: bool,
        raise_errors: bool,
        using_transactions: bool,
        collect_failed_rows: bool,
        **kwargs: Any,
    ) -> Result: ...
    def get_import_order(self) -> tuple[str, ...]: ...
    def get_export_order(self) -> tuple[str, ...]: ...
    def before_export(self, queryset: QuerySet[_ModelT], **kwargs: Any) -> None: ...
    def after_export(self, queryset: QuerySet[_ModelT], dataset: Dataset, **kwargs: Any) -> None: ...
    def filter_export(self, queryset: QuerySet[_ModelT], **kwargs: Any) -> QuerySet[_ModelT]: ...
    def export_field(self, field: Field, instance: _ModelT, **kwargs: Any) -> str: ...
    def get_export_fields(self, selected_fields: Sequence[str] | None = None) -> list[Field]: ...
    def export_resource(self, instance: _ModelT, selected_fields: Sequence[str] | None = None, **kwargs: Any) -> list[str]: ...
    def get_export_headers(self, selected_fields: Sequence[str] | None = None) -> list[str]: ...
    def get_user_visible_headers(self) -> list[str]: ...
    def get_user_visible_fields(self) -> list[str]: ...
    def iter_queryset(self, queryset: QuerySet[_ModelT]) -> Iterator[_ModelT]: ...
    def export(self, queryset: QuerySet[_ModelT] | None = None, **kwargs: Any) -> Dataset: ...

class ModelResource(Resource[_ModelT], metaclass=ModelDeclarativeMetaclass):
    DEFAULT_RESOURCE_FIELD: ClassVar[type[Field]] = ...
    WIDGETS_MAP: ClassVar[dict[str, type[Widget]]]
    @classmethod
    def get_m2m_widget(cls, field: DjangoField[Any, Any]) -> partial[ManyToManyWidget[Any]]: ...
    @classmethod
    def get_fk_widget(cls, field: DjangoField[Any, Any]) -> partial[ForeignKeyWidget[Any]]: ...
    @classmethod
    def widget_from_django_field(cls, f: DjangoField[Any, Any], default: type[Widget] = ...) -> type[Widget]: ...
    @classmethod
    def widget_kwargs_for_field(cls, field_name: str, django_field: DjangoField[Any, Any]) -> dict[str, Any]: ...
    @classmethod
    def field_from_django_field(cls, field_name: str, django_field: DjangoField[Any, Any], readonly: bool) -> Field: ...
    def get_queryset(self) -> QuerySet[_ModelT]: ...
    def init_instance(self, row: dict[str, Any] | None = None) -> _ModelT: ...
    def after_import(self, dataset: Dataset, result: Result, **kwargs: Any) -> None: ...
    @classmethod
    def get_display_name(cls) -> str: ...

_ResourceT = TypeVar("_ResourceT", bound=Resource[Any])

# HK Type Vars could help type the first overload:
@overload
def modelresource_factory(model: Model, resource_class: type[_ResourceT]) -> _ResourceT: ...
@overload
def modelresource_factory(model: _ModelT) -> ModelResource[_ModelT]: ...
