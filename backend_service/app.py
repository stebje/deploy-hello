from flask import Flask, jsonify
import psycopg2
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_PORT = os.getenv('DB_PORT', '5432')

def get_greeting():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT message FROM greetings LIMIT 1;")
    message = cur.fetchone()[0]
    cur.close()
    conn.close()
    return message

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/greeting', methods=['GET'])
def greeting():
    try:
        message = get_greeting()
        return jsonify({"message": message}), 200
    except Exception as e:
        logger.error("Error fetching greeting: %s", str(e))
        return jsonify({"error": str(e)}), 500

def initialize_database():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cur = conn.cursor()
        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS greetings (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL
            );
        """)
        # Check if the message exists
        cur.execute("SELECT COUNT(*) FROM greetings;")
        count = cur.fetchone()[0]
        if count == 0:
            # Insert the "Hello World" message
            cur.execute("INSERT INTO greetings (message) VALUES (%s);", ("Hello World",))
            conn.commit()
        cur.close()
        conn.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error("Error initializing database: %s", str(e))

#@app.before_first_request
#def setup():

if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=80)