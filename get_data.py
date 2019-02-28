from google.oauth2 import service_account
import pandas_gbq
import pandas as pd
import re
from sqlalchemy import create_engine
import logging
import sys


logger = logging.getLogger('pandas_gbq')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

projectid = 'sex-translator-69'
gcp_credentials = service_account.Credentials.from_service_account_file('C:/Users/bingb/Desktop/gcp_key.json')
engine = create_engine('postgresql://postgres:password@localhost:5432/ds4900')

# Number of repos
x = 500

repos_query = (
    "SELECT repo_name, watch_count FROM `bigquery-public-data.github_repos.sample_repos` order by watch_count desc limit " + str(x)
)

commits_query = (
    "select author.name as author_name, author.date as author_date, committer.name as committer_name, committer.date as committer_date, subject, message, d.old_path, d.new_path, repo_name from `bigquery-public-data.github_repos.sample_commits` c, unnest(difference) as d where c.repo_name in ("+re.sub(', watch_count','',repos_query)[:-1]+");"
)

files_query = (
    "select repo_name, path,id from `bigquery-public-data.github_repos.sample_files` where repo_name in ("+re.sub(', watch_count','',repos_query)[:-1]+");"
)


repos = pd.read_gbq(repos_query, project_id = projectid, credentials = gcp_credentials, dialect = 'standard')
commits = pd.read_gbq(commits_query, project_id = projectid, credentials = gcp_credentials, dialect = 'standard')
files = pd.read_gbq(files_query, project_id = projectid, credentials = gcp_credentials, dialect = 'standard')


repos.to_sql('repos', engine, index = False, if_exists = 'replace')
commits.to_sql('commits', engine, index = False, if_exists = 'replace', chunksize = 20000)
files.to_sql('files', engine, index = False, if_exists = 'replace', chunksize = 20000)
