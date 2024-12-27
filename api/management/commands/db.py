from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def execute_query(title, price, photo, description):
    try:
        with psycopg2.connect(
            dbname=os.getenv("NAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        ) as conn:  
            with conn.cursor() as cur:  
                insert_query = "INSERT INTO api_book(title, price, photo, description) VALUES(%s, %s, %s, %s)"
                data_to_insert = (title, price, photo, description)

                cur.execute(insert_query, data_to_insert)
                conn.commit()  

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

