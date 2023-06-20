from sklearn.tree import DecisionTreeClassifier, export_text
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import os

database_name = 'database_3.pkl'

try:
    with open('results/' + database_name, 'rb') as inp:
        ml_data = pickle.load(inp)
except NameError:
    print('No files found')

X_ls = []
y_ls = []
for i in range(len(ml_data)):
    X_ls.append(list(ml_data[i]['rel_dist'].values()))
    y_ls.append(ml_data[i]['status'])

X = np.array(X_ls)
y = np.array(y_ls)

# Create a decision tree classifier
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Generate decision tree rules
decision_tree_rules = export_text(model, feature_names=['l_LD', 'l_LC', 'l_LS',
                                                        'l_DC', 'l_DS', 'l_CS'])
print(decision_tree_rules)

#%%
# Plotting correlations
# Train a Random Forest Classifier
model = RandomForestClassifier()
model.fit(X, y)

# Extract feature importances
importances = model.feature_importances_

#%%
# Plot feature importances

feature_names = [r'$l_{LD}$', r'$l_{LC}$', r'$l_{LS}$', r'$l_{DC}$', r'$l_{DS}$', r'$l_{CS}$']
plt.bar(feature_names, importances, edgecolor='k')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.title('Random Forest Feature Importance')
plt.show()

