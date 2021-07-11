import psycopg2
from psycopg2 import sql
import os


class Database:
    db_url = ""

    def __init__(self) -> None:
        try:
            self.db_url = os.environ['DATABASE_URL']
        except KeyError:
            print("DATABASE_URL not set. Quitting...")
            quit()

    def get_triggers(self) -> dict:
        triggers = {}
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT
                                   trigger.trigger_rpn,
                                   response.response,
                                   response.bias,
                                   response.as_reply
                               FROM trigger INNER JOIN response
                                   ON trigger.id = response.trigger
                               WHERE trigger.approved = TRUE;""")

                for trigger, response, bias, as_reply in cur.fetchall():
                    r = {
                        'response': response,
                        'bias': bias,
                        'as_reply': as_reply
                    }

                    try:
                        triggers[trigger].append(r)
                    except KeyError:
                        triggers[trigger] = [r]

        return triggers

    def get_api_key(self, key) -> str:
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL("""SELECT key FROM api_key
                                       WHERE name = {};""")
                            .format(sql.Literal(key)))

                return cur.fetchall()[0][0]


db = Database()
