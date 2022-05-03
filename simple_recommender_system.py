#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from ast import literal_eval

import warnings

warnings.simplefilter("ignore")


# In[2]:


md = pd.read_csv("./dataset/movies_metadata.csv")
md.head()


# In[3]:


md["genres"] = (
    md["genres"]
    .fillna("[]")
    .apply(literal_eval)
    .apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
)


# In[4]:


md.head()


# In[5]:


md.info()


# In[6]:


md["release_date"] = pd.to_datetime(
    md["release_date"], format="%Y-%m-%d", errors="coerce"
)


# In[7]:


md["release_date"] = md["release_date"].dt.strftime("%Y")


# In[8]:


md = md.rename(columns={"release_date": "year"})


# In[9]:


md.head()


# In[10]:

gen_md = md.explode("genres")
genres_list = gen_md["genres"].unique()


# In[11]:


def genres() -> np.ndarray:
    return genres_list


# In[12]:


def build_chart(genre, n, percentile=0.85):
    df = gen_md[gen_md["genres"] == genre]
    vote_counts = df[df["vote_count"].notnull()]["vote_count"].astype("int")
    vote_averages = df[df["vote_average"].notnull()]["vote_average"].astype("int")
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)

    qualified = df[
        (df["vote_count"] >= m)
        & (df["vote_count"].notnull())
        & (df["vote_average"].notnull())
    ][["title", "year", "vote_count", "vote_average"]]
    qualified["vote_count"] = qualified["vote_count"].astype("int")
    qualified["vote_average"] = qualified["vote_average"].astype("int")

    qualified["wr"] = qualified.apply(
        lambda x: (x["vote_count"] / (x["vote_count"] + m) * x["vote_average"])
        + (m / (m + x["vote_count"]) * C),
        axis=1,
    )
    qualified = qualified.sort_values("wr", ascending=False).head(25)

    return qualified.head(n)


# In[13]:

"""
build_chart("Romance", 10)


# In[14]:


gen_md.dropna(inplace=True)


# In[15]:


genres_list
"""
