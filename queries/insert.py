def create_nodes(tx, i, a):
     tx.run(
            "MERGE(p:Port {port: $port})"
            "MERGE(h:Host {host: $host})"
            "MERGE (p)-[:OPEN]->(h)",
            host=i['host'],
            port=[i['port_no']]
     )
     
     if a.attacking_ip:
            if a.attacking_ip and a.attacking_hostname is None:
                   a.attacking_hostname = "None"
                   
                   tx.run(
                     "MATCH(h:Host {ip: $ip})"
                     "MERGE(a:Attacker {ip: $attacking_ip, hostname: $attacking_hostname})"
                     "MERGE(a)-[:CONNECTS_TO]->(h)",
                     attacking_hostname=a.attacking_hostname,
                     attacking_ip=a.attacking_ip,
                     ip=h['ip']
                     )