from django.db import connection
from django.db import transaction

from checkpoint.helpers.Exception import CustomException
from checkpoint.helpers.Database import Database as DBHelper


class Domain:

    # Table: domain



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int = 0, assetId: int = 0, domain: str = "") -> dict:
        c = connection.cursor()

        try:
            if id:
                c.execute("SELECT * FROM `domain` WHERE id = %s", [id])
            if assetId and domain:
                c.execute("SELECT * FROM `domain` WHERE `domain` = %s AND id_asset = %s", [domain, assetId])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent domain"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(id: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM `domain` WHERE `id` = %s", [id])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(assetId, domain) -> int:
        c = connection.cursor()

        try:
            with transaction.atomic():
                c.execute("INSERT INTO `domain` (id_asset, `domain`) VALUES (%s, %s)", [
                    assetId,
                    domain
                ])

                return c.lastrowid
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "Duplicated domain"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
