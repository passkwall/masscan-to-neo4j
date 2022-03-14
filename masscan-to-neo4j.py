#!/usr/bin/python3

import argparse
import re
from neo4j import GraphDatabase
from queries import insert

def check_attacking_args(a):
     if a.attacking_hostname and not a.attacking_ip:
          print("[!] - Attacking-host needs to be supplied with an attacking-ip (-ai / --attacking-ip).")
          exit()

def create_arg_parser():
     parser = argparse.ArgumentParser(description="Masscan-to-Neo4j Graph Database Utility")
     parser.add_argument(
          "-b",
          "--bolt",
          action="store",
          dest="bolt",
          help="Address of your bolt connector. Default, '127.0.0.1'",
          required=False,
          default="127.0.0.1",
     )
     parser.add_argument(
          "-u",
          "--username",
          action="store",
          dest="neo_user",
          help="Username of the Neo4j user.  Default, 'neo4j'.",
          required=False,
          default="neo4j",
     )
     parser.add_argument(
          "-p",
          "--password",
          dest="neo_pass",
          help="Password of the Neo4j user.",
          required=True,
     )
     parser.add_argument(
          "-P",
          "--port",
          dest="neo_port",
          help="Port of the bolt instance if not 7687.",
          required=False,
          default="7687",
     )
     parser.add_argument(
          "-f",
          "--file",
          dest="masscan_file",
          help="Scan of the grepable masscan file (-oG flag).",
          required=True,
     )
     parser.add_argument(
          "-ah",
          "--attacking-host",
          dest="attacking_hostname",
          help="Hostname of the attacking machine.",
     )
     parser.add_argument(
          "-ai",
          "--attacking-ip",
          dest="attacking_ip",
          help="IP address of the attacking machine.",
     )
     return parser

def create_neo4j_driver(bolt, neo_port, neo_user, neo_pass):
     uri = "neo4j://{}:{}".format(bolt, neo_port)
     print("Connecting to {}".format(uri))
     driver = GraphDatabase.driver(uri, auth=(neo_user, neo_pass))
     return driver

def open_masscan_file(file):
     return open(file, 'r')

def parse_masscan_file(file):
     host_regex_pattern = "([0-9]{1,3}\.){3}([0-9]{1,3})"
     port_data_pattern = "[0-9]{1,5}/[a-z]{0,8}/[a-z]{0,8}//[a-z]{0,10}//"
     entries = []
     masscan = open_masscan_file(file)
     for line in masscan:
          if "Host" in line:
               host_ip = re.search(host_regex_pattern, line).group()
               port_data = re.search(port_data_pattern, line).group()
               port_data = parse_port_protocol_info(port_data)
               port_data['host'] = host_ip
               entries.append(port_data)
     
     return entries

def parse_port_protocol_info(info):
     info = info.split("/")
     details = {
          'port_no': info[0],
          'port_status': info[1],
          'port_proto': info[2],
          'service_type': info[4]
     }
     return details

def populate_neo4j_database(data, driver, a):
     for entry in data:
          with driver.session() as session:
               session.write_transaction(insert.create_nodes, entry, a)

if __name__ == "__main__":
     arg_paser = create_arg_parser()
     args = arg_paser.parse_args()

     check_attacking_args(args)

     driver = create_neo4j_driver(args.bolt, args.neo_port, args.neo_user, args.neo_pass)
     parsed_masscan_data = parse_masscan_file(args.masscan_file)

     populate_neo4j_database(parsed_masscan_data, driver, args)

     print("Done Syncing!")