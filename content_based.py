#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import warnings

warnings.simplefilter("ignore")


# In[2]:


md2 = pd.read_csv("./dataset/movies_metadata.csv")


# In[3]:


links_small = pd.read_csv("./dataset/links.csv")


# In[4]:


links_small.head(5)


# In[5]:


links_small.info()


# In[6]:


links_small = links_small[links_small["tmdbId"].notnull()]["tmdbId"].astype("int")


# In[7]:


md2["genres"] = (
    md2["genres"]
    .fillna("[]")
    .apply(literal_eval)
    .apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
)


# In[8]:


md2["release_date"] = pd.to_datetime(
    md2["release_date"], format="%Y-%m-%d", errors="coerce"
)


# In[9]:


md2["release_date"] = md2["release_date"].dt.strftime("%Y")


# In[10]:


md2 = md2.rename(columns={"release_date": "year"})


# In[11]:


md2 = md2.drop([19730, 29503, 35587])


# In[12]:


md2["id"] = md2["id"].astype("int")


# In[13]:


smd = md2[md2["id"].isin(links_small)]
smd.shape


# In[14]:


smd["tagline"] = smd["tagline"].fillna("")
smd["description"] = smd["overview"] + smd["tagline"]
smd["description"] = smd["description"].fillna("")


# In[15]:


tf = TfidfVectorizer(
    analyzer="word", ngram_range=(1, 2), min_df=0, stop_words="english"
)
tfidf_matrix = tf.fit_transform(smd["description"])


# In[16]:


tfidf_matrix.shape


# In[17]:


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


# In[18]:


cosine_sim[0]


# In[19]:


smd = smd.reset_index()
titles = smd["title"]
titles_list = titles.unique()
indices = pd.Series(smd.index, index=smd["title"])


# In[20]:


def movie_titles() -> np.array:
    return titles_list


# In[21]:


def get_recommendations(title, n, percentile=0.5):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]

    df = smd.iloc[movie_indices]
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
    qualified = qualified.sort_values("vote_average", ascending=False).head(25)

    qualified.rename(
        columns={
            "title": "Title",
            "year": "Year",
            "vote_count": "Vote Count",
            "vote_average": "Vote Average",
            "wr": "Weight Rate",
        },
        inplace=True,
    )

    return qualified.head(n)


# In[22]:

"""
get_recommendations("The Godfather", 10)
"""
