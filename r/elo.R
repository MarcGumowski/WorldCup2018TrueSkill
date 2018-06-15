# ---------------------------------------------------------------------------- #
# World Cup: Elo Rating 
# Ver: 0.01
# ---------------------------------------------------------------------------- #

# Environment ------------------------------------------------------------------

# Clean environment
rm(list = ls())
gc()
options(scipen = 999)

# Install packages
listOfPackages <- c("data.table", "elo", "rvest", "XML", "httr", "ggplot2")
newPackages    <- listOfPackages[!(listOfPackages %in% installed.packages()[ ,"Package"])]
if(length(newPackages)) {
  install.packages(newPackages)
}

# Load packages
invisible(sapply(listOfPackages, library, character.only = TRUE))
rm(listOfPackages, newPackages)
gc()


# Data ------------------------------------------------------------------------

rating <- fread("csv/teamRating_17_05_2018.csv", encoding = "UTF-8")


# Elo -------------------------------------------------------------------------

# Matchup
Ateam <- "Egypt"
Bteam <- "Uruguay"

# Team
a <- rating[Team %in% Ateam, ]
b <- rating[Team %in% Bteam, ]

# Prob
Aprob <- elo.prob(~ a$`Elo Rating` + b$`Elo Rating`)
Bprob <- 1 - elo.prob(~ a$`Elo Rating` + b$`Elo Rating`)

matchup <- data.table(team = c(Ateam, Bteam), prob = c(Aprob, Bprob))
ggplot(matchup, aes(x = team, y = prob, fill = team)) +
  geom_col() +
  ggtitle("Match-up winning probabilites based on Elo rating") +
  scale_fill_manual(values = c("#DE7A22", "#6AB187")) +
  theme_bw() +
  guides(fill = FALSE)

print(paste0(Ateam, " winning probability is ", round(Aprob * 100, digits = 2), "%")) 
print(paste0(Bteam, " winning probability is ", round(Bprob * 100, digits = 2), "%")) 



