#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from ast import literal_eval

import warnings

warnings.simplefilter("ignore")


# In[2]:


im = pd.read_csv("./dataset/indian movies.csv")
im.head(5)


# In[3]:


im.info()


# In[4]:


im.shape


# In[5]:


im.dropna(inplace=True)


# In[6]:


im.shape


# In[7]:


im = im[im["Genres"] != "-"]


# In[8]:


im.shape


# In[9]:


im.info()


# In[10]:


im["Genres"] = im["Genres"].str.split(", ")


# In[11]:


im


# In[12]:


gen_im = im.explode("Genres")
gen_im["Language"] = gen_im["Language"].apply(str.capitalize)

genres_list_im = gen_im["Genres"].unique()
language_list_im = gen_im["Language"].unique()


# In[13]:


def genres_im() -> np.ndarray:
    return genres_list_im


# In[14]:


def language_im() -> np.ndarray:
    return language_list_im


# In[15]:


gen_im.head()


# In[16]:


def indian_genre_based(genre, lang, n):
    gen_im_new = gen_im[gen_im["Genres"] == genre]
    gen_im_new = gen_im_new[gen_im_new["Language"] == lang]
    gen_im_new = gen_im_new.sort_values(by=["Rating(10)"], ascending=False)
    gen_im_new = gen_im_new.drop(["ID", "Votes"], axis=1)
    return gen_im_new.head(n)


# In[17]:

"""
indian_genre_based("Comedy", "Hindi", 10)


# In[18]:


gen_im["Language"].unique()


# In[19]:


gen_im["Genres"] = gen_im["Genres"].apply(lambda x: x.strip())


# In[20]:


gen_im["Genres"] = gen_im["Genres"].replace({"Musical": "Music"})


# In[21]:


gen_im["Genres"].unique()

"""
