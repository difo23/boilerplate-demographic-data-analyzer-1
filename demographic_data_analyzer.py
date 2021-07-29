import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('./adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race = df['race']
    race_count = race.groupby(race).count()
    race_count = race_count.tolist()
    race_count.sort(reverse=True)
    
 
  
 
    # What is the average age of men?
    average_age_men = df.query("sex == 'Male' ")['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    total = df['education'].count()
    percentage_bachelors = df.query("education == 'Bachelors'").count().education * 100 / total
    percentage_bachelors = percentage_bachelors.round(1)
  

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    people_with_adv_ed_and_hig_salary = df.query("(education =='Bachelors' or education == 'Masters' or education == 'Doctorate') and salary == '>50K' ") 
    people_with_adv_ed = df.query("(education =='Bachelors' or education == 'Masters' or education == 'Doctorate') ")
    higher_education_rich = people_with_adv_ed_and_hig_salary.count().education * 100/ people_with_adv_ed.count().education 
    
    higher_education_rich = higher_education_rich.round(1)
 
    people_without_adv_ed = df.query("not (education =='Bachelors' or education == 'Masters' or education == 'Doctorate') ") 

    total = people_without_adv_ed.count().education
    people_without_adv_ed_and_hig_salary = df.query("not (education =='Bachelors' or education == 'Masters' or education == 'Doctorate') and salary == '>50K' ") 
    without_education = people_without_adv_ed_and_hig_salary.count().education
    lower_education_rich = without_education * 100 / total
    lower_education_rich = lower_education_rich.round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours= df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    people_mim_hour_week_and_hig_salary = df[df['hours-per-week'] == min_work_hours].query("salary == '>50K'")
    people_mim_hour_week = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = people_mim_hour_week_and_hig_salary.count().education * 100 / people_mim_hour_week.count().education

    grouped = df.groupby(["native-country"])['salary'].agg('count')
    total_people_country = grouped.to_frame(name= 'total_people')
    total_people_country['country'] = total_people_country.index
    grouped_salary = df.groupby(['native-country' , 'salary'])['native-country'].agg('count')
    total_people_salary = grouped_salary.to_frame()
    total_salary_country = total_people_salary.unstack(level='salary')
    total_salary_country['country'] = total_salary_country.index

    total_salary_salary_50K = total_salary_country[('native-country')]['>50K'].values
    total_salary_salary_menor_50K = total_salary_country[('native-country')]['<=50K'].values

    total_people_country['>50K'] = total_salary_salary_50K
    total_people_country['<=50K'] = total_salary_salary_menor_50K

    total_people_country['pergentage_high'] = total_people_country['>50K'] * 100/total_people_country['total_people']

    total_people_country['pergentage_low'] = total_people_country['<=50K'] * 100/ total_people_country['total_people']

    total_people_country[total_people_country.pergentage_high ==total_people_country.pergentage_high.max()].country[0]

    highest_earning_country = total_people_country[total_people_country.pergentage_high ==total_people_country.pergentage_high.max()].country[0]

    highest_earning_country_percentage = total_people_country.pergentage_high.max().round(1)

    df= df.rename(columns= {'native-country': 'country'})
    occupations = df.query("salary == '>50K' and country == 'India'").groupby('occupation')['salary'].count()
    occupations= occupations.to_frame(name=None)
    occupations['occupations'] = occupations.index

    top_IN_occupation = occupations[occupations.salary == occupations.salary.max()]['occupations'][0]
  
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

