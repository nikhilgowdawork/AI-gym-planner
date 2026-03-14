
import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from services.groq_service import generate_plan
from services.fitness_service import calculate_metrics
from services.prompt_service import build_response
import json
import pandas as pd 
from services.pdf_service import create_pdf


load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions" 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("API key not found. Please set GROQ_API_KEY in .env file.")
    st.stop()
    
# initialize state- we have to define every varaibles we use in the code,it should be stored in
# session state not in seperate variables 

if "page" not in st.session_state:
     st.session_state["page"] = 1
     st.session_state["age"] = None
     st.session_state["weight"] = None
     st.session_state["height"] = None
     st.session_state["Goal"] = None
     st.session_state["diet_type"] = None
     st.session_state["additional_detail"] = None
     st.session_state["exercise_place"]= None
     st.session_state["your_personalized_plan"]=None
     st.session_state["BMR"] = None
     st.session_state["TDEE"] = None
     st.session_state["protein_intake"] = None 
     st.session_state["daily_activity_level"]= None
     st.session_state["gender"]= None
     st.session_state["calorie_target"]= None
#page 1
if st.session_state["page"] == 1:
     st.title("AI GYM PLANNER")

     if st.button("start",key="start"):
          st.session_state["page"] = 2
          st.rerun()

#page 2
elif st.session_state["page"] == 2:
     st.session_state["age"] = st.number_input("AGE", min_value=0, max_value=100, value=1,step=1)
     st.caption("Age must be above 15 to get Personlized Plans. ")
     st.session_state["weight"] = st.number_input("WEIGHT (kg)",min_value=None, max_value=300,value=None, step=1)
     st.session_state["height"] = st.number_input("HEIGHT (cm)", min_value=None, max_value=250,value=None, step=1)
     st.session_state["Goal"] = st.selectbox("Goal",
                            [None,"weight loss","weight gain","muscle gain","maintain fitness"],
                            format_func=lambda x :"select Goal" if x is None else x     )
     st.session_state["diet_type"] = st.selectbox("diet type",
                            [None,"vegetarian","non-vegetarian","eggitarian","veg and non-veg"],
                            format_func=lambda x :"select diet type" if x is None else x     )
     st.session_state["exercise_place"] = st.selectbox("workout place",
                                                       [None,"home","gym"],
                                                       format_func=lambda x :"workout place" if x is None else x)
     st.session_state["daily_activity_level"]= st.selectbox("daily activity level",
                         [None,"low","medium","high","very high"],format_func=lambda x :"daily activity level" if x is None else x
                         )                                                  
     st.session_state["gender"] =st.selectbox("gender",
                                   [None,"male","female"],
                                   format_func=lambda x :"gender" if x is None else x
                                   )
     

if st.session_state["page"] == 2:     
 if  st.button("back"):
     st.session_state["page"] -= 1
     st.rerun()



#store user data in one variable 
user_data=f"""
Age: {st.session_state["age"]}
Weight: {st.session_state["weight"]} kg
Height: {st.session_state["height"]} cm
Goal: {st.session_state["Goal"]}
Diet Type: {st.session_state["diet_type"]}
Workout Place: {st.session_state["exercise_place"]}
Activity Level: {st.session_state["daily_activity_level"]}
Additional Details: {st.session_state["additional_detail"]}
"""

#button to submit the data and show back to user
if st.session_state["page"] == 2:

    if  st.session_state["age"] < 15:
      st.warning("Structured gym training is not recommended for user with age > 15 years. ")
      st.stop()
    
    required_feilds =[
         st.session_state["age"],
          st.session_state["weight"],
          st.session_state["height"],
          st.session_state["Goal"],
          st.session_state["diet_type"],
          st.session_state["exercise_place"],
          st.session_state["daily_activity_level"],
          st.session_state["gender"]
         ]
         
    if any (feild is None for feild in required_feilds):
         st.warning("Please complete all previous steps before generating the plan.")

     
    else:
        if st.button("submit",key="submit"):
         st.session_state["page"] = 3
         st.rerun()
    
    

    
     

#page 3
elif st.session_state["page"] == 3:
 st.write("ADDITIONAL DEATAILS/IMPORTANT DETAILS TO NOTE THEM AND ALTER THE RESPONSE ACCORDINGLY...like any injuries,recovered fratures,budget amd more will in generating effective reponse... :")
        
 st.session_state["additional_detail"] = st.chat_input("DESCRIPTION")

if st.session_state["page"] == 3:
             
 if  st.button("back"):
     st.session_state["page"] = 2
     st.rerun()
     

 if  st.button("submit",key="submit_page3"):
     st.session_state["page"] = 4
     st.rerun()
     



     

#page 4 - AI Analysis and Plans
elif st.session_state["page"] == 4:
     st.title("Your Personalized Plans")

     st.subheader("BMR, TDEE and Protein Intake Calculation :")
     

     #calculation function from fitness_sevice
     bmr,TDEE,protein,calorie_target = calculate_metrics (
         
         age=st.session_state["age"],
         weight=st.session_state["weight"],
         height=st.session_state["height"],
         gender=st.session_state["gender"],
         goal=st.session_state["Goal"],
         activity_level=st.session_state["daily_activity_level"]
         
         )
     

     st.session_state["BMR"] = bmr
     st.session_state["TDEE"] = TDEE
     st.session_state["protein_intake"] = protein
     st.session_state["calorie_target"] = calorie_target
        
     
     st.write(f"**BMR :** {bmr:.2f} calories/day")
     st.write(f"**TDEE :** {TDEE:.2f} calories/day")
     st.write(f"**Recommended Protein Intake :** {protein:.2f} grams/day")
     st.write(f"**Target Daily Calories :** {calorie_target:.2f} kcal/day")

     
     system_prompt = build_response(
         user_data,
         bmr,
         TDEE,
         protein,
         calorie_target
         
     ) 

generation_config={
    "temperature":1,
    "top_p":0.95,
    "top_k":40,
    "max_output_tokens":8192,
    "response_mime_type":"text/plain"

}
if st.session_state["page"] == 4:
     
     if st.session_state["your_personalized_plan"] is None:
            if st.button("Generate Plans", key="generate_plans"):
             with st.spinner("AI is creating your personalized plan..."):
               try:
                   generate_text = generate_plan(system_prompt)
                   plan_data = json.loads(generate_text)

                   st.session_state["your_personalized_plan"] = plan_data
                   st.write("plan generated successfully with AI!")
               except Exception as e:
                   st.error("something went wrong whike genrating your plan . plese try agian later.")
                   print("ERROR", e)
                   st.stop()
                    
     # Display the plan if generated
     if st.session_state["your_personalized_plan"] :
          st.divider()
          plan = st.session_state["your_personalized_plan"]

          intro = plan["introduction"]
          exercise_data = plan["exercise_plan"]
          diet_data = plan["diet_plan"]
          supplements = plan["supplements"]
          tips = plan["health_tips"]
          closing = plan["closing_message"]

          st.write(intro)

          st.subheader("7-Days Exercise Plan")
          exercise_df = pd.DataFrame(exercise_data)
          st.table(exercise_df)

          st.subheader("7-Day Diet Plan")
          diet_df = pd.DataFrame(diet_data)
          st.table(diet_df)

          st.subheader("Supplements")
          for s in supplements:
               st.write("•", s)

          st.subheader("Health Tips")
          for t in tips:
              st.write("•",t)

          st.write(closing)

          pdf_file = create_pdf(exercise_data, diet_data, supplements, tips)


     if st.session_state["your_personalized_plan"] != None:
         if st.button("Regenerate Plan"):
          with st.spinner("regenerating..."):
            try:
                   generate_text = generate_plan(system_prompt)
                   plan_data = json.loads(generate_text)

                   st.session_state["your_personalized_plan"] = plan_data
                   
            except Exception as e:
                   st.error("Failed to regenrate the Plan.")
                   print("ERROR", e)
                   
     # Navigation buttons
     col1, col2, col3 = st.columns(3)
     with col1:
          if st.button("Back", key="back_page4"):
               st.session_state["page"] = 3
               st.rerun()
     with col2:
         if st.session_state["your_personalized_plan"]:
          st.download_button(
          "Download Plan as PDF",
          pdf_file,
          "AI_Fitness_Plan.pdf",
          "application/pdf"
     )
         
     with col3:
          if st.button("Start Over", key="start_over"):
               st.session_state.clear()
               st.sessiom_state["page"] = 1
               st.rerun()
