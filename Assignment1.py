import numpy as np
import pandas as pd

#load data on pandas
sd = pd.read_csv("sales_data.csv")

#data exploration (head, info, describe)
print (sd.head())
print (sd.info())
print (sd.describe())

#Missing Values
print (sd.isnull())

#Use NumPy to compute mean, median, std of Sales
sales_array = np.array(sd.Sales)

mean_sales = np.mean(sales_array)
median_sales = np.median(sales_array)
std_of_sales = np.std(sales_array)

print("Mean of Sales",mean_sales)
print("Median of Sales", median_sales)
print("std of Sales",std_of_sales)

#Create Profit_Per_Unit Column
sd["Profit_Per_Unit"] = sd["Profit"]/sd["Quantity"]

#Filter Sales>250
print (sd[sd["Sales"]>250])

#Group by Region (total sales, avg profit)
print (sd.groupby("Region")["Sales"].sum())
print (sd.groupby("Region")["Profit"].mean())

#Create pivot table (Region vs Category)
pivot_table = pd.pivot_table(
    sd,
    values="Sales",        #what we calculate 
    index="Region",        #rows
    columns="Category",    #columns
    aggfunc="sum",         #calculation
    fill_value="0"         #fill for blanks
    )

print(pivot_table)

#Sort by Profit descending

print(sd.sort_values("Profit", ascending=False))

#Classify Sales (High/Medium/Low)

def Classify(x):
    if x>=300:
        return "High"
    elif x>=200:
        return "Medium"
    else:
        return "Low"
sd["Sales_Class"] = sd["Sales"].apply(Classify)
 
print(sd)

#top performing region

top_region = sd.groupby("Region")["Sales"].sum()
print (top_region)


#North is the strongest region by total sales (650) followed by West (600)
#Electronics is the biggest driver of revenue overall
#Furniture only appears in East and contributes the lowest overall sales which means theres opportunity for growth
# #Profit per unit highlights efficiency and we can see Electronics in the West and Furniture in the East has made the best profit per item