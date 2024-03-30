"""
This script sets up the sqlite database for the movie dataset. 
It creates a database locally.
"""
import sqlite3
import pandas as pd

# Create a connection to the database
conn = sqlite3.connect('../../../dataset/movielens.db')

# Read 6 cvs files from ./ml-25m directory
genome_scores = pd.read_csv('../../../dataset/ml-25m/genome-scores.csv')
genome_tags = pd.read_csv('../../../dataset/ml-25m/genome-tags.csv')
links = pd.read_csv('../../../dataset/ml-25m/links.csv')
movies = pd.read_csv('../../../dataset/ml-25m/movies.csv')
ratings = pd.read_csv('../../../dataset/ml-25m/ratings.csv')
tags = pd.read_csv('../../../dataset/ml-25m/tags.csv')

# Write the dataframes to the database
genome_scores.to_sql('genome_scores', conn)
genome_tags.to_sql('genome_tags', conn)
links.to_sql('links', conn)
movies.to_sql('movies', conn)
ratings.to_sql('ratings', conn)
tags.to_sql('tags', conn)

# Commit the changes and close the connection
conn.commit()
conn.close()
print("movielens.db set up successfully!")

# Check each table's row count
conn = sqlite3.connect('../../../dataset/movielens.db')
tables = ['genome_scores', 'genome_tags', 'links', 'movies', 'ratings', 'tags']
for table in tables:
    print("Table: {}, row count: {}".format(table, pd.read_sql_query("SELECT COUNT(*) FROM {}".format(table), conn)))

