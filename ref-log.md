Implementing a multi-agent workflow helped me understand how multiple specialized agents can collaborate to do a complex task more efficiently than a single model.I learned how dividing responsibilities between agents, where each has a specific defined role and prompt, can make the solution more efficient and easier to debug. Designing an “expert” agent can create a more coherent and easier to understand process. I also realized the importance of prompt design, since the clarity and specificity of each agent’s role directly influenced the quality of their output and the coordination between them.

Initially, I struggled with getting API calls to work consistently inside Codespaces. I fixed this by adding my API keys as a ‘new secret repository’. Another difficulty was ensuring that my reviewer agent uses internet search to verify information. I fixed this by editing the function for ‘reviewer-agent’ to call internet searches. 

For my prompt design, I used a similar format for both my agents, i.e. introduced persona, highlighted responsibilities, listed constraints (if any) and then specified output format. I did this to ensure that my prompts are organized and easy to interpret. I also experimented with rephrasing prompts to encourage collaboration between agents, for example, I explicitly asked the reviewer agent  “to validate and improve the travel itinerary produced by the planner agent” to improved output. 


External Tools and Gen AI assistance: 
Specific GenAI uses:
- I used Gen AI to help me fork my repository. 
Indirect Uses of Gen AI:
- I used Gen AI for tips to write good prompts that I used to write my system prompts. 