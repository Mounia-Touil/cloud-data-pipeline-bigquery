from flask import Flask, jsonify
from google.cloud import bigquery

app = Flask(__name__)

@app.route("/")
def get_data():
    client = bigquery.Client()

    query = """
    SELECT 
      c.name,
      c.dns_host_name,
      d.host_name,
      d.ipv4_address
    FROM `ksu-team-2.capstone_dev.computer` c
    LEFT JOIN `ksu-team-2.capstone_dev.dns_a_record` d
      ON LOWER(c.dns_host_name) LIKE CONCAT('%', LOWER(d.host_name), '%')
    LIMIT 20
    """

    results = client.query(query).result()

    data = []
    for row in results:
        data.append({
            "name": row.name,
            "dns": row.dns_host_name,
            "host": row.host_name,
            "ip": row.ipv4_address
        })

    return jsonify(data)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)