# Create a database connection
import argparse, os
from src.persistence.database import DatabaseAccess


database = DatabaseAccess(os.getenv("DB_URI"))

if __name__ == '__main__':

    # Parse arguments 
    parser = argparse.ArgumentParser(description="Create a new group")
    parser.add_argument('--id', type=int, help='Id of the Group', default=None)
    parser.add_argument('--name', type=str, help='Name of the Group', default=None)
    args = parser.parse_args()

    group_id = args.id
    name = args.name

    if group_id is None or name is None:
        print("Please provide the group id and name")
    else: 
        database.group_resource.create_group(group_id, name)