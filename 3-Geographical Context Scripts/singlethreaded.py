import requests
import json
import sqlite3 as sq3


def get_info(lat, lon):
    url = "https://geo.fcc.gov/api/census/area?lat=" + \
        str(lat) + "&lon=" + str(lon) + "&format=json"
    response = requests.get(url)

    data = {}

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

    cur.execute("SELECT count(*) FROM vehicles where state_name is NULL")
    count = cur.fetchone()[0]
    batch_size = 100

    for offset in range(0, count, batch_size):
        cur.execute(
            "SELECT url, lat, long, state_name FROM vehicles where state_name is NULL LIMIT ? OFFSET ?",
            (batch_size, offset))

        for row in cur:
            url, lat, lon, state_name = row
            if lat == None or lon == None or state_name != None:
                continue
            data = get_info(lat, lon)
            if not data:
                continue

            cur2.execute(
                '''UPDATE vehicles SET county_fips = ?, county_name = ?, state_fips = ?, state_code = ?, state_name = ? WHERE url = ?''',
                (data["county_fips"], data["county_name"], data["state_fips"],
                 data["state_code"], data["state_name"], url))

            done += 1
            if done % 100 == 0:
                print(done)

        conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
