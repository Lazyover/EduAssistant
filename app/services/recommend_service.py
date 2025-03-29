from app.react.tools.googleSearch import google_search
from app.react.tools_register import register_as_tool


class RecommendService:
    @register_as_tool(roles=['student', 'teacher'])
    @staticmethod
    def test():
        print("test")

    @register_as_tool(roles=['student', 'teacher'])
    @staticmethod
    def google_search(query: str):
        """Google search tool
        Args:
            query: query to search

        Returns:
            list: search results
        """
        results = google_search(query)

        return results


