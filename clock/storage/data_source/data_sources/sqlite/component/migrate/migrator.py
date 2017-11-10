from clock.storage.data_source.data_sources.sqlite.component.component import SqliteStorageComponent
from clock.storage.data_source.data_sources.sqlite.component.components.version_info import VersionInfoSqliteComponent
from clock.storage.data_source.data_sources.sqlite.component.migrate.strategies.create import SqliteCreateMigration
from clock.storage.data_source.data_sources.sqlite.component.migrate.strategies.none import SqliteNoMigration
from clock.storage.data_source.data_sources.sqlite.component.migrate.strategies.upgrade_or_downgrade import \
    SqliteUpgradeOrDowngradeMigration


MIGRATION_TYPE_CREATE = "create"
MIGRATION_TYPE_UPGRADE = "upgrade"
MIGRATION_TYPE_DOWNGRADE = "downgrade"
MIGRATION_TYPE_NONE = "none"
MIGRATION_TYPE_UNKNOWN = "unknown"


class SqliteComponentMigrator:
    def __init__(self, component: SqliteStorageComponent, version_info: VersionInfoSqliteComponent):
        self.component = component
        self.version_info = version_info
        self.old_version = version_info.get_version(self.component.name)
        self.new_version = self.component.version
        self.migration_type = self._get_migration_type()

    def _get_migration_type(self):
        if self.old_version is None:
            return MIGRATION_TYPE_CREATE
        elif self.old_version < self.new_version:
            return MIGRATION_TYPE_UPGRADE
        elif self.old_version > self.new_version:
            return MIGRATION_TYPE_DOWNGRADE
        elif self.old_version == self.new_version:
            return MIGRATION_TYPE_NONE
        else:
            return MIGRATION_TYPE_UNKNOWN

    def migrate(self):
        migration_strategy = self._get_migration_strategy()
        migration_strategy.migrate()

    def _get_migration_strategy(self):
        migration_args = (self.component, self.version_info, self.migration_type, self.old_version, self.new_version)
        if self.migration_type == MIGRATION_TYPE_CREATE:
            return SqliteCreateMigration(*migration_args)
        elif self.migration_type in (MIGRATION_TYPE_UPGRADE, MIGRATION_TYPE_DOWNGRADE):
            return SqliteUpgradeOrDowngradeMigration(*migration_args)
        elif self.migration_type == MIGRATION_TYPE_NONE:
            return SqliteNoMigration(*migration_args)
        else:
            raise MigrationStrategyNotFound(self.component, self.migration_type)


class SqliteComponentMigratorException(Exception):
    def __init__(self, component: SqliteStorageComponent, migration_type: str, message: str):
        super().__init__(
            "Component '{name}' {type} migration failed with error: {message}. "
            "Component was not migrated. "
            "Unexpected things may happen."
            .format(name=component.name, type=migration_type, message=message)
        )


class MigrationStrategyNotFound(SqliteComponentMigratorException):
    def __init__(self, component: SqliteStorageComponent, migration_type: str):
        super().__init__(
            component, migration_type,
            "no migration strategy found"
        )
