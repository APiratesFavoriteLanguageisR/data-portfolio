#install.packages("dplyr", dependencies = TRUE)
#install.packages("tidyverse", dependencies = TRUE)
#install.packages("janitor", dependencies = TRUE)
#install.packages("ggplot2", dependencies = TRUE)
#install.packages("Hmisc", dependencies = TRUE)
#install.packages("weights", dependencies = TRUE)
#install.packages("ggrepel", dependencies = TRUE)
#install.packages("car", dependencies = TRUE)
#install.packages("factoextra")

library(dplyr)
library(tidyverse)
library(janitor)
library(ggplot2)
library(Hmisc)
library(weights)
library(ggrepel)
library(car)
library(factoextra)

## If Needed##
#rm(list = ls())

seda_data <- read.csv("seda_county_long_cs_4.1.csv")
seda_data <- clean_names(seda_data)

seda_data_filtered <- filter(seda_data, stateabb == "CA")
View(seda_data_filtered)

##Exploratory Section###

glimpse(seda_data_filtered)
summary(seda_data_filtered)

summary(is.na(as.numeric(seda_data_filtered$cs_mn_all)))

seda_data_filtered %>%
  filter(!is.na(cs_mn_ecd)) %>%  
  group_by(year, subject) %>%
  dplyr::summarize(mean_score = mean(cs_mn_ecd), .groups = 'drop')

##Weighted Analysis
ela_weighted <- seda_data_filtered %>%
  filter(subject == "rla") %>%
  dplyr::summarize(
    mean_all = wtd.mean(cs_mn_all, weights = totgyb_all, na.rm = TRUE),
    mean_ecd = wtd.mean(cs_mn_ecd, weights = totgyb_ecd, na.rm = TRUE),
    mean_nec = wtd.mean(cs_mn_nec, weights = totgyb_nec, na.rm = TRUE)
  )

math_weighted <- seda_data_filtered %>%
  filter(subject == "mth") %>%
  dplyr::summarize(
    mean_all = wtd.mean(cs_mn_all, weights = totgyb_all, na.rm = TRUE),
    mean_ecd = wtd.mean(cs_mn_ecd, weights = totgyb_ecd, na.rm = TRUE),
    mean_nec = wtd.mean(cs_mn_nec, weights = totgyb_nec, na.rm = TRUE)
  )

############################################### Time Series #########################################################
seda_data_filtered %>%
  group_by(year, subject) %>%
  dplyr::summarize(mean_score = mean(cs_mn_all, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(x = year, y = mean_score, color = subject)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  geom_label_repel(
    aes(label = round(mean_score, 2)), 
    vjust = -0.8, 
    size = 3,
    show.legend = FALSE
  ) +
  scale_color_manual(values = c("mth" = "#1f77b4", "rla" = "#ff7f0e")) +
  labs(
    title = "California County-Average Achievement Over Time",
    subtitle = "Mean deviation from national average (in SD units), by subject (2009–2018)",
    x = "Year",
    y = "Standardized Score (vs. national mean)",
    color = "Subject"
  ) +
  theme_minimal(base_size = 13)

####################################### County Comparisons###########################################################

# Step 1: Filter for ELA and exclude NA values
ela_county_summary <- seda_data_filtered %>%
  filter(subject == "rla", !is.na(cs_mn_all)) %>%
  group_by(sedacountyname) %>%
  dplyr::summarize(
    avg_score = mean(cs_mn_all, na.rm = TRUE),
    .groups = "drop"
  )

# Step 2: Get Top 5 and Bottom 5 Counties
top_bottom_ela <- ela_county_summary %>%
  arrange(desc(avg_score)) %>%
  slice_head(n = 5) %>%
  bind_rows(
    ela_county_summary %>% arrange(avg_score) %>% slice_head(n = 5)
  )

# Step 3: Plot
ggplot(top_bottom_ela, aes(x = reorder(sedacountyname, avg_score), y = avg_score, fill = avg_score > 0)) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  labs(
    title = "Top and Bottom Performing Counties in ELA (2009–2018)",
    x = "County",
    y = "Mean Deviation from National Average (SD units)"
  ) +
  scale_fill_manual(values = c("TRUE" = "#4daf4a", "FALSE" = "#e41a1c")) +
  theme_minimal(base_size = 13)



# Step 1: Filter for ELA and exclude NA values
ela_weighted_county <- seda_data_filtered %>%
  filter(subject == "rla", !is.na(cs_mn_all)) %>%
  group_by(sedacountyname) %>%
  dplyr::summarize(
    weighted_avg = weighted.mean(cs_mn_all, totgyb_all, na.rm = TRUE),
    .groups = "drop"
  )

# Step 2: Get Top 5 and Bottom 5 Counties
top_bottom_ela <- ela_weighted_county %>%
  arrange(desc(weighted_avg )) %>%
  slice_head(n = 5) %>%
  bind_rows(
    ela_weighted_county %>% arrange(weighted_avg ) %>% slice_head(n = 5)
  )

# Step 3: Plot
ggplot(top_bottom_ela, aes(x = reorder(sedacountyname, weighted_avg ), y = weighted_avg , fill = weighted_avg  > 0)) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  labs(
    title = "Top and Bottom Performing Counties in ELA (2009–2018)",
    x = "County",
    y = "Mean Deviation from National Average (SD units)"
  ) +
  scale_fill_manual(values = c("TRUE" = "#4daf4a", "FALSE" = "#e41a1c")) +
  theme_minimal(base_size = 13)




# Step 1: Filter for Math and exclude NA values
math_county_summary <- seda_data_filtered %>%
  filter(subject == "mth", !is.na(cs_mn_all)) %>%
  group_by(sedacountyname) %>%
  dplyr::summarize(
    avg_score = mean(cs_mn_all, na.rm = TRUE),
    .groups = "drop"
  )

# Step 2: Get Top 5 and Bottom 5 Counties
top_bottom_math <- math_county_summary %>%
  arrange(desc(avg_score)) %>%
  slice_head(n = 5) %>%
  bind_rows(
    math_county_summary %>% arrange(avg_score) %>% slice_head(n = 5)
  )

# Step 3: Plot
ggplot(top_bottom_math, aes(x = reorder(sedacountyname, avg_score), y = avg_score, fill = avg_score > 0)) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  labs(
    title = "Top and Bottom Performing Counties in Math (2009–2018)",
    x = "County",
    y = "Mean Deviation from National Average (SD units)"
  ) +
  scale_fill_manual(values = c("TRUE" = "#4daf4a", "FALSE" = "#e41a1c")) +
  theme_minimal(base_size = 13)



# Step 1: Filter for Math and exclude NA values
math_weighted_county <- seda_data_filtered %>%
  filter(subject == "mth", !is.na(cs_mn_all)) %>%
  group_by(sedacountyname) %>%
  dplyr::summarize(
    weighted_avg = weighted.mean(cs_mn_all, totgyb_all, na.rm = TRUE),
    .groups = "drop"
  )

# Step 2: Get Top 5 and Bottom 5 Counties
top_bottom_math <- math_weighted_county %>%
  arrange(desc(weighted_avg )) %>%
  slice_head(n = 5) %>%
  bind_rows(
    math_weighted_county %>% arrange(weighted_avg ) %>% slice_head(n = 5)
  )

# Step 3: Plot
ggplot(top_bottom_math, aes(x = reorder(sedacountyname, weighted_avg ), y = weighted_avg , fill = weighted_avg  > 0)) +
  geom_col(show.legend = FALSE) +
  coord_flip() +
  labs(
    title = "Top and Bottom Performing Counties in Math (2009–2018)",
    x = "County",
    y = "Mean Deviation from National Average (SD units)"
  ) +
  scale_fill_manual(values = c("TRUE" = "#4daf4a", "FALSE" = "#e41a1c")) +
  theme_minimal(base_size = 13)
########################################## SED Comparison ###########################################################

###ELA###
# dplyr::summarize and reshape the data
ela_equity_data <- seda_data_filtered %>%
  filter(subject == "rla") %>%
  group_by(year) %>%
  dplyr::summarize(
    All_Students = mean(cs_mn_all, na.rm = TRUE),
    Econ_Disadv = mean(cs_mn_ecd, na.rm = TRUE),
    Not_Econ_Disadv = mean(cs_mn_nec, na.rm = TRUE)
  ) %>%
  pivot_longer(cols = -year, names_to = "Group", values_to = "Score")

# Plot with labels for all years
ggplot(ela_equity_data, aes(x = year, y = Score, color = Group)) +
  geom_line(size = 1.2) +
  geom_point() +
  geom_label_repel(aes(label = round(Score, 2)), vjust = -0.6, size = 3) +
  labs(
    title = "ELA Achievement by Economic Status (California Counties)",
    subtitle = "Mean Deviation from National Average (SD units)",
    x = "Year", y = "Mean Deviation from National Average (SD units)"
  ) +
  theme_minimal(base_size = 13)

###Math###
# dplyr::summarize and reshape the data
math_equity_data <- seda_data_filtered %>%
  filter(subject == "mth") %>%
  group_by(year) %>%
  dplyr::summarize(
    All_Students = mean(cs_mn_all, na.rm = TRUE),
    Econ_Disadv = mean(cs_mn_ecd, na.rm = TRUE),
    Not_Econ_Disadv = mean(cs_mn_nec, na.rm = TRUE)
  ) %>%
  pivot_longer(cols = -year, names_to = "Group", values_to = "Score")

# Plot with labels for all years
ggplot(math_equity_data, aes(x = year, y = Score, color = Group)) +
  geom_line(size = 1.2) +
  geom_point() +
  geom_label_repel(aes(label = round(Score, 2)), vjust = -0.6, size = 3) +
  labs(
    title = "Math Achievement by Economic Status (California Counties)",
    subtitle = "Mean Deviation from National Average (SD units)",
    x = "Year", y = "Mean Deviation from National Average (SD units)"
  )+
  theme_minimal(base_size = 13)

########################################## Race Comparison ##########################################################


# Recreate your long-format data frame including All Students
ela_race_long <- seda_data_filtered %>%
  filter(subject == "rla") %>%
  select(year, cs_mn_all, cs_mn_blk, cs_mn_hsp, cs_mn_wht, cs_mn_asn, cs_mn_mtr, cs_mn_nam) %>%
  rename(
    All_Students = cs_mn_all,
    Black = cs_mn_blk,
    Hispanic = cs_mn_hsp,
    White = cs_mn_wht,
    Asian = cs_mn_asn,
    Multi_Racial = cs_mn_mtr,
    Native_American = cs_mn_nam
  ) %>%
  pivot_longer(cols = c(All_Students, Black, Hispanic, White, Asian, Multi_Racial, 
                        Native_American),
               names_to = "group",
               values_to = "mean_score")

# Aggregate by year and group
ela_race_summary <- ela_race_long %>%
  group_by(year, group) %>%
  dplyr::summarize(mean_score = mean(mean_score, na.rm = TRUE), .groups = "drop")

# Plot with line, points, and labels
ggplot(ela_race_summary, aes(x = year, y = mean_score, color = group)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  geom_text_repel(aes(label = round(mean_score, 2)), size = 3, show.legend = FALSE) +
  labs(
    title = "ELA Achievement by Race (California Counties)",
    subtitle = "Mean Deviation from National Average (SD units) (2009–2018)",
    x = "Year",
    y = "Mean Deviation from National Average (SD units)",
    color = "Group"
  ) +
  theme_minimal(base_size = 13) +
  scale_color_manual(values = c(
    "All_Students" = "black",
    "Black" = "red",
    "Hispanic" = "darkgreen",
    "White" = "blue",
    "Asian" = "purple",
    "Native_American" = "chocolate",
    "Multi_Racial" = "orange"
  ))

math_race_long <- seda_data_filtered %>%
  filter(subject == "mth") %>%
  select(year, cs_mn_all, cs_mn_blk, cs_mn_hsp, cs_mn_wht, cs_mn_asn, cs_mn_mtr, cs_mn_nam) %>%
  rename(
    All_Students = cs_mn_all,
    Black = cs_mn_blk,
    Hispanic = cs_mn_hsp,
    White = cs_mn_wht,
    Asian = cs_mn_asn,
    Multi_Racial = cs_mn_mtr,
    Native_American = cs_mn_nam
  ) %>%
  pivot_longer(cols = c(All_Students, Black, Hispanic, White, Asian, Multi_Racial, 
                        Native_American),
               names_to = "group",
               values_to = "mean_score")

# Aggregate by year and group
math_race_summary <- math_race_long %>%
  group_by(year, group) %>%
  dplyr::summarize(mean_score = mean(mean_score, na.rm = TRUE), .groups = "drop")

# Plot with line, points, and labels
ggplot(math_race_summary, aes(x = year, y = mean_score, color = group)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  geom_text_repel(aes(label = round(mean_score, 2)), size = 3, show.legend = FALSE) +
  labs(
    title = "Math Achievement by Race (California Counties)",
    subtitle = "Mean Deviation from National Average (SD units) (2009–2018)",
    x = "Year",
    y = "Mean Deviation from National Average (SD units)",
    color = "Group"
  ) +
  theme_minimal(base_size = 13) +
  scale_color_manual(values = c(
    "All_Students" = "black",
    "Black" = "red",
    "Hispanic" = "darkgreen",
    "White" = "blue",
    "Asian" = "purple",
    "Native_American" = "chocolate",
    "Multi_Racial" = "orange"
  ))


######################################### Gender Comparison #########################################################
# ELA - Gender Achievement
ela_gender_data <- seda_data_filtered %>%
  filter(subject == "rla") %>%
  group_by(year) %>%
  dplyr::summarize(
    All_Students = mean(cs_mn_all, na.rm = TRUE),
    Female = mean(cs_mn_fem, na.rm = TRUE),
    Male = mean(cs_mn_mal, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  pivot_longer(cols = -year, names_to = "Group", values_to = "Score")

# Plot ELA gender graph
ggplot(ela_gender_data, aes(x = year, y = Score, color = Group)) +
  geom_line(size = 1.2) +
  geom_point() +
  geom_label_repel(aes(label = round(Score, 2)), vjust = -0.6, size = 3) +
  labs(
    title = "ELA Achievement by Gender (California Counties)",
    subtitle = "Mean Deviation from National Average (SD units)",
    x = "Year", y = "Mean Deviation from National Average (SD units)"
  ) +
  theme_minimal(base_size = 13)

# Math - Gender Achievement
math_gender_data <- seda_data_filtered %>%
  filter(subject == "mth") %>%
  group_by(year) %>%
  dplyr::summarize(
    All_Students = mean(cs_mn_all, na.rm = TRUE),
    Female = mean(cs_mn_fem, na.rm = TRUE),
    Male = mean(cs_mn_mal, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  pivot_longer(cols = -year, names_to = "Group", values_to = "Score")

# Plot Math gender graph
ggplot(math_gender_data, aes(x = year, y = Score, color = Group)) +
  geom_line(size = 1.2) +
  geom_point() +
  geom_label_repel(aes(label = round(Score, 2)), vjust = -0.6, size = 3) +
  labs(
    title = "Math Achievement by Gender (California Counties)",
    subtitle = "Mean Deviation from National Average (SD units)",
    x = "Year", y = "Mean Deviation from National Average (SD units)"
  ) +
  theme_minimal(base_size = 13)

############################################## Model ################################################################

## ELA
# Aggregate weighted average achievement score by county
ela_scores <- seda_data_filtered %>%
  filter(subject == "rla", !is.na(cs_mn_all)) %>%
  group_by(sedacountyname) %>%
  dplyr::summarize(
    avg_score = weighted.mean(cs_mn_all, totgyb_all, na.rm = TRUE),
    .groups = "drop"
  )

# Aggregate demographic variables by county
demographics <- seda_data_filtered %>%
  filter(subject == "rla") %>%
  group_by(sedacountyname) %>%
  dplyr::summarize(
    pct_ecd  = sum(totgyb_ecd, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_blk  = sum(totgyb_blk, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_wht  = sum(totgyb_wht, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_hsp  = sum(totgyb_hsp, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_asn  = sum(totgyb_asn, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_mtr  = sum(totgyb_mtr, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_aia  = sum(totgyb_nam, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_fem  = sum(totgyb_fem, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_mal  = sum(totgyb_mal, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    .groups = "drop"
  )


# Combine performance and demographics into one modeling dataset
model_df <- left_join(ela_scores, demographics, by = "sedacountyname")

# Linear regression model to see which factors are most predictive
model <- lm(avg_score ~ pct_ecd + pct_blk + pct_wht + pct_hsp + pct_asn + pct_mtr, data = model_df)
summary(model)

vif(model)


# Select and scale only the demographic predictors
pca_vars <- model_df %>%
  select(pct_ecd, pct_blk, pct_wht, pct_hsp, pct_asn, pct_mtr) %>%
  scale()

# Run Principal Component Analysis
pca_result <- prcomp(pca_vars, center = TRUE, scale. = TRUE)

# Summary of variance explained
summary(pca_result)

# View loadings (eigenvectors for PCs)
pca_result$rotation

plot(pca_result, type = "l", main = "Scree Plot of PCA")

biplot(pca_result, scale = 0)

fviz_pca_biplot(pca_result, repel = TRUE)

# Add PC scores to your dataset
model_df$PC1 <- pca_result$x[,1]
model_df$PC2 <- pca_result$x[,2]

# Correlate PC1 with average ELA scores
cor.test(model_df$PC1, model_df$avg_score)

ggplot(model_df, aes(x = PC1, y = avg_score, label = sedacountyname)) +
  geom_point(size = 2, alpha = 0.7) +
  geom_text_repel(size = 3) +
  geom_smooth(method = "lm", se = TRUE, color = "blue", linetype = "dashed") +
  labs(
    title = "Correlation Between PC1 (Demographics) and Average ELA Score",
    subtitle = "Counties with higher PC1 values tend to score lower",
    x = "Principal Component 1 Score (PC1)",
    y = "Average ELA Achievement (SD Units)"
  ) +
  theme_minimal(base_size = 13)

## Math
# Step 1: Aggregate weighted average Math score by county
math_scores <- seda_data_filtered %>%
  filter(subject == "mth", !is.na(cs_mn_all)) %>%
  group_by(sedacountyname) %>%
  dplyr::summarize(
    avg_score = weighted.mean(cs_mn_all, totgyb_all, na.rm = TRUE),
    .groups = "drop"
  )

# Step 2: Reuse demographic proportions from ELA (same structure, totals)
# If needed, change 'rla' to 'mth' in demographic block, but using 'rla' ensures shared base

demographics <- seda_data_filtered %>%
  filter(subject == "rla") %>%  # demographic totals stable across subjects
  group_by(sedacountyname) %>%
  dplyr::summarize(
    pct_ecd  = sum(totgyb_ecd, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_blk  = sum(totgyb_blk, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_wht  = sum(totgyb_wht, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_hsp  = sum(totgyb_hsp, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_asn  = sum(totgyb_asn, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_mtr  = sum(totgyb_mtr, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_aia  = sum(totgyb_nam, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_fem  = sum(totgyb_fem, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    pct_mal  = sum(totgyb_mal, na.rm = TRUE) / sum(totgyb_all, na.rm = TRUE),
    .groups = "drop"
  )

# Step 3: Merge into math model dataset
model_df_math <- left_join(math_scores, demographics, by = "sedacountyname")

# Step 4: Linear regression
model_math <- lm(avg_score ~ pct_ecd + pct_blk + pct_wht + pct_hsp + pct_asn + pct_mtr, data = model_df_math)
summary(model_math)

# Check multicollinearity
vif(model_math)

# Step 5: Run PCA on demographic predictors
pca_vars_math <- model_df_math %>%
  select(pct_ecd, pct_blk, pct_wht, pct_hsp, pct_asn, pct_mtr) %>%
  scale()

pca_result_math <- prcomp(pca_vars_math, center = TRUE, scale. = TRUE)

# Step 6: Output
summary(pca_result_math)
pca_result_math$rotation

# Visuals
plot(pca_result_math, type = "l", main = "Scree Plot of PCA (Math)")
biplot(pca_result_math, scale = 0)

fviz_pca_biplot(pca_result_math, repel = TRUE)

# Step 7: Correlate PC1 with avg Math score
model_df_math$PC1 <- pca_result_math$x[,1]
model_df_math$PC2 <- pca_result_math$x[,2]

cor.test(model_df_math$PC1, model_df_math$avg_score)

# Step 8: Plot
ggplot(model_df_math, aes(x = PC1, y = avg_score, label = sedacountyname)) +
  geom_point(size = 2, alpha = 0.7) +
  geom_text_repel(size = 3) +
  geom_smooth(method = "lm", se = TRUE, color = "blue", linetype = "dashed") +
  labs(
    title = "Correlation Between PC1 (Demographics) and Average Math Score",
    subtitle = "Counties with higher PC1 values tend to score lower",
    x = "Principal Component 1 Score (PC1)",
    y = "Average Math Achievement (SD Units)"
  ) +
  theme_minimal(base_size = 13)
