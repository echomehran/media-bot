class SearchService:
    async def search(self, query: str) -> str:
        return f"Searching for: {query}"