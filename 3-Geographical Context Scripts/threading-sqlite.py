import requests
import json
import sqlite3 as sq3
import concurrent.futures


def get_info(row):
    data = {}
    url, lat, lon, state_name = row
    if lat == None or lon == None or state_name != None:
        return data

    url = "https://geo.fcc.gov/api/census/area?lat=" + \
        str(lat) + "&lon=" + str(lon) + "&format=json"
    response = requests.get(url)

    if response.status_code == 400:
        pass
    elif response.status_code == 200:
        parsed = json.loads(response.content)

        if len(parsed["results"]) > 0:
            data["county_fips"] = parsed["results"][0]["county_fips"]
            data["county_name"] = parsed["results"][0]["county_name"]
            data["state_fips"] = parsed["results"][0]["state_fips"]
            data["state_code"] = parsed["results"][0]["state_code"]
            data["state_name"] = parsed["results"][0]["state_name"]

    else:
        print("WEIRD!!!")

    return data


def main():
    conn = sq3.connect("cities.db")

    cur = conn.cursor()
    cur2 = conn.cursor()
    done = 0
    errors = 0

    cur.execute("SELECT count(*) FROM vehicles where state_name is NULL")
    count = cur.fetchone()[0]
    batch_size = 300

    for offset in range(0, count, batch_size):
        cur.execute(
            "SELECT url, lat, long, state_name FROM vehicles where state_name is NULL LIMIT ? OFFSET ?",
            (batch_size, offset))

        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(
                get_info, row): row for row in cur}
            for future in concurrent.futures.as_completed(future_to_url):
                row = future_to_url[future]
                try:
                    data = future.result()
                    done += 1
                    cur2.execute(
                        '''UPDATE vehicles SET county_fips = ?, county_name = ?, state_fips = ?, state_code = ?, state_name = ? WHERE url = ?''',
                        (data["county_fips"], data["county_name"], data["state_fips"],
                         data["state_code"], data["state_name"], row[0]))
                except Exception as exc:
                    # print(row, "generated an error", exc)
                    cur2.execute(
                        '''UPDATE vehicles SET state_name = ? WHERE url = ?''',
                        ("FAILED", row[0]))
                    errors += 1

                if done % 300 == 0:
                    print(done)
                    print('\t', errors)

        conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
