from pageindex import PageIndexClient
from dotenv import load_dotenv
load_dotenv()
import os
import json

#init client
pi_client = PageIndexClient(api_key=os.getenv("PAGE_INDEX_API_KEY"))

doc_id = "pi-cmpe2c2vj021701pnfxokeohi"

tree_result  = pi_client.get_tree(doc_id, node_summary=True)
pageindex_tree = tree_result.get("result", [])

print(f"📊 Top-level sections: {len(pageindex_tree)}")
print("\n🌲 Raw tree (first node):")
print(json.dumps(pageindex_tree[0] if pageindex_tree else {}, indent=2))

#save locally
with open("pageindex_tree.json", "w") as f:
    json.dump(pageindex_tree, f, indent=2)