import os
from datetime import datetime
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class Repo(object):
    """Class store repo information"""
    def __init__(self, data):
        self.name = data['nameWithOwner']
        self.last_updated = datetime.fromisoformat(data["pushedAt"][:-1])
        template = data['templateRepository']
        if template:
            self.template =  template['nameWithOwner']
        else:
            self.template = None


def create_client():
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}", 
    }
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=headers)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client


def generate_query(cursor=None):
    """Construct graph api query"""
    if cursor:
        after = f' after: "{cursor}"'
    else:
        after = ""

    return gql(
        f'''
        {{
            viewer {{
                repositories(first: 100{after}) {{
                    edges {{
                        cursor
                        node {{
                            nameWithOwner
                            pushedAt
                            templateRepository {{
                                nameWithOwner
                            }}
                        }}
                    }}
                }}
            }}
        }}
        '''
    )

def repo_filter(repo):
    if repo.template != "bo-sfl/personal-template":#"SFLScientific/SFL-Template":
        return False
    # if repo.last_updated < datetime.today() - datetime.timedelta(days=280):
    #     return False
    return True


def main():
    client = create_client()
    current_cursor = None
    results = []
    while True:
        # Provide a GraphQL query
        query = generate_query(current_cursor)
        result = client.execute(query)['viewer']['repositories']['edges']
        # Execute the query on the transport
        results.extend([Repo(x['node']) for x in result])
        if len(result) < 100:
            break
        else:
            current_cursor = result[-1]['cursor']

    return [x.name for x in filter(repo_filter, results)]


if __name__ == "__main__":
    main()