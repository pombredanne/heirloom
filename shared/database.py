
class Database():
    def __init__(self, db: str) -> None:
        pass

    def connect(self) -> Engine:

#    def select(self, sql: str, args: Optional[List[ValidSqlArgumentDescription]] = None) -> List[Dict[str, ValidSqlArgumentDescription]]:
#        pass
#
#    def execute(self, sql: str, args: Optional[List[ValidSqlArgumentDescription]] = None) -> int:
#        pass
#
#    def execute_anything(self, sql: str, args: Optional[List[ValidSqlArgumentDescription]] = None, fetch_rows: bool = True) -> Tuple[int, List[Dict[str, ValidSqlArgumentDescription]]]:
#        pass
#
#    def execute_with_reconnect(self, sql: str, args: Optional[List[ValidSqlArgumentDescription]] = None, fetch_rows: Optional[bool] = False) -> Tuple[int, List[ValidSqlArgumentDescription]]:
#        pass
#
#    def insert(self, sql: str, args: Optional[List[ValidSqlArgumentDescription]] = None) -> int:
#        pass
#
#    def begin(self) -> None:
#        pass
#
#    def commit(self) -> None:
#        pass
#
#    def last_insert_rowid(self) -> int:
#        pass
#
#    def get_lock(self, lock_id: str, timeout: int = 1) -> None:
#        pass
#
#    def release_lock(self, lock_id: str) -> None:
#        pass
#
#    def value(self, sql: str, args: Optional[List[ValidSqlArgumentDescription]] = None, default: Any = None, fail_on_missing: bool = False) -> Any:
#        pass
#
#    def values(self, sql: str, args: Optional[List[ValidSqlArgumentDescription]] = None) -> List[Any]:
#        pass
#
#    def nuke_database(self) -> None:
#        pass
#
#def get_database(location: str) -> Database:
#    pass
#
#def sqlescape(s: ValidSqlArgumentDescription, force_string: bool = False, backslashed_escaped: bool = False) -> ValidSqlArgumentDescription:
#    pass
#
#def sqllikeescape(s: str) -> str:
#    pass
