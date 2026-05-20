import json
import os
from dotenv import load_dotenv
load_dotenv()
from pageindex import PageIndexClient
from helpers.Client import GroqClient

client = GroqClient().client

pi_client = PageIndexClient(api_key=os.getenv("PAGE_INDEX_API_KEY"))

doc_id = "pi-cmpe2c2vj021701pnfxokeohi"

tree_result  = pi_client.get_tree(doc_id, node_summary=True)

pageindex_tree = tree_result.get("result", [])

def llm_tree_search(query: str, tree: list, model: str = "openai/gpt-oss-20b") -> dict:
    """
    Core PageIndex retrieval:
    Sends the query + document tree to an LLM.
    LLM reasons over the structure and returns relevant node_ids.
    
    Returns: dict with 'thinking' (reasoning) and 'node_list' (node IDs)
    """
    
    # Compress tree to save tokens — only send titles + short summaries
    def compress(nodes):
        out = []
        for n in nodes:
            entry = {
                "node_id": n["node_id"],
                "title":   n["title"],
                "page":    n.get("page_index", "?"),
                "summary": n.get("text", "")[:150]  # first 150 chars
            }
            if n.get("nodes"):
                entry["children"] = compress(n["nodes"])
            out.append(entry)
        return out
    
    compressed_tree = compress(tree)
    
    prompt = f"""You are given a query and a document's tree structure (like a Table of Contents).
Your task: identify which node IDs most likely contain the answer to the query.
Think step-by-step about which sections are relevant.

Query: {query}

Document Tree:
{json.dumps(compressed_tree, indent=2)}

Reply ONLY in this exact JSON format:
{{
  "thinking": "<your step-by-step reasoning>",
  "node_list": ["node_id1", "node_id2"]
}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)




# ── Helper: Find nodes by ID ─────────────────────────────────────────────────
def find_nodes_by_ids(tree: list, target_ids: list) -> list:
    """Recursively walk the tree and collect nodes matching target_ids."""
    found = []
    for node in tree:
        if node["node_id"] in target_ids:
            found.append(node)
        if node.get("nodes"):
            found.extend(find_nodes_by_ids(node["nodes"], target_ids))
    return found



# ── Generate answer from retrieved nodes ─────────────────────────────────────

def generate_answer(query: str, nodes: list, model: str = "openai/gpt-oss-20b") -> str:
    """
    Takes retrieved nodes as context and generates a grounded answer.
    Instructs the LLM to cite section titles and page numbers.
    """
    if not nodes:
        return "⚠️ No relevant sections found in the document."
    
    # Build context string from retrieved nodes
    context_parts = []
    for node in nodes:
        context_parts.append(
            f"[Section: '{node['title']}' | Page {node.get('page_index', '?')}]\n"
            f"{node.get('text', 'Content not available.')}"
        )
    context = "\n\n---\n\n".join(context_parts)
    
    prompt = f"""You are an expert document analyst.
Answer the question using ONLY the provided context.
For every claim you make, cite the section title and page number in parentheses.
Be concise and precise.

Question: {query}

Context:
{context}

Answer:"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content



# ── The complete Vectorless RAG function ─────────────────────────────────────
def vectorless_rag(query: str, tree: list, verbose: bool = True) -> str:
    """
    Full end-to-end PageIndex RAG pipeline:
    
    Step 1: LLM Tree Search  → finds relevant node_ids
    Step 2: Node Retrieval   → fetches section content
    Step 3: Answer Generation → produces cited answer
    """
    if verbose:
        print(f"{'='*55}")
        print(f"🔍 Query: {query}")
        print(f"{'='*55}")
    
    # Step 1: Tree Search
    search_result  = llm_tree_search(query, tree)
    node_ids       = search_result.get("node_list", [])
    
    if verbose:
        print(f"\n🧠 Reasoning: {search_result.get('thinking', '')[:200]}...")
        print(f"🎯 Retrieved node IDs: {node_ids}")
    
    # Step 2: Retrieve nodes
    nodes = find_nodes_by_ids(tree, node_ids)
    
    if verbose:
        print(f"📄 Sections found: {[n['title'] for n in nodes]}")
    
    # Step 3: Generate answer
    answer = generate_answer(query, nodes)
    
    if verbose:
        print(f"\n📝 Answer:\n{answer}")
    
    return answer


# ── Run the full pipeline ────────────────────────────────────────────────────
answer = vectorless_rag(
    query="Which part of ML is difficult to understand?",
    tree=pageindex_tree
)