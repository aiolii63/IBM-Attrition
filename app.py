# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 09:49:38 2022

@author: olivi
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pywaffle import Waffle



import warnings
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", 50)

ibm = pd.read_csv('clean_ibm.csv', sep=';')

st.set_page_config(layout="wide")

cat_colors = sns.color_palette('PuBu')
cont_colors = sns.color_palette('PuBu')

plt.style.use('ggplot')

figsize_std = (10,8)
figs=[plt.figure(figsize=figsize_std) for _ in range(0,8)] # 8 figures

mylabels = ["Stayers", "Leavers"]
mycolors = [ '#539ecd', "tomato"]

numerical = ['Age','DistanceFromHome','NumCompaniesWorked','MonthlyIncome']
categorical = ['WorkLifeBalance','Department','EducationField','MaritalStatus']
measurements = numerical + categorical



st.header('                                        IBM ATTRITION ANALYSIS')

container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        
        st.header('1 | Data Exploration')
        st.write("#### Hands on exploration of employee distribution")
       
               
        # 1_HISTOGRAM
        
        st.write("   ")
        x_axis = st.selectbox("X-Axis", numerical)
        
        ax = figs[0].add_subplot(1,1,1) 
        sns.histplot(data=ibm, x=x_axis, multiple="dodge", shrink=0.5, ax = ax)
        ax.set(xlabel= x_axis, ylabel = "Employee count")
        st.write(figs[0])
        

    with col2:   
        
        st.header('   ')
        st.header('   ')
        st.write('   ')
        st.write("#### Detailed employee distribution")

        #2_FACET GRID
         
 
        ax = figs[1].add_subplot(1,1,1)  
        ibm[numerical].hist(bins=15, figsize=(15, 6), layout=(2, 2))
        fig, ax = plt.subplots(2,2 , figsize=(20, 20))
        plt.style.use('ggplot')
        sns.color_palette("Reds", 10)

        for variable, subplot in zip(categorical, ax.flatten()):
               sns.countplot(ibm[variable], ax=subplot)
                
               
        plt.savefig('facet.png', bbox_inches='tight')
        st.image('facet.png')



container2 = st.container()
col1, col2 = st.columns(2)

with container2:
    
    with col1:
        st.header('2 | More Data exploration')
        st.write("#### Education level distribution")
       
        # 3_WAFFLE CHART
        ax= figs[2].add_subplot(1,1,1)
        waffle_data= ibm['Education'].value_counts()
        plt.figure(FigureClass=Waffle, 
                   rows=35, columns=45, values=waffle_data, 
                   labels=["Bachelor", "Master", "College", "Below College", "PhD"],
                   legend={'loc': 'lower right', 'ncol': 5, 'fontsize': 8, 'framealpha': 0.8}, 
                   starting_location='NW', block_arranging_style= 'snake')
       
        plt.style.use('ggplot')
        plt.savefig('waffle.png', bbox_inches='tight')
        st.image('waffle.png')
 

     
    with col2:
     
        st.header('   ')
        st.header('   ')
        st.write('   ')
        st.write('#### Monthly Income vs Seniority at IBM')   

           
   
        #4_HEXBIN
        ax = sns.jointplot(x=ibm["YearsAtCompany"], y=ibm["MonthlyIncome"], kind='hex', marginal_kws=dict(bins=30, fill=True), xlim= (0,20), ylim= (0,10000), cmap='BuPu' )
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        st.pyplot()
             

container3 = st.container()
col1, col2 = st.columns(2)


with container3:
    with col1:
        
        st.header('3 | Focus on attrition')
        st.write("#### Attrition ratio at IBM")
        
         
        # 5_PIE CHART
        dist = pd.DataFrame(ibm["Attrition"].value_counts())
        labels= dist.index
        
        
        ax = figs[4].add_subplot(1,1,1)
        ax.pie(dist.Attrition, labels = mylabels, colors = mycolors, autopct='%1.1f%%', textprops={'fontsize': 10, 'fontweight' : 10, 'color' : 'Black'})
       
        plt.style.use('ggplot')
     
        st.write(figs[4])
        
    
    with col2:
        st.header('   ')
        st.header('   ')
        st.write('   ')
        st.write("#### Searching for correlations")


        #6_HEATMAP
        ax = figs[5].add_subplot(1,1,1)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        sns.heatmap(ibm.corr().round(2), xticklabels=ibm.corr().columns, yticklabels=ibm.corr().columns, cmap="PuBu", center=0, annot=True, ax = ax)
       
        st.write(figs[5])
       

container4 = st.container()
col1, col2 = st.columns(2)

with container4:
   
    with col1:
        
        st.header('4 | Understanding attrition at IBM')
        st.write("#### Attrition vs Income evolution")
          
        #7_SCATTER
       
        ax = figs[6].add_subplot(1,1,1)
        sns.lmplot(data= ibm, x= "Age", y = "MonthlyIncome", fit_reg = True, hue = 'Attrition', palette=mycolors)
        ax.set(xlabel="Age", ylabel = "Monthly Income", xlim= (15,70), ylim= (2000, 20000))
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        plt.style.use('ggplot')

        plt.savefig('scatter.png', bbox_inches='tight')
        st.image('scatter.png')
        
        
    with col2:
        
        st.header('   ')
        st.header('   ')
        st.write('   ')
        st.write("#### Attrition vs Distance from home")
        
        #8_SCATTER2
       
        ax = figs[7].add_subplot(1,1,1)
        
        sns.lmplot(data= ibm, x= "Age", y= "DistanceFromHome", fit_reg = True, hue = 'Attrition', palette=mycolors)
        ax.set(xlabel="Age", ylabel = "Distance to get to work", xlim= (15,65), ylim= (0, 30))
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        plt.style.use('ggplot')

        plt.savefig('scatter2.png', bbox_inches='tight')
        st.image('scatter2.png')
        



      
