import pandas as pd
import variables
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.tree import export_graphviz

from six import StringIO
from IPython.display import Image

import pydotplus

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.impute import SimpleImputer

filename = "../data/raw/fy21_hs_survey_analysis.pkl"

df = pd.read_pickle(filename)

df_ml = df.drop(variables.to_drop, axis=1)
# Impute missing values using a median strategy
imp = SimpleImputer(missing_values=np.nan, strategy="median")
imp.fit(df_ml)
idf = df_ml.copy()
idf[:] = imp.transform(df_ml)

# Define label (y) and feature (X) dataframes
y = idf[["nps_positive"]]
X = idf.drop(["nps_positive", "nps_detractor"], axis=1)

y = idf[["nps_detractor"]]
X = idf.drop(["nps_positive", "nps_detractor"], axis=1)

# Split into test and train datasets
# A test size of 20% is commonly used for predictive modeling but can be reduced for studying feature importance
# Setting random state allows for repeatability of training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)

# Train model
# Tree depth can be adjusted depending upon the number of significant features
dtclf = DecisionTreeClassifier(criterion="gini", max_depth=3)
dtclf = dtclf.fit(X_train, y_train)

# Run test data through trained model
y_pred = dtclf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))


dot_data = StringIO()
export_graphviz(
    dtclf,
    out_file=dot_data,
    filled=True,
    rounded=True,
    special_characters=True,
    feature_names=X.columns,
    class_names=["Negative NPS Score", "Positive NPS Score"],
)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png("output_detractor.png")
Image(graph.create_png())


# Logistic Regression model
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Scale data to compare feature importance
# Normally feature scaling isn't required for Logistic Regression but it's important
# An alternative approach would be to use L2 regularization
scaler = StandardScaler()
scaler.fit(X)
X_scaled = pd.DataFrame(scaler.transform(X), columns=X.columns)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.1, random_state=1
)

lrclf = LogisticRegression(max_iter=1000)
lrclf.fit(X_train, y_train.values.ravel())

y_pred = dtclf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

k = 10

abs_weights = np.abs(lrclf.coef_.ravel())
sorted_index = np.argsort(abs_weights)[::-1]

# Get the index of the top-k features
top_k_index = sorted_index[:k]

# get the names of the top k most important features
top_k = list(zip(X.columns[top_k_index], lrclf.coef_.ravel()[top_k_index]))
for top in top_k:
    print(top)
