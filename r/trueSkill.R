# ---------------------------------------------------------------------------- #
# World Cup: True Skill Rating 
# Ver: 0.01
# ---------------------------------------------------------------------------- #

# Environment ------------------------------------------------------------------

# Clean environment
rm(list = ls())
gc()
options(scipen = 999)

# Install packages
listOfPackages <- c("data.table", "trueskill", "rvest", "XML", "httr")
newPackages    <- listOfPackages[!(listOfPackages %in% installed.packages()[ ,"Package"])]
if(length(newPackages)) {
  install.packages(newPackages)
}

# Load packages
invisible(sapply(listOfPackages, library, character.only = TRUE))
rm(listOfPackages, newPackages)
gc()

 
# Scrape Data ------------------------------------------------------------------

# Teams list
teamNumber <- 32
node       <- "h3"
url        <- "https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_squads"
teamName   <- read_html(url) %>% html_nodes(node) %>% html_text()
team <- readHTMLTable(doc = content(GET(url), "text"))
team <- team[1:teamNumber]
names(team) <- teamName[1:teamNumber]
team <- rbindlist(team, idcol = TRUE)
setnames(team, ".id", "Team")
team[ ,Player := gsub(" \\(captain\\)", "", Player)]
team <- team[ ,c("Team", "Player")]

# Scrape ratings from https://www.whoscored.com
xpath <- '//*[@id="mw-content-text"]'
url  <- "https://www.whoscored.com/Statistics"


# TrueSkill --------------------------------------------------------------------

# Matchup
Ateam <- "Iran"
Bteam <- "Spain"

# Composition





