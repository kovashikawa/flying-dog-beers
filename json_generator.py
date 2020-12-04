import pandas as pd
import networkx as nx
from itertools import combinations

import sqlalchemy
import json
from sqlalchemy import create_engine

engine = create_engine('mysql://root:seilatosotestando@localhost:3306/recipes')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

#conecta ao dump

recipes = sqlalchemy.Table('recipes', metadata, autoload=True, autoload_with=engine)
ingredients = sqlalchemy.Table('ingredients_detailed', metadata, autoload=True, autoload_with=engine)

#pega os dados relevantes

# ------------ grafo circular de relações mais comuns de ingredientes -------------------------------------------------

base = sqlalchemy.select([ingredients, recipes]).select_from(
    ingredients.join(recipes, ingredients.columns.fk_ingredient_det_recipe_id ==
                                              recipes.columns.recipe_id, isouter=True))

ResultSet = connection.execute(base).fetchall()

base_db = pd.DataFrame(ResultSet)
base_db.columns = ResultSet[0].keys()

#base usada para o grafo

f = lambda x : pd.DataFrame(list(combinations(x.values,2)),
                            columns=['ingredientA','ingredientB'])
edges = (base_db[['recipe_id', 'ingredient']].groupby(
    'recipe_id')['ingredient'].apply(f)
                               .reset_index(level=1, drop=True)
                               .reset_index())
edges2 = edges.groupby(['ingredientA', 'ingredientB']).size().reset_index().rename(columns={0:'count'})
edges3 = edges2.loc[edges2['count']>200].reset_index()
edges4 = pd.concat([edges3,
                    edges3.loc[edges3['ingredientA']==edges3['ingredientB']]]).drop_duplicates(keep=False)

#selecionamos apenas as conexões que ocorrem mais de duzentas vezes, para garantir que o grafo seja leve e facilmente
#visualizável

G = nx.Graph()
G = nx.from_pandas_edgelist(edges4, 'ingredientA', 'ingredientB', ['count'])

with open('../food.json', 'w') as f:
    f.write(json.dumps(nx.cytoscape_data(G)))

#geração do grafo a partir dos dados
