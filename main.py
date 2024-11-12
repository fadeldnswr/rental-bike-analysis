# Import Library and Packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Dashboard Title
st.title("Bike Sharing Demand Analysis")
st.markdown("""
Dashboard ini merupakan hasil analisis yang didapat dari dataset Bike Sharing.
Dashboard ini menunjukkan beberapa visualisasi serta korelasi dari variabel yang ada
pada dataset Bike Sharing.
            """)

# Load Dataset
@st.cache_data
def loadData():
    data = pd.read_csv("day.csv")
    data["dteday"] = pd.to_datetime(data["dteday"])
    
    Q1 = data["casual"].quantile(0.25)
    Q3 = data["casual"].quantile(0.75)

    IQR = Q3 - Q1
    upperBound = Q3 + 1.5 * IQR
    lowerBound = Q1 - 1.5 * IQR

    upperCondition = data["casual"] > upperBound
    lowerCondition = data["casual"] < lowerBound
    
    newData = data.copy()
    newData["casual"] = np.where(
    newData["casual"] > upperBound,
    upperBound,
    np.where(
        newData["casual"] < lowerBound,
        lowerBound,
        newData["casual"]
    )
)
    return newData

# Display Dataset
newData = loadData()
st.subheader("Dataset Overview")
st.write(newData.head())

# Exploratory Analysis
st.subheader("Demand Analysis")
st.markdown("""
Pada bagian ini, dilakukan analisis untuk melihat hubungan antara registered dan casual
terhadap total user pada bike sharing dataset.
            """)

# Plotting Registered vs Casual User Demand
fig, ax = plt.subplots()
sns.boxplot(data=newData[["casual", "registered", "cnt"]], ax=ax)
plt.title("User Demand from Registered, Casual, and Total User")
plt.xlabel("Total User")
plt.ylabel("Demand")
st.pyplot(fig)

# Weather and Demand Analysis
st.subheader("Pengaruh Kondisi Cuaca terhadap Rental Sepeda dalam Satu Minggu")
st.markdown("""
Bagian ini menunjukkan bagaimana kondisi cuaca dapat mempengaruhi
total user yang menggunakan sepeda dalam kurun waktu satu minggu.
""")

weatherMap = {
    1: "Clear",
    2: "Mist",
    3: "Light Snow",
    4: "Heavy Rain"
}

weekdayMap = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}

newData["weekday"] = newData["weekday"].map(weekdayMap)
newData["weathersit"] = newData["weathersit"].map(weatherMap)

# Scatter plot of weather vs demand
fig, ax = plt.subplots()
sns.barplot(x=newData["weekday"], y=newData["cnt"], hue=newData["weathersit"], ax=ax)
plt.title("Bike Rental In a Week for Each Weather")
plt.xlabel("Day")
plt.ylabel("Total User of Bike Rental")
st.pyplot(fig)

# Bar plot 
st.subheader("Pengaruh hari libur pada demand peminjaman sepeda di setiap musim")
st.markdown("""
Bagian ini menunjukkan bagaimana hari libur dapat mempengaruhi user
yang menggunakan rental sepeda pada setiap musim.
""")

holidayMap = {
    0: "No Holiday",
    1: "Holiday"
}

seasonMap = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

newData["holiday"] = newData["holiday"].map(holidayMap)
newData["season"] = newData["season"].map(seasonMap)

fig, ax = plt.subplots()
sns.barplot(x=newData["season"], y=newData["cnt"], hue=newData["holiday"], ax=ax)
plt.title("Bike Rental in Holidays for Each Season")
plt.xlabel("Season")
plt.ylabel("Total User of Bike Rental")
st.pyplot(fig)


# Yearly Demand Trend Analysis
st.subheader("Tren Demand Rental Sepeda Tahunana")
st.markdown("""
Bagian ini menunjukkan demand rental sepeda tahunan.
""")

# Extract year from date for yearly trend analysis
fig, ax = plt.subplots()
sns.lineplot(data=newData, x="dteday", y="cnt", ax=ax)
plt.title("Total Bike Rentals per Year")
plt.xlabel("Year")
plt.ylabel("Total Demand")
st.pyplot(fig)

st.markdown("""
---
**Data Source**: Bike Sharing Dataset  
Developed by Fadel Achmad Daniswara  
""")

