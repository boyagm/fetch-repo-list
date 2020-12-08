import os
import argparse
from datetime import datetime, timedelta
from functools import partial
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
        "Authorization": f"token {os.getenv('ORG_DISTRIBUTE_TOKEN')}", 
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

def repo_filters(repo, template_name, last_n_day):
    if repo.template != template_name:
        return False
    if repo.last_updated < datetime.today() - timedelta(days=last_n_day):
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description='Process inputs.')
    parser.add_argument('--last_active', type=int, default=1)
    parser.add_argument(
        '--template_name', 
        type=str, 
        default="SFLScientific/SFL-Template")
    args = parser.parse_args()

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
    
    repo_filter = partial(
        repo_filters, 
        template_name=args.template_name, 
        last_n_day=args.last_active,
        )
    x =  [x.name for x in filter(repo_filter, results)]
    ww = " ".join(x) 
    print(ww)
    return  ww


if __name__ == "__main__":
    main()