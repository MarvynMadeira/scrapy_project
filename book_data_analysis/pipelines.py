import psycopg2
from psycopg2.extras import RealDictCursor


class PostgresPipeline(object):

    def __init__(self):
        self.cur = None

    def open_spider(self, spider):
        print('Conectando spider ao PostgreSQL...')
        dsn = "postgresql://root:amazonDB@localhost:5432/booksDB"

        self.connection = psycopg2.connect(dsn=dsn)
        print('Conexão PostgreSQL bem-sucedida')
        self.cur = self.connection.cursor()

        self.cur.execute("""
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            
            CREATE TABLE IF NOT EXISTS Livros_Amazon_Data (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                title TEXT,
                code TEXT,
                url TEXT,
                currency TEXT,
                present_price INTEGER, 
                created_at TIMESTAMP
            );
        """)
        self.connection.commit()
        print('tabela criada com sucesso!')

    def process_item(self, item, spider):
        print("process_item chamado com:", item)
        try:
            self.cur.execute("""
                INSERT INTO Livros_Amazon_Data (
                    title, code, url, currency, present_price,
                    created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                item.get('title'),
                item.get('code'),
                item.get('url'),
                item.get('currency'),
                item.get('present_price'),
                item.get('created_at')
            ))
            self.connection.commit()
        except Exception as e:
            spider.logger.error(f'Erro ao inserir dados no PostgreSQL: {e}')
            self.connection.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.logger.info('Fechando conexão com PostgreSQL...')
        self.cur.close()
        self.connection.close()
