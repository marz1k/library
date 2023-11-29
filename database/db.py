import asyncpg as sql


class DataBase:
    def __init__(self, host: str, database: str, password: str, user: str = 'postgres', port: str = '5432'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    async def create_db(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)

        await con.execute("CREATE TABLE IF NOT EXISTS books("
                          "name VARCHAR,"
                          "author VARCHAR,"
                          "genre VARCHAR,"
                          "description VARCHAR)")

        await con.execute("CREATE TABLE IF NOT EXISTS genres("
                          "genre VARCHAR)")

    async def execute(self, query, *args):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute(query, *args)
        await con.close()

    async def fetchrow(self, query, *args):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow(query, *args)
        await con.close()
        return data

    async def fetch(self, query, *args):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch(query, *args)
        await con.close()
        return data

    async def add_book(self, name: str, author: str, genre: str, description: str):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("INSERT INTO books(name, author, genre, description) VALUES($1, $2, $3, $4)",
                          name, author, genre, description)

        # Checking if genre already in GENRES table. If not -> adding.
        genres = await con.fetch("SELECT genre FROM genres WHERE genre = $1", genre)
        if len(genres) == 0:
            await con.execute("INSERT INTO genres(genre) VALUES($1)", genre)

        await con.close()

    async def delete_book(self, book_id: int):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        await con.execute("DELETE FROM books WHERE book_id = $1", book_id)
        await con.close()

    async def find_book(self, key: str):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM books WHERE "
                               "LOWER(name) LIKE '%' || LOWER($1) || '%' "
                               "or LOWER(author) LIKE '%' || LOWER($1) || '%' ", key.lower())
        return data

    async def select_all_books(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM books")
        return data

    async def select_book_by_genre(self, genre: str):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT * FROM books WHERE genre = $1", genre)
        return data

    async def select_book_by_id(self, book_id: int):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetchrow("SELECT * FROM books WHERE book_id = $1", book_id)
        return data

    async def select_all_genres(self):
        con = await sql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password)
        data = await con.fetch("SELECT genre FROM genres")
        return data
