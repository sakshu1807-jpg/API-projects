import pandas as pd

def convert_dict_to_df(details: dict) -> pd.DataFrame:
    new_df = pd.DataFrame([details])
    return new_df

def preprocess_new_data(new_df: pd.DataFrame, oe, scalar) -> pd.DataFrame:
    processed_df = new_df.copy()

    processed_df['Sex'] = processed_df['Sex'].map({'M': 1, 'F': 0})
    processed_df['ExerciseAngina'] = processed_df['ExerciseAngina'].map({'Y': 1, 'N': 0})
    processed_df = processed_df.rename(columns=
        {
            'Sex': 'is_Male', 
            'ExerciseAngina': 'is_EA'
        }
    )

    cols_to_be_encoded = ['ChestPain', 'ST_Slope', 'RestingECG']
    processed_df[cols_to_be_encoded] = oe.transform(processed_df[cols_to_be_encoded])

    processed_df['MaxHRcase'] = pd.cut(processed_df['MaxHR'],
                                       bins=[0, 138, 154, float('inf')],
                                       labels=['High', 'very_low', 'High'], ordered=False)
    processed_df['MaxHRcase'] = processed_df['MaxHRcase'].map({'High': 1, 'very_low': 0})

    processed_df['Cholesterolcase'] = pd.cut(processed_df['Cholesterol'],
                                         bins=[85, 200, 250, float('inf')],
                                         labels=['Low', 'High', 'Very High'], ordered=False, include_lowest=True)
    processed_df['Cholesterolcase'] = processed_df['Cholesterolcase'].map({'Low': 0, 'High': 1, 'Very High': 2})

    processed_df['Oldpeakcase'] = pd.cut(processed_df['Oldpeak'],
                                         bins=[-float('inf'), -2, -1, 1, 2, float('inf')],
                                         labels=['Very High', 'High', 'Low', 'High', 'Very High'], ordered=False)
    processed_df['Oldpeakcase'] = processed_df['Oldpeakcase'].map({'Very High': 2, 'High': 1, 'Low': 0})

    num_cols_to_scale = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
    processed_df[num_cols_to_scale] = scalar.transform(processed_df[num_cols_to_scale])

    return processed_df

def final_prediction(final_df: pd.DataFrame, model) -> int:
    prediction = int(model.predict(final_df)[0])
    return prediction