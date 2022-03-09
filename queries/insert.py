def create_nodes(tx, i):
     tx.run(
            "MERGE(p:Port {port: $port})"
            "MERGE(h:Host {host: $host})"
            "MERGE (p)-[:OPEN]->(h)",
            host=i['host'],
            port=[i['port_no']]
     )