library(shiny)
library(data.table)

teams_list = unique(fread('app_data/upd_game_df.csv',drop = 1)$winner_name)

# Define UI for application that draws a histogram
ui <- 
  navbarPage(title ="NHL App Prototype",
             tabPanel(title = "Ice Time",
                      value = "IT",
                      fluidPage(
                        fluidRow(
                          splitLayout(cellWidths = c("5%","30%", "30%",'30%',"5%"),
                                      div(),
                                      selectInput(inputId = 'selected_team1',
                                                  selected = 'Calgary Flames',
                                                  label = 'Team 1',
                                                  choices = teams_list,
                                                  multiple = FALSE,
                                                  selectize = FALSE),
                                      selectInput(inputId = 'selected_team2',
                                                  selected = 'Edmonton Oilers',
                                                  label = 'Team 2',
                                                  choices = teams_list,
                                                  multiple = FALSE,
                                                  selectize = FALSE),
                                      HTML(paste0("<b>","Entire NHL","</b>")),
                                      div()
                                      )
                          ),
                        fluidRow(
                          splitLayout(cellWidths = c("5%","30%", "30%", '30%',"5%"),
                                      div(),
                                      plotOutput("avgIceTime1",height = '1200px'), 
                                      plotOutput("avgIceTime2",heigh = '1200px'),
                                      plotOutput("avgIceTimeLeague",heigh = '1200px'),
                                      div()
                                      )
                          )
                        ) #Close fluidPage
             ),
             tabPanel(title = "Shift Duration",
                     value = "SD",
                     fluidPage(
                       fluidRow(
                         splitLayout(cellWidths = c("5%","30%", "30%",'30%',"5%"),
                                     div(),
                                     selectInput(inputId = 'selected_team3',
                                                 selected = 'Calgary Flames',
                                                 label = 'Team 1',
                                                 choices = teams_list,
                                                 multiple = FALSE,
                                                 selectize = FALSE),
                                     selectInput(inputId = 'selected_team4',
                                                 selected = 'Edmonton Oilers',
                                                 label = 'Team 2',
                                                 choices = teams_list,
                                                 multiple = FALSE,
                                                 selectize = FALSE),
                                     HTML(paste0("<b>","Entire NHL","</b>")),
                                     div()
                         )
                       ),
                       fluidRow(
                         splitLayout(cellWidths = c("5%","30%", "30%", '30%',"5%"),
                                     div(),
                                     plotOutput("avgNumShift1",height = '1200px'), 
                                     plotOutput("avgNumShift2",heigh = '1200px'),
                                     plotOutput("avgShiftLeague",heigh = '1200px'),
                                     div(),
                                     div()
                                     )
                         )
                       ) #Close fluidPage
                     )#Close Ice Time Panel
             )#Close NavBarPage

server <- function(input, output) {
  
  source('avg_shift_plots.R')
  
  output$avgNumShift1 <- renderPlot({
    team_avg_shift(input$selected_team3)
  })
  
  output$avgNumShift2 <- renderPlot({
    team_avg_shift(input$selected_team4)
  })
  
  output$avgIceTime1 <- renderPlot({
    team_avg_iceTime(input$selected_team1)
  })
  
  output$avgIceTime2 <- renderPlot({
    team_avg_iceTime(input$selected_team2)
  })
  
  output$avgIceTimeLeague <- renderPlot({
    league_avg_iceTime()
  })
  
  output$avgShiftLeague <- renderPlot({
    league_avg_shift()
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)

