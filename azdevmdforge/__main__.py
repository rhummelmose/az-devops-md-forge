from pprint import pprint
from typing import List

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.released.work_item_tracking.work_item_tracking_client import WorkItemTrackingClient
from azure.devops.v5_1.work_item_tracking.models import WorkItemQueryResult, WorkItemFieldReference, WorkItemLink, WorkItem

from .config import Config

def main():

    # Load configuration from environment variables
    configuration = Config.config_loading_from_env()
    if not configuration.valid():
        raise Exception("Invalid configuration. Required environment variables have to be set.")

    # Build authentication credentials from configuration
    credentials = None
    if configuration.auth_type == Config.AuthType.personal_access_token.value:
        credentials = BasicAuthentication("", configuration.auth_token)

    # Establish connection to Azure DevOps and instantiate work item client
    connection = Connection(base_url=configuration.org_url, creds=credentials)
    client: WorkItemTrackingClient = connection.clients.get_work_item_tracking_client()

    # Run query referenced by id on Azure DevOps
    query_result: WorkItemQueryResult = client.query_by_id(configuration.query_id)

    # We only support results of type workItemLink, these are what's returned by "Tree of work items" queries
    if query_result.query_result_type != "workItemLink":
        raise Exception("Query returned unhandled query result type: " + query_result.query_result_type)

    # If there are no relations, the query returned nothing
    if query_result.work_item_relations is None:
        raise Exception("No work item relations returned by referenced query")

    # No items are actully returned by the query, only a list of relations that describe the tree.
    # Extract the unique work item ids from the list of relations.
    work_item_ids: List[int] = list()
    for relation in query_result.work_item_relations:
        if relation.source is not None and relation.source.id not in work_item_ids:
            work_item_ids.append(relation.source.id)
        if relation.target is not None and relation.target.id not in work_item_ids:
            work_item_ids.append(relation.target.id)

    # Get the actual work items by the extracted ids
    work_items = client.get_work_items(work_item_ids)

    # Build rendering tree
    rendering_tree = list()
    relation: WorkItemLink
    for relation in query_result.work_item_relations:
        # TO-DO: Add strings to rendering tree
        if relation.source is not None:
            print("SOURCE: ", end="")
            pprint(relation.source.__dict__)
        if relation.target is not None:
            print("TARGET: ", end="")
            pprint(relation.target.__dict__)

    # TO-DO: Render rendering tree to string and return by writing to stdout or file

main()
