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
listOfPackages <- c("data.table", "elo", "rvest", "XML", "httr")
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
elo.prob(~ a$`Elo Rating` + b$`Elo Rating`)
1 - elo.prob(~ a$`Elo Rating` + b$`Elo Rating`)
