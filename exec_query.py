import sqlite3

def main() -> None:

    with sqlite3.connect('occurrences.db') as conn:
        cursor = conn.execute(
            "UPDATE occurrences SET username = ? WHERE id = ?",
            ("flavio", 2)
        )
        print(f"{cursor.rowcount} linha(s) atualizada(s)")

if __name__ == "__main__":
    main()