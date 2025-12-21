# AgentCore Hero Demo - LangGraph in the Cloud
# Shows: code -> configure -> deploy -> invoke

Output recordings/09-hero.gif
Output recordings/09-hero.mp4

Source tapes/_settings.tape

Set TypingSpeed 30ms

# Show the LangGraph agent code
Type "head -60 examples/langgraph-web-search/agent.py"
Enter
Sleep 3s

# Navigate and configure
Type "cd examples/langgraph-web-search"
Enter
Sleep 300ms

# Show the 3-step deployment
Type "# Step 1: Configure"
Enter
Sleep 500ms
Type "agentcore configure -e agent.py --region us-east-1 --name web_search_agent"
Enter
Sleep 2s

Type "# Step 2: Deploy"
Enter
Sleep 500ms
Type "agentcore launch"
Enter
Sleep 3s

Type "# Step 3: Invoke"
Enter
Sleep 500ms
Type `agentcore invoke '{"prompt": "Search for AWS re:Invent 2024 announcements"}'`
Enter
Sleep 3s

# Cleanup command
Type "# Cleanup: agentcore destroy"
Enter
Sleep 2s
