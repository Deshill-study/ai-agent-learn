from ddgs import DDGS

def internet_search(query: str):
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(
            query,
            max_results=5, 
            region="wt-wt", 
            safesearch="moderate", 
            timelimit="y"
        )
        if ddgs_gen:
            return [r for r in ddgs_gen]
    return "No results found."