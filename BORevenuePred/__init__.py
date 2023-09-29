import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import linear_model
from sklearn import metrics

df = pd.read_csv('../boxoffice.csv', encoding='latin-1')
df.drop(['world_revenue', 'opening_revenue'], axis=1, inplace=True)
df.drop('budget', axis=1, inplace=True)

for col in ['MPAA', 'genres']:
    df[col] = df[col].fillna(df[col].mode()[0])
    df.dropna(inplace=True)

df['domestic_revenue'] = df['domestic_revenue'].str[1:]

for col in ['domestic_revenue', 'opening_theaters', 'release_days']:
    df[col] = df[col].str.replace(',', '')

    temp = (~df[col].isnull())
    df[temp][col] = df[temp][col].convert_dtypes(float)

    df[col] = pd.to_numeric(df[col], errors='coerce')

features = ['domestic_revenue', 'opening_theaters', 'release_days']
for col in features:
    df[col] = df[col].apply(lambda x: np.log10(x))

vectorizer = CountVectorizer()
vectorizer.fit(df['genres'])
features = vectorizer.transform(df['genres']).toarray()

genres = vectorizer.get_feature_names_out()
for i, name in enumerate(genres):
    df[name] = features[:, i]

df.drop('genres', axis=1, inplace=True)

for col in df.loc[:, 'action':'western'].columns:
    if (df[col] == 0).mean() > 0.95:
        df.drop(col, axis=1, inplace=True)

le1 = LabelEncoder()
df['distributor'] = le1.fit_transform(df['distributor'])

le2 = LabelEncoder()
df['MPAA'] = le2.fit_transform(df['MPAA'])

y = df['domestic_revenue']
x = df.drop(['domestic_revenue', 'title'], axis=1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

lm = linear_model.LinearRegression()
model = lm.fit(x_train, y_train)

y_pred = model.predict(x_test)

mse = round(metrics.mean_squared_error(y_test, y_pred), 2)
r2 = round(metrics.r2_score(y_test, y_pred), 2)