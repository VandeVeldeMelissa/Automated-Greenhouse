from mysql import connector
import os


class Database:

    # 1. open connection with class variabels for reuse
    @staticmethod
    def __open_connection():
        try:
            db = connector.connect(
                option_files=os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "../config.py")
                ),
                autocommit=False,
            )
            if "AttributeError" in (str(type(db))):
                raise Exception("foutieve database parameters in config")
            cursor = db.cursor(dictionary=True, buffered=True)  # lazy loaded
            return db, cursor
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Er is geen toegang tot de database")
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                print("Error: De database is niet gevonden")
            else:
                print(err)
            return

    # 2. Executes READS
    @staticmethod
    def get_rows(sqlQuery, params=None):
        result = None
        db, cursor = Database.__open_connection()
        try:

            cursor.execute(sqlQuery, params)

            result = cursor.fetchall()
            cursor.close()
            if result is None:
                print(ValueError(f"Resultaten zijn onbestaand.[DB Error]"))
            db.close()
        except Exception as error:
            print(error)  # development message
            result = None
        finally:
            return result

    @staticmethod
    def get_one_row(sqlQuery, params=None):
        db, cursor = Database.__open_connection()
        try:
            cursor.execute(sqlQuery, params)
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                raise ValueError("Resultaten zijn onbestaand.[DB Error]")
        except Exception as error:
            print(error)  # development message
            result = None
        finally:
            db.close()
            return result

    # 3. Executes INSERT, UPDATE, DELETE with PARAMETERS
    @staticmethod
    def execute_sql(sqlQuery, params=None):
        result = None
        db, cursor = Database.__open_connection()
        try:
            cursor.execute(sqlQuery, params)
            db.commit()
            # confirmation create (int of 0)
            result = cursor.lastrowid
            # confirmation update, delete (array)
            # result = result if result != 0 else params  # Extra check!!
            if result != 0:  # is an insert, this sends lastrowid response back.
                result = result
            else:  # is an update or a delete
                if cursor.rowcount == -1:  # There is an error in the SQL
                    raise Exception("Fout in SQL")
                elif (
                    cursor.rowcount == 0
                ):  # Nothing has changed, where voldoet niet of geen wijziging in de data
                    result = 0
                elif result == "undefined":  # Hoeveel rijen werden gewijzigd
                    raise Exception("SQL error")
                else:
                    result = cursor.rowcount
        except connector.Error as error:
            db.rollback()
            result = None
            print(f"Error: Data niet bewaard.{error.msg}")
        finally:
            cursor.close()
            db.close()
            return result
