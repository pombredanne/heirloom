"""Main"""
from database.create_database_schema import create_database_schema
from database import database_helper

def main():
    database_helper.update_database('3.19.2')

if __name__ == '__main__':
    main()
