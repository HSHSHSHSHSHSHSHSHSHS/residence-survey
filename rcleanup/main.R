##Library stuff
library(tidyverse) #very important
library(magrittr) #pipes
library(shiny) #dashboard
library(shinydashboard) #dashboard
library(reactable)
library(dplyr) #important
library(ggplot2) #important
library(GGally) #more gg plot
library(stringr)

##Cleaning data! yippee

# Import ------------------------------------------------------------------

dininghall_og <- read_csv("/Users/weeb/Downloads/*data proj/Dining/Dining Hall R/dininghall.csv") #backup do not touch!
dininghall <- read_csv("/Users/weeb/Downloads/*data proj/Dining/Dining Hall R/dininghall.csv") #use
glimpse (dininghall)


# rename qs ---------------------------------------------------------------

dininghall <- dininghall %>%
  rename("Responder_Number" = 'Responder #',
         "Eating_Freq" =  'How often do you eat at dining halls?',
         "Residence" = 'Residence?',
         "Mealplan" = 'Mealplan?',
         "Bring_Back" = 'Bring back?',
         "Main_Factor" = 'Why takeout over dine in?',
         "Details" = 'Details?',
         "Takeout_Freq" = 'How often would you takeout?',
         "Max_Pay" = 'How much would you pay?',
         "Food_Thievery" = 'Have you taken food out before?',
         "Bought_Takeout" = 'Have you bought mcgill takeout?',
         "Why_Not" = 'Why not?',
         "Delivery_Freq" = 'How often do you Uber Eats?',
         "Cost_Factor" = 'Cost importance',
         "Speed_Factor" = 'Speed Importance',
         "Quality_Factor" = 'Quality importance',
         "Variety_Factor" = 'Variety importance') %>%
  select(-Residence, -Details)

# Filter out demographics only responders ---------------------------------

dininghall_filtered <- dininghall %>%
  filter(!is.na(Bring_Back)
         | !is.na(Main_Factor)
         | !is.na(Takeout_Freq)
         | !is.na(Max_Pay)
         | !is.na(Food_Thievery)
         | !is.na(Bought_Takeout)
         | !is.na(Why_Not)
         | !is.na(Delivery_Freq)
         | !is.na(Cost_Factor)
         | !is.na(Speed_Factor)
         | !is.na(Quality_Factor)
         | !is.na(Variety_Factor))

# Mutate NAs --------------------------------------------------------------

dininghall_filtered$RVC <- ifelse(is.na(dininghall_filtered$RVC), "2", dininghall_filtered$RVC)
dininghall_filtered$BMH <- ifelse(is.na(dininghall_filtered$BMH), "2", dininghall_filtered$BMH)
dininghall_filtered$New <- ifelse(is.na(dininghall_filtered$New), "2", dininghall_filtered$New)
dininghall_filtered$C4 <- ifelse(is.na(dininghall_filtered$C4), "2", dininghall_filtered$C4)
dininghall_filtered$Eating_Freq <- ifelse(is.na(dininghall_filtered$Eating_Freq), "Missing", dininghall_filtered$Eating_Freq)
dininghall_filtered$Mealplan <- ifelse(is.na(dininghall_filtered$Mealplan), "Missing", dininghall_filtered$Mealplan)

# Mutate Y_N to 1 0 -------------------------------------------------------

dininghall_filtered_check <- dininghall_filtered %>%
  mutate(RVC = ifelse(RVC == "Yes", 1, ifelse(RVC == "No", 0, 2)),
         BMH = ifelse(BMH == "Yes",1, ifelse(BMH == "No", 0, 2)),
         New = ifelse(New == "Yes",1,ifelse(New == "No", 0, 2)),
         C4 = ifelse(C4 == "Yes",1,ifelse(C4 == "No", 0, 2))
         ) #%>%
  #mutate_at(vars(RVC:C4), as.numeric)

# Mutate thievery ---------------------------------------------------------

dininghall_filtered_plus_plus <- dininghall_filtered_check %>%
  mutate(Food_Thievery_YN = Food_Thievery)

dininghall_filtered_ex <- dininghall_filtered_plus_plus %>%
  mutate(Food_Thievery_YN = recode(Food_Thievery_YN,
                                      "never" = 'No',
                                      "rarely" = 'Yes',
                                      "sometimes"='Yes',
                                      "often" = 'Yes'
  ))


# Code qualitative --------------------------------------------------------

dininghall_filtered_plus <- dininghall_filtered_ex %>%
  mutate(Why_Not_Qualitative = Why_Not)

dininghall_filtered_extra <- dininghall_filtered_plus %>%
  mutate(Why_Not_Qualitative = recode(Why_Not_Qualitative,
                                      "it is not available in my residence" = "Availability",
                                      "I but from the cafés. Most dining halls don't have takeout like this." = 'Availability',
                                      "To spenny" = 'Price',
                                      "too expensive!"='Price',
                                      "it's not as good quality tbh" = 'Quality',
                                      "no variety and i don't want to pay extra" = "Variety, Price",
                                      "Not accesible to students with allergies" = "Accessibility",
                                      "Lack of houses and not fresh" = "Variety, Quality",
                                      "Because I want actual sushi not pepper and carrot sushi" = 'Quality',
                                      "Quality versus price, grab n go quality is awful" = 'Quality, Price',
                                      "Not part of MANDATORY meal plan that I pay 6500 for (more expensive than paying per entry)" = 'Price',
                                      "price and quality/variety of food" = 'Price, Quality, Variety',
                                      "Price, quality, variety" = 'Price, Quality, Variety',
                                      "Looks gross" = "Quality",
                                      "quality/variety" = "Quality, Variety"
  ))


# Export lol --------------------------------------------------------------

write.csv(dininghall_filtered_extra,file='/Users/weeb/Downloads/*data proj/Dining/Dining Hall R/Dininghall_r.csv', row.names=FALSE)