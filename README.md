# masscan-to-neo4j
Simple python script for importing Masscan results to a Neo4j Graph Database.

> [For a version to use with Nmap, click here.](https://github.com/passkwall/nmap-to-neo4j)


![](2022-03-09_14-32-11.png)

## Usage

First, run a Masscan scan in your network. Save the results with the greppable flag (`-oG`).
```
sudo masscan 192.168.1.1/24 --top-ports=100 -oG masscan_results
```

Now start your Neo4j instance and run the `masscan-to-neo4j.py` script.
```
python3 masscan-to-neo4j.py -p neo4j_password -f masscan_results
```


## Installation Prerequisites 
1. [Neo4j Community Edition](https://neo4j.com/download-center/) (tested on 4.4.4)
2. Python3
3. Python virtualenv (recommended)


## Setup
```
virtualenv venv
pip3 install -r requirements
```

## Querying Results
Neo4j is complicated at times, but this tool is super simple. I generally recommend a few of the following queries:


#### Find and return all ports
```
match (a:Port) return a
```

#### Find and return all hosts
```
match (a:Host) return a
```

#### Find and return a specific host and its ports
```
MATCH (p:Port)-[:OPEN]->(h:Host) where h.host = "192.168.1.18" return p,h
```

[Here is a Cheat Sheet for Cypher you can refer to](https://neo4j.com/docs/cypher-refcard/current/) in case you want to learn more. 