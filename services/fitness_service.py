def calculate_metrics(age,weight,height,gender,goal,activity_level):

    #BMR
    if gender == "male":
        bmr = 10 * weight + 6.25 *height - 5*age + 5
    else:
        bmr = 10 * weight + 6.25 *height - 5*age - 161

    #activity multipiers

    activity_factor = {

        "low":1.2,
        "medium":1.55,
        "high":1.735,
        "very high":1.9 
      }
    TDEE = bmr * activity_factor[activity_level]

    

    if goal == "weight loss":
        calorie_target = TDEE - 300 
    elif goal == "weight gain" or goal == "muscle gain":
        calorie_target = TDEE + 300
    else:
        calorie_target = TDEE


    


    goal_map = {
        "weight loss":1.9,
        "weight gain":1.5,
        "muscle gain":2.0,
        "maintain fitness":1.3
    }
    protein = weight * goal_map[goal] 

    return bmr ,TDEE, protein, calorie_target