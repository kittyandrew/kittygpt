from kittygpt import Agent

from extras.space import get_astronauts, get_coords_iss
from extras.wiki import wiki_search

if __name__ == "__main__":
    agent = Agent()
    agent.add_command(wiki_search)
    agent.add_command(get_astronauts)
    agent.add_command(get_coords_iss)
    print(agent.run(input("Goal: "), autonomous=True))
