#!/usr/bin/env python
# coding: utf-8

# # Mid-Course Project
# 
# Hi There, and thanks for your help. If you're reading this you've been selected to help on a secret initiative.
# 
# You will be helping us analyze a portion of data from a company we want to acquire, which could greatly improve the fortunes of Maven Mega Mart.
# 
# We'll be working with `project_transactions.csv` and briefly take a look at `product.csv`.
# 
# First, read in the transactions data and explore it.
# 
# * Take a look at the raw data, the datatypes, and cast `DAY`, `QUANTITY`, `STORE_ID`, and `WEEK_NO` columns to the smallest appropriate datatype. Check the memory reduction by doing so.
# * Is there any missing data?
# * How many unique households and products are there in the data? The fields household_key and Product_ID will help here.

# In[131]:


import pandas as pd
import numpy as np


# In[132]:


transactions = pd.read_csv("project_transactions.csv")


# In[133]:


product= pd.read_csv('product.csv')


# In[134]:


product.head()


# In[135]:


transactions.head()


# In[136]:


transactions.info(memory_usage="deep")


# In[137]:


transactions.describe().round()


# In[138]:


transactions.isna().sum()


# In[139]:


transactions=transactions.astype({"DAY": "Int16",
                                 "QUANTITY": "Int32",
                                 "STORE_ID": "Int32",
                                 "WEEK_NO": "Int8"})


# In[140]:


transactions["household_key"].nunique()


# In[141]:


transactions["PRODUCT_ID"].nunique()


# ## Column Creation
# 
# Create two columns:
# 
# * A column that captures the `total_discount` by row (sum of `RETAIL_DISC`, `COUPON_DISC`)
# * The percentage disount (`total_discount` / `SALES_VALUE`). Make sure this is positive (try `.abs()`).
# * If the percentage discount is greater than 1, set it equal to 1. If it is less than 0, set it to 0. 
# * Drop the individual discount columns (`RETAIL_DISC`, `COUPON_DISC`, `COUPON_MATCH_DISC`).
# 
# Feel free to overwrite the existing transaction DataFrame after making the modifications above.

# In[142]:


transactions["total_discount"]= (transactions["RETAIL_DISC"]+transactions['COUPON_DISC'])


# In[143]:


transactions["percentage disount"]= (transactions["total_discount"]/transactions['SALES_VALUE']).abs()


# In[144]:


transactions["percentage disount"]=(transactions["percentage disount"]
                                    .where(transactions["percentage disount"] > 0,0)
                                    .where(transactions["percentage disount"] < 1,1.0))


# In[145]:


transactions.drop(["RETAIL_DISC", 'COUPON_DISC', 'COUPON_MATCH_DISC'],axis=1)


# In[146]:


transactions.head()


# ## Overall Statistics
# 
# Calculate:
# 
# * The total sales (sum of `SALES_VALUE`), 
# * Total discount (sum of `total_discount`)
# * Overall percentage discount (sum of total_discount / sum of sales value)
# * Total quantity sold (sum of `QUANTITY`).
# * Max quantity sold in a single row. Inspect the row as well. Does this have a high discount percentage?
# * Total sales value per basket (sum of sales value / nunique basket_id).
# * Total sales value per household (sum of sales value / nunique household_key). 

# In[147]:


sum_sales=transactions["SALES_VALUE"].sum().round(2)


# In[148]:


sum_dis=transactions["total_discount"].sum().round(2)


# In[149]:


overall_per_dis=sum_dis / sum_sales
overall_per_dis


# In[150]:


transactions["QUANTITY"].sum().round(2)


# In[151]:


transactions["QUANTITY"].max()


# In[152]:


transactions.loc[transactions["QUANTITY"].argmax()]


# In[153]:


sales_per_basket =sum_sales / transactions["BASKET_ID"].nunique()
sales_per_basket


# In[154]:


sales_per_household=sum_sales / transactions["household_key"].nunique()
sales_per_household


# In[155]:


transactions.info()


# In[156]:


transactions.head()


# In[157]:


transactions['household_key'].sort_values()


# ## Household Analysis
# 
# * Plot the distribution of total sales value purchased at the household level. 
# * What were the top 10 households by quantity purchased?
# * What were the top 10 households by sales value?b
# * Plot the total sales value for our top 10 households by value, ordered from highest to lowest.
# 

# In[158]:


(transactions.groupby("household_key")
            .agg({'SALES_VALUE':'sum'}))


# In[159]:


(transactions.groupby("household_key")
            .agg({'SALES_VALUE':'sum'})
            .plot.hist())


# In[160]:


top_10_sale=(transactions.groupby("household_key")
            .agg({'SALES_VALUE':'sum'})
            .sort_values("SALES_VALUE",ascending= False)
            .iloc[:10])


# In[161]:


top_10_quant=(transactions.groupby("household_key")
            .agg({"QUANTITY":"sum"})
            .sort_values("QUANTITY",ascending= False)
            .iloc[:10])


# In[162]:


(transactions.groupby("household_key")
            .agg({'SALES_VALUE':'sum'})
            .sort_values("SALES_VALUE",ascending= False)
            .iloc[:10]
            .plot.bar())


# ## Product Analysis
# 
# * Which products had the most sales by sales_value? Plot  a horizontal bar chart.
# * Did the top 10 selling items have a higher than average discount rate?
# * What was the most common `PRODUCT_ID` among rows with the households in our top 10 households by sales value?
# * Look up the names of the  top 10 products by sales in the `products.csv` dataset.
# * Look up the product name of the item that had the highest quantity sold in a single row.

# In[163]:


product.head()


# In[164]:


top_prod=(transactions.groupby("PRODUCT_ID")
            .agg({'SALES_VALUE':'sum'})
            .sort_values("SALES_VALUE",ascending= False)
            .iloc[:10])
top_prod


# In[165]:


top_prod["SALES_VALUE"].sort_values().plot.barh()


# In[166]:


((transactions
 .query("PRODUCT_ID in @top_prod.index")
 .loc[: ,"total_discount"]
 .sum()) 
/(transactions.query("PRODUCT_ID in @top_prod.index").loc[: ,"SALES_VALUE"]
  .sum())
)


# In[167]:


top_10_sale


# In[168]:


top_10_quant


# In[169]:


top_prod


# In[170]:


(transactions
    .query("household_key in @top_10_sale.index")
    .loc[:,"PRODUCT_ID"]
    .value_counts()
    .iloc[:10]
    .index)


# In[172]:


product.query("PRODUCT_ID in @top_prod.index")


# In[ ]:




