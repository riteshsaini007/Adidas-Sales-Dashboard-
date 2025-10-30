import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

import datetime

# Page setup(Tam-jham)
st.write("Streamlit DashBoard")
st.set_page_config(layout="wide", page_title="Adidas Sales Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Load Data(Data Mere Pss aja)
df = pd.read_excel("Adidas.xlsx")

# ===== HEADER =====
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
with col1:
    try:
        image = Image.open("erth.jpg")
        st.image(image, width=220)
    except FileNotFoundError:
        st.error("Image 'erth.jpg' not found.")
with col2:
    st.markdown(
        "<h1 style='text-align:center; color:white;'>Adidas Sales Dashboard 🏷️</h1>",
        unsafe_allow_html=True
    )
with col3:
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.markdown(
        f"<p style='text-align:right; font-size:16px; color:white;'>Last updated:<br><b>{box_date}</b></p>",
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

# [   ===== MAIN SECTION =====   Jai Shree Ram]
#3 columns bani hai for symmetrical layout
col1, col2, col3 = st.columns([0.45, 0.2, 0.45])

bright_colors = ["#00FFFF", "#FF007F", "#FFD700", "#00FF7F", "#1E90FF", "#FF4500"]

# Bar Chart (Left Side)
with col1:
    fig1 = px.bar(
        df,
        x="Retailer",
        y="TotalSales",
        color="Retailer",
        color_discrete_sequence=bright_colors,
        labels={"TotalSales": "Total Sales ($)"},
        title="Total Sales by Retailer",
        template="none",
        height=500
    )
    fig1.update_traces(marker_line_color='white', marker_line_width=1.5, opacity=0.95)
    fig1.update_layout(
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        xaxis=dict(showgrid=True, color="white"),
        yaxis=dict(showgrid=True, color="white"),
        font=dict(color="white", size=13),
        title=dict(x=0.4, font=dict(size=20, color="white", family="Arial Black")),
        legend=dict(orientation="v", y=0.9, x=1.02, font=dict(color="white", size=11))
    )
    st.plotly_chart(fig1, use_container_width=True)

# Summary (Center)
with col2:
    st.markdown("<h3 style='color:#FFD700;'>Quick Summary 📈</h3>", unsafe_allow_html=True)
    total_sales = df["TotalSales"].sum()
    avg_sales = df["TotalSales"].mean()
    best_retailer = df.loc[df["TotalSales"].idxmax(), "Retailer"]

    st.markdown(f"<h5 style='color:white;'>Total Sales</h5>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#00FF7F;'>${total_sales:,.0f}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='color:white;'>Average Sales</h5>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#00FF7F;'>${avg_sales:,.0f}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='color:white;'>Top Retailer</h5>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color:#00BFFF;'>{best_retailer}</h4>", unsafe_allow_html=True)


#Second vala Chart (Right Side mai , Line Chart)
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b '%y") 

# Group by month and sum of sales
result = df.groupby(by="Month_Year")["TotalSales"].sum().reset_index()

with col3:
    fig2 = px.line(
        result,
        x="Month_Year",
        y="TotalSales",
        title="Total Sales Over Time",
        template="plotly_dark",  
        markers=True  
    )
    st.plotly_chart(fig2, use_container_width=True) 



#Download And other things are here!
_, view1 , dwn1, view2, dwn2  = st.columns([0.01,0.20,0.45,0.20,0.20]) 

with view1:
    expander = st.expander("Redailer Wise Sales")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)

with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
    file_name = "RetailerSales.csv",mime= "text/csv")

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)

with dwn2:
    st.download_button("Get Data", data = result.to_csv().encode("utf-8"),
    file_name = "MonthlySales.csv",mime= "text/csv")




st.divider()



# Another one

result1 = df.groupby(by = "State")[["TotalSales","UnitsSold"]].sum().reset_index()
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = result1["State"],y = result1["TotalSales"], name = "Total Sales"))
fig3.add_trace(go.Scatter(x = result1["State"],y = result1["UnitsSold"],mode = "lines",
name = "Units Sold", yaxis = "y2"))
fig3.update_layout(
    title= "Total Sales and Units Sold by State",
    xaxis = dict(title = "State"),
    yaxis = dict(title = "Total Sale", showgrid = True),
    yaxis2 = dict(title = "Units Sold",overlaying= "y", side = "right"),
    template = "gridon",
    legend = dict(x = 1,y = 1)

)

_,col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width= True)


# Download & View things are here for third graph
_, view3, dwn3 = st.columns([0.3, 0.35, 0.35])

with view3:
    expander = st.expander("View State-wise Sales Data")
    expander.write(result1)

with dwn3:
    st.download_button(
        "Get State Data",
        data=result1.to_csv(index=False).encode("utf-8"),
        file_name="StateSales.csv",
        mime="text/csv"
    )

st.divider()


# Another One TreeMap
_, col7 = st.columns([0.1,1])


treemap = df[["Region","City","TotalSales"]].groupby(by = ["Region","City"])["TotalSales"].sum().reset_index()
def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)
fig4 = px.treemap(treemap, path = ["Region","City"], values = "TotalSales",
                hover_name = "TotalSales (Formatted)",
                hover_data = ["TotalSales (Formatted)"],
                color = "City", height = 700, width = 600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4,use_container_width=True)

# View & Download section for Treemap graph
_, view4, dwn4 = st.columns([0.3, 0.45, 0.45])

with view4:
    expander = st.expander("View Region-City Sales Data")
    expander.write(treemap)

with dwn4:
    st.download_button(
        "Get Region-City Data",
        data=treemap.to_csv(index=False).encode("utf-8"),
        file_name="RegionCitySales.csv",
        mime="text/csv"
    )
