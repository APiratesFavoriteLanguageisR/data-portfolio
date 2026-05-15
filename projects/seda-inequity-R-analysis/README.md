# California K-12 Achievement Gap Analysis (SEDA 2009-2018)

## Overview

This project performs statistical analysis of educational datasets using R, which looks for patterns in student outcomes and applies statistical methods to understand relationships between demographic and performance variables. The dataset used is SEDA data from the Educational Opportunity Project at Stanford University [source](https://edopportunity.org/). The data includes ELA and Math scores for students throughout California from 2009 - 2018.

The analysis aims to uncover if any factors are directly correlated with student test scores, including location, school socioeconomic disadvantage (SED) status percentage, and ethnicity/race makeup. Linear Regression and Principal Component Analysis (PCA) methods are used to uncover the insights discussed later.

## Tech Stack

- R
  
- `tidyverse` - Data science and visualization R package [CRAN](https://cran.r-project.org/web/packages/tidyverse/index.html)
  
- `dplyr` - R package intended for using and manipulating dataframes [CRAN](https://cran.r-project.org/web/packages/dplyr/index.html)
  
- `janitor` - R package that helps clean and examine messy datasets [CRAN](https://cran.r-project.org/web/packages/janitor/index.html)
  
- `ggplot2` - R package for creating customizable visualizations. Loaded individually for explicit dependency tracking, also included in tidyverse [CRAN](https://cran.r-project.org/web/packages/ggplot2/index.html)
  
- `Hmisc` - General data analysis toolkit R package [CRAN](https://cran.r-project.org/web/packages/Hmisc/index.html)
  
- `weights` - R package used for computing weighted statistics [CRAN](https://cran.r-project.org/web/packages/weights/index.html)
  
- `ggrepel` - ggplot2 extension for improved labeling [CRAN](https://cran.r-project.org/web/packages/ggrepel/index.html)
  
- `car` - R package used for regression analysis [CRAN](https://cran.r-project.org/web/packages/car/index.html)
  
- `factoextra` - R package used for Principal Component Analysis (PCA) [CRAN](https://cran.r-project.org/web/packages/factoextra/index.html)

## How to Run

- First, make sure to have R and RStudio installed
  - Install R here: [R](https://www.r-project.org/)
  - Install Rstudio here: [Rstudio](https://posit.co/downloads)
- Clone the repo from Github
- Make sure to navigate to where the R script is installed using the session > set working directory button in Rstudio or simply open the R script in RStudio. Note: the working directory should be set to the project root, not the script location
- Install any needed libraries or dependencies above (the installation code is commented out at the top of the script. Simply uncomment it once to install the packages)
- Either run the script line by line or run it all at once.
- plots will render in the RStudio viewer pane

## Key Findings

Overall, Math and English Language Arts (ELA) scores generally improved from 2009 - 2018.

When looking at both Math and ELA test scores at the county level, Marin, Placer, and Santa Clara Counties consistently ranked among the top performers, while Lake, Mendocino, Glenn, and Monterey Counties were among the lowest.

The more interesting findings, however, are uncovered when looking at individual student groups.

- Non-economically disadvantaged students far outperformed economically disadvantaged students.
- Female students, on average, outperformed male students.
- There were relatively large discrepancies between higher performing races (Asian/White) and lower performing races (Black/Hispanic)
- Principal Component Analysis confirmed that demographic composition, particularly economic disadvantage and Hispanic population percentage, were associated with lower county level achievement scores. Note: PCA captures variance across counties rather than individual level inequity. Black students score similarly low to Hispanic students in direct comparisons but load onto a secondary component (PC2) due to smaller and less variable Black populations across California counties.

For both subjects, the analysis uncovered that student demographics were correlated with test scores, meaning there are some gaps in achievement within California county schools for certain underserved student groups. These findings suggest persistent equity gaps that warrant further investigation.

## What is Next?

- This analysis could be further expanded to all states, rather than California.
- The current analysis cuts off at 2018. However, it would be very interesting to extend to the most recent state test year, especially to include and analyze student performance during the COVID pandemic.
- Further considerations for this analysis could include formally applying the Kaiser criterion to eigenvalue selection rather than relying on visual scree plot interpretation, as well as cross validation or adjusted R-squared analysis to assess whether the regression model generalizes beyond the current sample.