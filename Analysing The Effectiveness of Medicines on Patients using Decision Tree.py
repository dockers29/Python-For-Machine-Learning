#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import sklearn.tree as tree


# In[2]:


import subprocess

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

runcmd('echo "Hello, World!"', verbose = True)


# ## Downloading the data

# In[3]:


runcmd("wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/drug200.csv", verbose = True)


# Exploring the data

# In[4]:


df=pd.read_csv('drug200.csv')


# In[5]:


df.head()


# The data consists of several information regarding the age, sex, blood pressure(BP), cholesterol, drugs, and how the patients respond to the drugs.

# In[6]:


df.shape


# The data consists of 200 patients with 6 informations.

# In[7]:


X = df[['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']].values
X[0:5]


# Sklearn decision trees does not read categorical data such as Sex, BP, and Cholesterol. Thus we must change the data into numerical values by using pd.get_dummies() or preprocessing.LabelEncoder to convert the category into dummy numerics.

# In[8]:


from sklearn import preprocessing
le_sex=preprocessing.LabelEncoder()
le_sex.fit(['F','M'])
X[:,1] = le_sex.transform(X[:,1])


# In[9]:


X[0:5]


# In[10]:


df["Cholesterol"].value_counts()


# So F=0 and M=1, continue for BP and Cholesterol.

# In[11]:


le_BP = preprocessing.LabelEncoder()
le_BP.fit([ 'LOW', 'NORMAL', 'HIGH'])
X[:,2] = le_BP.transform(X[:,2])


# In[12]:


le_Chol = preprocessing.LabelEncoder()
le_Chol.fit([ 'NORMAL', 'HIGH'])
X[:,3] = le_Chol.transform(X[:,3]) 

X[0:5]


# Target Variable

# In[13]:


y=df["Drug"]
y[0:5]
y


# ## Setting the decision tree

# In[14]:


from sklearn.model_selection import train_test_split


# In[15]:


get_ipython().run_line_magic('pinfo2', 'train_test_split')


# In[16]:


X_trainset, X_testset, y_trainset, y_testset=train_test_split(X, y, test_size=0.3, random_state=3)


# In[17]:


X_trainset, X_testset, y_trainset, y_testset


# In[18]:


print('Shape of X test {}'.format(X_testset.shape),'&','Shape of y test {}'.format(y_testset.shape))


# ## Modelling

# In[19]:


drugtree=DecisionTreeClassifier(criterion='entropy', max_depth=4)
drugtree


# In[20]:


clf=drugtree.fit(X_trainset, y_trainset)


# ## Prediction

# Let's make prediction using the model above on the test data set and store it into a variable predTree.

# In[21]:


predTree=drugtree.predict(X_testset)


# In[22]:


print(predTree)
print(y_testset)


# The first 5 are okay as we could see, but let's evaluate the overall performance of the model.

# ## Evaluate The Model

# For model evaluation, we will use metrics from sklearn to check the accuracy of the model.

# In[23]:


from sklearn import metrics
import matplotlib.pyplot as plt


# In[24]:


print("DecisionTree's Accuracy:", metrics.accuracy_score(y_testset, predTree))


# The closer the value to 1, the closer it matches with the testset, implying better accuracy.

# # Visualizing The Tree

# First, let's install the packages and import them

# In[25]:


#!conda install -c conda-forge pydotplus -y
#!conda install -c conda-forge python-graphviz -y


# In[26]:


get_ipython().run_line_magic('pinfo', 'tree.plot_tree')


# In[27]:


tree.plot_tree(drugtree)
plt.show()


# In[28]:


with open("drug200.csv", 'w') as f:  
    f = tree.export_graphviz(clf, out_file=f)  


# In[29]:


import os
os.unlink('drug200.csv')


# In[30]:


import pydotplus
dot_data=tree.export_graphviz(clf, out_file=None)
graph2=pydotplus.graph_from_dot_data(dot_data)
graph2.write("drug200.csv.pdf")


# In[31]:


feature_names=['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']


# In[32]:


target_names=['drugA','drugB', 'drugC', 'drugX', 'drugY']


# In[33]:


from IPython.display import Image
dot_data=tree.export_graphviz(clf, out_file=None,  
                     feature_names=feature_names, class_names=target_names, filled=True, rounded=True,  # leaves_parallel=True, 
                     special_characters=True)
graph2 = pydotplus.graph_from_dot_data(dot_data)
nodes = graph2.get_node_list()
Image(graph2.create_png() ) 


# Notes:
# 1) Everytime a split happens, we try to increase the purity of the prediction by using a certain criteria in each nodes.
# 
# 2) With the accuracy of 0.98 is quite accurate. Below I also make sure that the classification is correct by filtering out data via conditions.
# 
# 3) Drug A is for those who have Na_to_K lower than or equals to 14.6, High BP, and younger or at age 50, while Drug Y is for those who have Na_to_K higher than 14.6.
# 
# Numeric value interpretation:
# 
# BP: High=0, Low=1, Normal=2
# 
# Cholesterol: High=1, Normal=0

# ## Making sure that our labelling of drug classification is correct

# In[34]:


newdf = df[(df.Drug == "drugA")] #reading the graph,check whether BP of patients for drug A and B is equals to 0, which is High.
drugXBP=newdf['BP'].value_counts()
newdf2 = df[(df.Drug == "drugB")]
drugBBP=newdf2['BP'].value_counts()
print("BP of Drug X:",drugXBP,"& BP of Drug B", drugBBP)


# In[36]:


newdf = df[(df.Drug == "drugA")] #reading the graph,check whether Age of patients for drug A is less or equals to 50, and B otherwise.
drugXAge=newdf['Age'].value_counts()
newdf2 = df[(df.Drug == "drugB")]
drugBAge=newdf2['Age'].value_counts()
print("Age of Drug X:",
      drugXAge,
      "& Age of Drug B", drugBAge)


# It is as classified by the model.

# In[ ]:




