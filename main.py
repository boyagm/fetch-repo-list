import json 
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


def create_client(token):
    """Create a Graph DB query client"""
    headers = {
        "Authorization": f"token {token}", 
    }
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=headers)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client


def generate_query(cursor, org=None):
    """
    Construct a Github GraphQL API query
    """
    if org:
    
        return gql(f'''
            {{
                viewer {{
                    organization(login: {org}) {{
                        {generate_repo_query(cursor)}
                    }}
                }}
            }}
            '''
        )
    else:
        return gql(f'''
        {{
            viewer {{
                {generate_repo_query(cursor)}
                }}
        }}
        '''
        )


def generate_repo_query(cursor):
    """
    Construct a sub-query to fetch all information
    """
    return f'''
    repositories(first: 100 {next_cursor(cursor)}) {{
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
    '''

def next_cursor(cursor):
    '''Get after string for query'''
    if cursor:
        return f'after: "{cursor}"'
    else:
        return ""


def time_filters(repo, last_n_day):
    """Return True if the repo is active in last N days"""
    if repo.last_updated < datetime.today() - timedelta(days=last_n_day):
        return False
    return True


def template_filters(repo, template_name):
    """Return True if the repo is created using the template"""
    if repo.template != template_name:
        return False
    return True


def parse_results(result_json, org=None):
    if org:
        results = result_json['viewer']['organization']['repositories']['edges']
    else:
        results = result_json['viewer']['repositories']['edges']
    
    repo_list = [Repo(x['node']) for x in results]
    last_cursor = results[-1]['cursor']
    return repo_list, last_cursor

def main():
    parser = argparse.ArgumentParser(description='Process inputs.')
    parser.add_argument('--last_active', type=int, default=None)
    parser.add_argument('--org_name', type=str, default=None)
    parser.add_argument(
        '--template_name', 
        type=str, 
        default=None)
    parser.add_argument(
        '--token', 
        type=str, 
        required=True)

    args = parser.parse_args()

    client = create_client(args.token)
    current_cursor = None
    repo_list = []
    while True:
        # Construct a GraphQL query
        query = generate_query(current_cursor, args.org_name)
        # Execute the query on the transport
        result_json = client.execute(query)
        repos, current_cursor= parse_results(result_json, args.org_name)
        repo_list.extend(repos)
        if len(repos) < 100:
            break

    if args.last_active:
        repo_filter = partial(time_filters, last_n_day=args.last_active)
        repo_list = filter(repo_filter, repo_list)
    
    if args.template_name:
        repo_filter = partial(template_filters, template_name=args.template_name)
        repo_list = filter(repo_filter, repo_list)

    repo_names =  [x.name for x in repo_list]
    for x in repo_list:
        print(x.name, x.template, x.last_updated)

    with open("repos.txt", "w") as f:
        f.write(f'{{\\"repo\\":{repo_names}}}')
        
    return


if __name__ == "__main__":
    main()