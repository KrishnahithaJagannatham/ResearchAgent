from config import get_llm
from tools import tavily_search

llm = get_llm()

def analysis_planning(state):
    question = state["question"]

    prompt = f"""
    You are a Strategic Technology Research Analyst.

    Given the research question below:

    {question}

    Perform the following in ONE response:

    1. Classify the domain into one of:
       - Technology Evaluation
       - AI System Analysis
       - Market Strategy
       - Policy Analysis
       - Scientific Research
       - General Analysis

    2. Define 5–7 strategic analysis dimensions.

    3. Generate 4 focused research queries that:
       - Cover core evaluation
       - Cover risks/limitations
       - Cover competitive comparison
       - Cover future outlook

    Return the output in this structured format:

    DOMAIN:
    <domain>

    STRATEGY:
    - bullet
    - bullet

    QUERIES:
    1.
    2.
    3.
    4.
    """

    response = llm.invoke(prompt)
    content = response.content

    # Simple parsing
    domain = ""
    strategy = ""
    queries = []

    if "DOMAIN:" in content:
        domain = content.split("DOMAIN:")[1].split("STRATEGY:")[0].strip()

    if "STRATEGY:" in content:
        strategy = content.split("STRATEGY:")[1].split("QUERIES:")[0].strip()

    if "QUERIES:" in content:
        query_block = content.split("QUERIES:")[1].strip()
        queries = [line.strip() for line in query_block.split("\n") if line.strip()]

    state["domain"] = domain
    state["strategy"] = strategy
    state["queries"] = queries
    state["thinking_log"].append("Analysis plan generated (domain + strategy + queries).")

    return state
def evidence_gathering(state):
    queries = state["queries"]
    collected_results = []

    for q in queries:
        # Skip empty or invalid queries
        if not q or len(q.strip()) < 10:
            continue

        clean_query = q.strip()

        try:
            results = tavily_search(clean_query)

            # Ensure results exist and have structure
            if results and isinstance(results, dict):
                collected_results.append({
                    "query": clean_query,
                    "results": results
                })

        except Exception as e:
            # Log tool failure but DO NOT crash the agent
            state["thinking_log"].append(
                f"Tavily search failed for query: '{clean_query[:50]}'"
            )
            continue

    state["raw_evidence"] = collected_results
    state["thinking_log"].append(
        f"Evidence gathered for {len(collected_results)} queries."
    )

    return state

def evidence_scoring(state):
    raw_evidence = state["raw_evidence"]
    scored = []

    for item in raw_evidence:
        query = item["query"]
        tavily_results = item["results"].get("results", [])

        for result in tavily_results:
            url = result.get("url", "")
            content = result.get("content", "")
            tavily_score = result.get("score", 0)

            heuristic_score = 0.0

            # Domain credibility
            if ".gov" in url or ".edu" in url:
                heuristic_score += 0.3

            # Recency heuristic
            if any(year in content for year in ["2023", "2024", "2025"]):
                heuristic_score += 0.2

            # Data keywords
            if any(word in content.lower() for word in ["data", "benchmark", "report", "study"]):
                heuristic_score += 0.2

            # Length heuristic
            if len(content) > 300:
                heuristic_score += 0.2

            heuristic_score = min(heuristic_score, 1.0)

            # Combine Tavily relevance + heuristic credibility
            final_score = (0.6 * tavily_score) + (0.4 * heuristic_score)

            scored.append({
                "query": query,
                "url": url,
                "final_score": round(final_score, 3),
                "tavily_score": tavily_score,
                "heuristic_score": heuristic_score
            })

    state["scored_evidence"] = scored
    state["thinking_log"].append("Evidence scored using Tavily relevance + credibility heuristics.")

    return state

def evaluation_node(state):
    scored = state["scored_evidence"]

    if not scored:
        state["confidence"] = 0.0
    else:
        avg_score = sum(item["final_score"] for item in scored) / len(scored)
        state["confidence"] = round(avg_score, 3)

    # Track evolution
    if "confidence_history" not in state:
        state["confidence_history"] = []

    state["confidence_history"].append(state["confidence"])

    state["thinking_log"].append(
        f"Confidence evaluated: {state['confidence']}"
    )

    return state

def refinement_node(state):
    question = state["question"]
    strategy = state["strategy"]

    prompt = f"""
    The research question is:
    {question}

    The strategic dimensions are:
    {strategy}

    Previous evidence was insufficient.

    Generate 2 concise, clean search queries.
    Return ONLY the queries.
    No numbering.
    No bullet points.
    No explanations.
    """

    response = llm.invoke(prompt)
    lines = response.content.split("\n")

    new_queries = []
    for line in lines:
        clean = line.strip().lstrip("-").lstrip("0123456789. ").strip()
        if len(clean) > 10:  # filter junk
            new_queries.append(clean)

    state["queries"] = new_queries[:2]  # limit to 2
    state["iteration"] += 1
    state["thinking_log"].append("Refinement triggered. Cleaned new queries generated.")

    return state

def conflict_detection_node(state):
    scored = state["scored_evidence"]

    top_sources = sorted(
        scored,
        key=lambda x: x["final_score"],
        reverse=True
    )[:5]

    source_list = "\n".join([item["url"] for item in top_sources])

    llm = get_llm()

    prompt = f"""
    Based on the following sources:

    {source_list}

    Identify any conflicting viewpoints or disagreements.
    Return 3-5 bullet points summarizing conflicts.
    """

    response = llm.invoke(prompt)

    state["conflicts"] = response.content
    state["thinking_log"].append("Conflict analysis completed.")

    return state

    
def synthesis_node(state):
    question = state["question"]
    strategy = state["strategy"]
    scored = state["scored_evidence"]

    if not scored:
        state["report"] = "Insufficient evidence to generate report."
        return state

    top_sources = sorted(
        scored,
        key=lambda x: x["final_score"],
        reverse=True
    )[:6]

    source_text = "\n".join(
        [f"- {item['url']} (score: {item['final_score']})"
         for item in top_sources]
    )

    prompt = f"""
    You are a Strategic Technology Analyst.

    Research Question:
    {question}

    Strategic Dimensions:
    {strategy}

    Evidence Sources:
    {source_text}

    Generate a structured strategic report with:
    1. Executive Summary
    2. Key Strategic Insights
    3. Risk & Limitations
    4. Conflicting Perspectives (if any)
    5. Strategic Recommendation
    6. Cited Sources
    """

    response = llm.invoke(prompt)

    state["report"] = response.content
    state["thinking_log"].append("Strategic synthesis report generated.")

    return state