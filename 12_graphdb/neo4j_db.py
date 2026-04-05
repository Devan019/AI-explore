from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
load_dotenv()

url =  os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE")

driver = GraphDatabase.driver(url, auth=(username, password))


def clean_node(node):
    data = dict(node)
    data.pop("embedding", None)  # remove vector field safely
    return data


def get_graph(tx):
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    """
    result = tx.run(query)

    data = []
    for record in result:
        n = record["n"]
        r = record["r"]
        m = record["m"]

        data.append({
            "source": clean_node(n),
            "relationship": r.type,
            "target": clean_node(m)
        })

    return data
with driver.session() as session:
    graph_data = session.execute_read(get_graph)

for item in graph_data:
    print(item)
