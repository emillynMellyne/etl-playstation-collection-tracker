def create_table(engine, metadata):
    with engine.connect() as conn:
        metadata.create_all(engine)
        conn.close()


def insert_values(table, engine, rows_to_insert):
    with engine.connect() as conn:
        conn = engine.connect()
        conn.execute(table.insert(), rows_to_insert)
        conn.commit()
        conn.close()
