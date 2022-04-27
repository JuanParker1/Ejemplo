import pandas as pd
import numpy as np

# me busco los csv
peli = pd.read_csv('peliculas.csv')
#print (peli.head())
rating = pd.read_csv('ratings.csv')
#print (rating.head())
usuarios = pd.read_csv('usuarios.csv')
#print (usuarios.head())

# unidmos csv de pelis con rating
pelu_rating = pd.merge(peli, rating, on='peli_id')
#print (pelu_rating.head())

# unidmos csv de pelis+rating con usuarios
clasif = pd.merge(pelu_rating, usuarios, on='user_id')
#print (clasif.head())

#ordenamos por rating
mas_ratings = clasif.groupby('titulo').size().sort_values(ascending=False)[:25]
#print (mas_ratings)

#rating promedio
peli_stats = clasif.groupby('titulo').agg({'rating': [np.size, np.mean]})
#print (peli_stats.head())
print (peli_stats.sort_values([('rating', 'mean')], ascending=False).head())
minimo_100 = peli_stats['rating']['size'] >= 100
print (peli_stats[minimo_100].sort_values([('rating', 'mean')], ascending=False)[:15])