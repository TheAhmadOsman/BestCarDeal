import psycopg2
import concurrent.futures

conn = psycopg2.connect(database="cars", user="postgres",
                        password="yourpsqlpassword", host="127.0.0.1", port="5432")


def main():
    states = {}
    with open("stateweathervals.txt") as f:
        for line in f:
            line = line.strip()
            line = line.replace(': ', ':')
            line = line.split(':')
            states[line[0]] = int(line[1])

    cur = conn.cursor()

    for key, value in states.items():
        cur.execute(
            '''UPDATE vehicles SET weather = %s WHERE state_name = %s''', (value, key, ))
        conn.commit()
        print("Done", key)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
