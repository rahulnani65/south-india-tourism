from composio_openai import ComposioToolSet, Action, App

# Initialize ToolSet (make sure COMPOSIO_API_KEY is set in env)
toolset = ComposioToolSet()

# Example: Fetch a specific GitHub action tool
github_star_tool = toolset.get_tools(
    actions=[Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER]
)
print(github_star_tool)

# Example: Fetch all 'important' GitHub tools
github_tools = toolset.get_tools(apps=[App.GITHUB])
print(f"Fetched {len(github_tools)} GitHub tools.")