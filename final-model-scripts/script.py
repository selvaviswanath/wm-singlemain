from subprocess import run

def predict_workspace():
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.naive_bayes import GaussianNB

    # Load the data
    data = pd.read_csv('./window.csv', header=0)
    data = pd.get_dummies(data, columns=['name'])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data.drop('workspaceNum', axis=1), 
                                                        data['workspaceNum'], 
                                                        test_size=0.2, 
                                                        random_state=42)

    # Train the decision tree classifier
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Make predictions on the current window
    current_window = run(["xdotool", "getwindowfocus", "getwindowname"], capture_output=True, text=True).stdout.strip()
    current_window_data = pd.DataFrame([[current_window, 0, 0, 0, 0, 0, 1]], columns=data.columns[:-1])
    current_window_data = pd.get_dummies(current_window_data, columns=['name'])
    prediction = model.predict(current_window_data.drop('workspaceNum', axis=1))

    # Switch to the predicted workspace
    run(["qtile-cmd", "workspace", str(prediction[0])])
