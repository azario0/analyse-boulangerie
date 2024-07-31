import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Analyse des Ventes de Boulangerie", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Bakery sales.csv")
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df['unit_price'] = df['unit_price'].str.replace('€', '').str.replace(',', '.').astype(float)
    df['total_price'] = df['Quantity'] * df['unit_price']
    df['date'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.time
    df['hour'] = df['datetime'].dt.hour
    df['week'] = df['datetime'].dt.isocalendar().week
    df['month'] = df['datetime'].dt.month
    return df

df = load_data()

# Main title
st.title("Analyse des Ventes de Boulangerie")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Ventes Quotidiennes", "Produits Populaires", "Tendances Horaires", "Tendances Hebdomadaires", "Analyses Supplémentaires"])

with tab1:
    st.header("Ventes Quotidiennes")
    
    daily_sales = df.groupby('date')['total_price'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_sales['date'], daily_sales['total_price'])
    ax.set_title('Ventes Quotidiennes')
    ax.set_xlabel('Date')
    ax.set_ylabel('Ventes Totales (€)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.write("""
    Ce graphique montre l'évolution des ventes quotidiennes au fil du temps. 
    On peut observer les fluctuations des ventes d'un jour à l'autre, ce qui peut aider à identifier les jours de forte et de faible activité.
    """)

with tab2:
    st.header("Produits les Plus Vendus")
    
    top_products = df.groupby('article')['Quantity'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    top_products.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 des Produits les Plus Vendus')
    ax.set_xlabel('Produit')
    ax.set_ylabel('Quantité Vendue')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    st.write("""
    Ce graphique présente les 10 produits les plus vendus en termes de quantité.
    Il permet d'identifier les produits les plus populaires, ce qui peut être utile pour la gestion des stocks et les décisions de production.
    """)

with tab3:
    st.header("Tendances des Ventes Horaires")
    
    hourly_sales = df.groupby('hour')['total_price'].sum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_sales.plot(kind='bar', ax=ax)
    ax.set_title('Tendance des Ventes Horaires')
    ax.set_xlabel('Heure de la Journée')
    ax.set_ylabel('Ventes Totales (€)')
    st.pyplot(fig)
    
    st.write("""
    Ce graphique montre la répartition des ventes selon l'heure de la journée.
    Il permet d'identifier les heures de pointe et les périodes creuses, ce qui peut aider à optimiser les horaires du personnel et la production.
    """)

with tab4:
    st.header("Tendances des Ventes Hebdomadaires")
    
    weekly_sales = df.groupby('week')['total_price'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(weekly_sales['week'], weekly_sales['total_price'])
    ax.set_title('Tendance des Ventes Hebdomadaires')
    ax.set_xlabel('Semaine de l\'Année')
    ax.set_ylabel('Ventes Totales (€)')
    st.pyplot(fig)
    
    st.write("""
    Ce graphique présente l'évolution des ventes totales par semaine.
    Il permet d'observer les tendances saisonnières et d'identifier les périodes de forte et de faible activité au cours de l'année.
    """)

with tab5:
    st.header("Analyses Supplémentaires")
    
    # Monthly sales trend
    monthly_sales = df.groupby('month')['total_price'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_sales['month'], monthly_sales['total_price'], marker='o')
    ax.set_title('Tendance des Ventes Mensuelles')
    ax.set_xlabel('Mois')
    ax.set_ylabel('Ventes Totales (€)')
    ax.set_xticks(range(1, 13))
    st.pyplot(fig)
    
    st.write("""
    Ce graphique montre l'évolution des ventes mensuelles.
    Il permet d'identifier les mois les plus performants et les variations saisonnières sur l'ensemble de l'année.
    """)
    
    # Extract category from 'article' and compute total sales per category
    df['category'] = df['article'].apply(lambda x: x.split()[0])
    category_sales = df.groupby('category')['total_price'].sum().sort_values(ascending=False)

    # Select top 15 categories
    top_20_categories = category_sales.head(15)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    top_20_categories.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Répartition des Ventes par Catégorie de Produits')
    ax.set_ylabel('')  # Hide y-label
    st.pyplot(fig)

    st.write("""
    Ce graphique en camembert montre la répartition des ventes totales par catégorie de produits.
    Il permet d'identifier les catégories les plus importantes en termes de chiffre d'affaires.
    """)
    
    # Correlation heatmap
    correlation = df[['Quantity', 'unit_price', 'total_price', 'hour', 'week']].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Carte de Corrélation')
    st.pyplot(fig)
    
    st.write("""
    Cette carte de chaleur montre les corrélations entre différentes variables.
    Elle permet d'identifier les relations potentielles entre la quantité vendue, le prix unitaire, le prix total, l'heure de la journée et la semaine de l'année.
    """)

# Add a sidebar with some statistics
st.sidebar.header("Statistiques Générales")
st.sidebar.write(f"Nombre total de transactions: {len(df)}")
st.sidebar.write(f"Chiffre d'affaires total: {df['total_price'].sum():.2f} €")
st.sidebar.write(f"Nombre de produits uniques: {df['article'].nunique()}")
st.sidebar.write(f"Période couverte: du {df['date'].min()} au {df['date'].max()}")