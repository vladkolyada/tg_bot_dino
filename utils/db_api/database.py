import asyncio
import asyncpg

from data import config


class DataBase:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.PGUSER,
                database=config.DBNAME,
                password=config.PGPASSWORD,
                host=config.IP,
                port=config.DBPORT,
                loop=loop
            )
        )

    async def create_table_users(self):
        await self.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS users_dino(
            id BIGINT NOT NULL PRIMARY KEY, 
            first_name VARCHAR(70),
            last_name VARCHAR(80),
            nickname VARCHAR(60),
            active INTEGER NOT NULL
            );
            """
        )

    async def add_new_user_to_the_table(self, id, first_name, last_name, nickname):
        sql = "INSERT INTO users_dino(id, first_name, last_name, nickname, active) " \
              "VALUES($1, $2, $3, $4, 1);"
        try:
            await self.pool.execute(sql, id, first_name, last_name, nickname)
        except asyncpg.exceptions.UniqueViolationError:
            pass

    async def take_a_data(self, id):
        sql = "SELECT first_name, last_name, nickname FROM users_dino WHERE id=$1;"
        try:
            async with self.pool.acquire() as conn:
                user_data = await conn.fetch(sql, id)

                answer = []
                for i in user_data:
                    answer.append([i[0], i[1], i[2]])
                    # 0 - first_name; 1 - last_name; 2 - nickname.
                return answer
        except asyncpg.exceptions.UniqueViolationError:
            pass

    async def set_active(self, id, active):
        sql = "UPDATE users_dino SET active=$1 WHERE id=$2;"
        try:
            await self.pool.execute(sql, active, id)
        except asyncpg.exceptions.UniqueViolationError:
            pass

    async def get_all_users(self):
        sql = "SELECT id, active FROM users_dino;"
        try:
            async with self.pool.acquire() as conn:
                all_users = await conn.fetch(sql)

                users = []
                for i in all_users:
                    users.append([i[0], i[1]])
                return users
        except asyncpg.exceptions.UniqueViolationError:
            pass
