import requests
import json
import psycopg2
import concurrent.futures
import time

conn = psycopg2.connect(database="cars", user="postgres",
                        password="postgresqlpassword!!!", host="127.0.0.1", port="5432")


def get_info(row):
    data = {}
    url, lat, lon, state_name = row

    cur = conn.cursor()

    if lat == None or lon == None:
        cur.execute(
            '''UPDATE vehicles SET state_name = %s WHERE url = %s''',
            ("FAILED", row[0], ))
        conn.commit()
        cur.close()
        return True

    url = "https://geo.fcc.gov/api/census/area?lat=" + \
        str(lat) + "&lon=" + str(lon) + "&format=json"

    response = requests.get(url)
    if response.status_code == 400:
        try:
            cur.execute(
                '''UPDATE vehicles SET state_name = %s WHERE url = %s''',
                ("FAILED", row[0], ))
            conn.commit()
            cur.close()
        except:
            raise Exception("Failed!")
    elif response.status_code == 200:
        parsed = json.loads(response.content)

        if len(parsed["results"]) > 0:
            data["county_fips"] = parsed["results"][0]["county_fips"]
            data["county_name"] = parsed["results"][0]["county_name"]
            data["state_fips"] = parsed["results"][0]["state_fips"]
            data["state_code"] = parsed["results"][0]["state_code"]
            data["state_name"] = parsed["results"][0]["state_name"]
            try:
                cur.execute(
                    '''UPDATE vehicles SET county_fips = %s, county_name = %s, state_fips = %s, state_code = %s, state_name = %s WHERE url = %s''',
                    (data["county_fips"], data["county_name"], data["state_fips"],
                     data["state_code"], data["state_name"], row[0], ))
                conn.commit()
                cur.close()
            except Exception as e:
                raise Exception("Failed here dude :(!", e, parsed["results"])
        else:
            cur.execute(
                '''UPDATE vehicles SET state_name = %s WHERE url = %s''',
                ("FAILED", row[0], ))
            conn.commit()
            cur.close()
    else:
        print("WEIRD!!!")

    return True


def main():
    cur = conn.cursor()
    done = 0
    errors = 0

    cur.execute("SELECT count(*) FROM vehicles where state_name is NULL")
    count = cur.fetchone()[0]

    BATCHSIZE = 50000
    CONNECTIONS = 5000

    for offset in range(0, count, BATCHSIZE):
        cur.execute(
            "SELECT url, lat, long, state_name FROM vehicles where state_name is NULL LIMIT %s OFFSET %s",
            (BATCHSIZE, offset, ))

        with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
            future_to_url = {executor.submit(
                get_info, row): row for row in cur}

            time1 = time.time()
            for future in concurrent.futures.as_completed(future_to_url):
                row = future_to_url[future]
                try:
                    done += 1
                    future.result()
                except Exception as exc:
                    print(row, "generated an error", exc)
                    errors += 1
                if done % CONNECTIONS == 0:
                    print(done)
                    print('    ', errors)
                conn.commit()
            time2 = time.time()

        print(f'Took {time2-time1:.2f} s')

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
