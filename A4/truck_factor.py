#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine


# # Read in data

# In[2]:


engine = create_engine('postgresql://postgres:password@localhost:5432/ds4900')


# In[3]:


repo_query = 'select * from repos'


# In[4]:


repos = pd.read_sql(repo_query, engine)


# In[5]:


files_query = 'select * from files'


# In[6]:


files = pd.read_sql(files_query, engine)


# In[7]:


commits_query = 'select * from commits'


# In[8]:


commits = pd.read_sql(commits_query, engine)


# In[9]:


query = 'select * from github'


# In[10]:


github = pd.read_sql(query, engine)


# # How many files, commits, and repos are there?

# In[11]:


print('There are '+ str(len(files)) +' files.')


# In[12]:


print('There are '+ str(len(commits)) +' commits.')


# In[13]:


print('There are '+ str(len(repos)) +' repos.')


# # How many unique authors and committers are there?

# In[14]:


print('There are '+ str(len(github['author_name'].unique())) +' unique authors.')


# In[15]:


print('There are '+ str(len(github['committer_name'].unique())) +' unique committers.')


# # Truck factor

# In[16]:


authors_per_file = github.groupby('id')['author_name'].count()


# In[17]:


authors_per_path = pd.merge(pd.DataFrame(authors_per_file), files[['id', 'path']], on = 'id')[['path', 'author_name']]


# In[18]:


committers_per_file = github.groupby('id')['committer_name'].count()


# In[19]:


committers_per_path = pd.merge(pd.DataFrame(committers_per_file), files[['id', 'path']], on = 'id')[['path', 'committer_name']]


# # Files with 2 or less authors

# In[20]:


authors_per_path[authors_per_path['author_name'] <= 2]


# # Files with 2 or less committers

# In[21]:


committers_per_path[committers_per_path['committer_name'] <= 2]

