import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector

X = pd.DataFrame({'city': ['London', 'London', 'Paris', 'Sallisaw', ''],
                  'title': ['His Last Bow', 'How Watson Learned the Trick', 'A Moveable Feast', 'The Grapes of Wrath', 'The Jungle'],
                  'expert_rating': [5, 3, 4, 5, np.NaN],
                  'user_rating': [4, 5, 4, np.NaN, 3]})
print(X)

num_cols = X.select_dtypes(include=np.number).columns.tolist()
cat_cols = X.select_dtypes(exclude=np.number).columns.tolist()

# Categorical pipeline
categorical_preprocessing = Pipeline(
[
    ('Imputation', SimpleImputer(missing_values='', strategy='most_frequent')),
    ('Ordinal encoding', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)),
]
)
# Continuous pipeline
continuous_preprocessing = Pipeline(
[
    ('Imputation', SimpleImputer(missing_values=np.nan, strategy='mean')),
    ('Scaling', StandardScaler())
]
)
# Creating preprocessing pipeline
preprocessing = make_column_transformer(
    (continuous_preprocessing, num_cols),
    (categorical_preprocessing, cat_cols),
)

# Final pipeline
pipeline = Pipeline(
    [('Preprocessing', preprocessing)]
)

X_trans = pipeline.fit_transform(X)

print(pd.DataFrame(X_trans, columns= num_cols + cat_cols))