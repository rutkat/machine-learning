import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    total_count = len(df)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series(df['race'].value_counts())
    
    # What is the average age of men?
    men_age = df.loc[df['sex'] == 'Male']
    average_age_men = men_age['age'].mean().round(0)
    
    # print('\nAvg age men: ', average_age_men)

    # What is the percentage of people who have a Bachelor's degree?
    # print(df['education'].value_counts().get('Bachelors', 0))
    # print((df['education'] == 'Bachelors').sum())
    bachelor_count = (df['education'] == 'Bachelors').sum() / total_count
    percentage_bachelors = (bachelor_count * 100).round(2)
    
    # print(f'percentage_bacherlors: {percentage_bachelors}%')

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    higher_ed_df = df[(df['salary'] == '>50K') \
        & ((df['education'] == 'Bachelors') \
            |  (df['education'] == 'Masters') \
            |  (df['education'] == 'Doctorate'))]

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = ((len(higher_ed_df) / total_count) * 100)
     
    # print(f'higher_education: {higher_education}%') 

     # What percentage of people without advanced education make more than 50K?
    lower_ed_df = df[(df['salary'] == '>50K') \
        & ((df['education'] != 'Bachelors') \
            &  (df['education'] != 'Masters') \
            &  (df['education'] != 'Doctorate'))] 
    
    lower_education = ((len(lower_ed_df) / total_count) * 100)

    # print(f'lower_education: {lower_education}%')

    # percentage with salary >50K
    higher_education_rich = higher_education
    lower_education_rich = lower_education

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = ((df['hours-per-week'] <= min_work_hours & (df['salary'] == '>50K')).sum() / total_count)

    rich_percentage = num_min_workers

    # What country has the highest percentage of people that earn >50K?
    highest_countries = df[(df['salary'] == '>50K')]['native-country'].value_counts()

    highest_earning_country = highest_countries.index[0]

    highest_earning_country_percentage = (highest_countries[0] / len(df['native-country'] == highest_earning_country)) * 100

    india_occu = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = india_occu['occupation'].value_counts().index[0]
    
    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

calculate_demographic_data(0)

