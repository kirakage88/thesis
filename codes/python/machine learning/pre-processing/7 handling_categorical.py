import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder



df = pd.DataFrame([
    ['green', 'M', 10.1,'class2'],
    ['red', 'L', 13.5, 'class1'],
    ['blue', 'XL', 15.3, 'class2']])

df.columns = ['color', 'size', 'price', 'classlabel']


size_mapping = {
    'XL': 3,
    'L': 2,
    'M': 1
}

df['size'] = df['size'].map(size_mapping)
print(df)

class_le = LabelEncoder()
y = class_le.fit_transform(df['classlabel'].values)
#print(y)

#print(df['color'].unique())

ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop='first', categories='auto').set_output(transform='pandas')

ohetransform = ohe.fit_transform(df[['color']])
#print(ohetransform)

df = pd.concat([df, ohetransform],axis=1).drop(columns=['color'])
print(df)