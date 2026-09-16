"""Вычислитель эталонных результатов для SQL-задач.

Каждый кейс — dict {ddl, query, hidden}:
  - ddl    : строка с CREATE TABLE + INSERT (несколько операторов);
  - query  : эталонный SQL-запрос, результат которого и будет expected;
  - hidden : True для скрытого теста.
expected вычисляется реальным прогоном в SQLite, поэтому всегда корректен.
"""
import sqlite3


def sql_cases(items):
    """Вернуть список кейсов в формате genlib.build_sql_problem.

    Каждый элемент items: {"ddl": str, "query": str, "hidden": bool}.
    """
    out = []
    for it in items:
        con = sqlite3.connect(":memory:")
        try:
            con.executescript(it["ddl"])
            exp = [list(r) for r in con.execute(it["query"]).fetchall()]
        finally:
            con.close()
        out.append({
            "schema": it["ddl"],
            "expected": exp,
            "hidden": bool(it.get("hidden", False)),
        })
    return out