import logging, json
import psycopg2, psycopg2.extras
from psycopg2.extras import LogicalReplicationConnection
from decouple import config


def process_change(message: psycopg2.extras.ReplicationMessage, data_handle_function: callable):
    def parse_data(raw_data: psycopg2.extras.ReplicationMessage):
        # considers all exceptions where data is not relevant to us
        if not raw_data.payload: return
        try:
            data: dict = json.loads(raw_data.payload)
            if not data or "change" not in data or not data["change"]: return
            return data["change"]
        except Exception as e:
            print(f'Error occured while parsing data from CDC: \n{e}', flush=True)
            return
    

    received_data: list[dict] = parse_data(message)
    data_handle_function(received_data)

    # flushes the LSN (marks the data as processed)
    message.cursor.send_feedback(flush_lsn=message.data_start)
    print("LSN flushed", flush=True)


def create_replication_connection(slot_name: str, data_handle_function: callable) -> None:
    # creates a replication connection to postgres
    conn: psycopg2.extensions.connection = psycopg2.connect(
            host=config("LOCALHOST"),
            database=config("DB_DATABASE"),
            user=config("DB_ADMIN_USERNAME"),
            password=config("DB_ADMIN_PASSWORD"),
            port=config("DB_PORT"), connection_factory=LogicalReplicationConnection)

    cur: psycopg2.extras.ReplicationCursor = conn.cursor()
    print("Succesfully connected to Database", flush=True)
    # Creates a replication slot with wal2json if it already exists psycopg2.errors.DuplicateObject is raised
    try:
        cur.execute(f"""SELECT * FROM pg_create_logical_replication_slot('{slot_name}', 'wal2json') """)
        conn.commit()
        logging.info("Replication slot created")
    except psycopg2.errors.DuplicateObject:
        logging.info("Replication slot already exists")

    # Start the replication stream and limits it to only the flight table
    options: dict = {"add-tables": config("TABLES")}
    cur.start_replication(slot_name=f'{slot_name}', decode=True, options=options)
    logging.info("Replication started")
    
    cur.consume_stream(lambda msg: process_change(msg, data_handle_function))

    cur.close()
    conn.close()
