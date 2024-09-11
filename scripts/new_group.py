# Create a database connection
import argparse, os, sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.persistence.models.group import Group
from src.persistence.database import DatabaseAccess

# Load credentials from .env file
load_dotenv()

database = DatabaseAccess(os.getenv("DATABASE_URL"))

if __name__ == '__main__':

    # Parse arguments 
    parser = argparse.ArgumentParser(description="Create a new group")
    parser.add_argument('--id', type=int, help='Id of the Discord Channel', default=None)
    parser.add_argument('--name', type=str, help='Name of the Group', default=None)
    args = parser.parse_args()

    channel_id = args.id
    name = args.name

    if channel_id is None or name is None:
        print("Please provide the group id and name")
    else: 

        group = Group(channel_id=channel_id, name=name)

        database.group_resource.create(group)