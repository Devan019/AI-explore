# Two types of memory

# Short Term and Long Term

# | Feature            | Short-Term Memory (Context Window)                | Long-Term Memory (External / Persistent)                |
# | ------------------ | ------------------------------------------------- | ------------------------------------------------------- |
# | **Definition**     | Temporary memory within a single conversation     | Stored memory across multiple sessions                  |
# | **Where it lives** | Inside the model’s context window (tokens)        | External storage (DB, vector DB, files, APIs like Mem0) |
# | **Persistence**    | ❌ Lost after conversation ends                   | ✅ Persists over time                                    |
# | **Capacity**       | Limited (e.g., 8K–200K tokens depending on model) | Scalable (depends on storage system)                    |
# | **Speed**          | Very fast (directly available to model)           | Slightly slower (requires retrieval step)               |
# | **Use Case**       | Chat history, current instructions, reasoning     | User preferences, past interactions, knowledge base     |
# | **Example**        | “Remember what I said 5 messages ago”             | “User likes React and hates DSA”                        |
# | **Implementation** | Automatically handled by LLM                      | Requires tools (vector DB, embeddings, RAG, Mem0, etc.) |
# | **Failure Mode**   | Context overflow → older messages get truncated   | Retrieval failure → wrong or missing memories           |
# | **Control**        | Limited control                                   | Full control                                            |




#type of long term
# | Type                    | Description                                                            | Example                              |
# | ----------------------- | ---------------------------------------------------------------------- | ------------------------------------ |
# | **Episodic Memory**     | Stores past interactions/events (conversation history across sessions) | “User asked about Docker yesterday”  |
# | **Semantic Memory**     | Stores facts and knowledge                                             | “React is a frontend library”        |
# | **Procedural Memory**   | Stores how to perform tasks (skills/workflows)                         | “Steps to deploy MERN app on Vercel” |
# | **User Profile Memory** | Stores user preferences, behavior, interests                           | “User prefers concise answers”       |
# | **Contextual Memory**   | Stores situation-specific info (project, session context)              | “User is building AlgoAnims project” |
