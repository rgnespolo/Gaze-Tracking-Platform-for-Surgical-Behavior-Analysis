#library(dplyr)
library(tidyverse)
library(saccades)
summary_saccades_fixation <- read_csv("./saccades_fixation_summary_Copy.csv")
users = list('yannek', 'daniel', 'george', 'monique', 'mara', 'emily')
# subspecialty = ('retina', 'cataract', 'other')
# subspecialty_user = (1, 1, 1, 1, 3, 2]
# years_oph = [20, 4, 4, 8, 7, 4]
# years_sub = [10, 1, 1, 2, 2, 1]
phases = list('rhexis', 'phaco', 'cortex', 'core_vitr', 'memb_peel', 'laser')


for (i in 1:6){ #phase
  for (j in 1:6){ #user
    print('a')
    df_single_user <- filter(summary_saccades_fixation, user_code == j, phase_code == i)
    print(df_single_user['No. of fixations per trial'].mean()
  }
}