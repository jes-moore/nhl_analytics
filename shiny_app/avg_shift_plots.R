library(data.table)
library(dplyr)
library(ggplot2); theme_set(theme_minimal)
library(gridExtra)
library(varhandle)
team_avg_shift <- function(team_name){
  #Load all Data
  games_df = fread('app_data/upd_game_df.csv',drop = 1)
  
  ## Load data for team
  team_df = games_df[games_df$winner_name == team_name |
                       games_df$loser_name == team_name]
  
  ## Get data by team rather than by game
  team_df$outcome = 'win'
  team_df$outcome[team_df$loser_name == team_name] = 'lose'
  
  team_df$avgShiftLen = team_df$winner_avgShiftLen
  team_df$avgShiftLen[team_df$outcome == 'lose'] =
    team_df$loser_avgShiftLen[team_df$outcome == 'lose']
  
  ## Aggregate seasons by win and lose
  by_season = team_df %>% 
    group_by(season,avgShiftLen,outcome) %>% 
    summarise('count' = n())
  
  by_season = na.exclude(dcast(by_season,
                               season + avgShiftLen ~ outcome))
  by_season$count = by_season$lose + by_season$win
  by_season$win_rate = by_season$win / (by_season$win + by_season$lose)
  by_season = by_season[by_season$count > 5,]

  ## Aggregate all seasons by win and lose
  all_seasons = team_df %>% group_by(avgShiftLen,outcome) %>% summarise('count' = n())
  all_seasons = dcast(all_seasons,avgShiftLen ~ outcome)
  all_seasons$win_rate = all_seasons$win / (all_seasons$win + all_seasons$lose)
  all_seasons = na.exclude(all_seasons)
  all_seasons$win_rate = as.numeric(all_seasons$win_rate)
  
  #Create Plots for Multiplot
  p1 = ggplot() + 
    geom_col(data = by_season[by_season$season == 20122013,],
             aes(x = avgShiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') + 
    ggtitle('2012-2013 Season') + theme_minimal(base_size = 14) +
    xlim(c(41,50)) + ylim(0,1) + xlab('Mean of Mean Player Shift Duration') + 
    ylab('Win Rate ')

  p2 = ggplot() + 
    geom_col(data = by_season[by_season$season == 20132014,],
                           aes(x = avgShiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') + 
    ggtitle('2013-2014 Season') + theme_minimal(base_size = 14) +
    xlim(c(41,50)) + ylim(0,1) + xlab('Mean of Mean Player Shift Duration') + 
    ylab('Win Rate ')
  
  p3 = ggplot() +
    geom_col(data = by_season[by_season$season == 20142015,],
             aes(x = avgShiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') + 
    ggtitle('2014-2015 Season') + theme_minimal(base_size = 14) +
    xlim(c(41,50))  + ylim(0,1) + xlab('Mean of Mean Player Shift Duration') + 
    ylab('Win Rate ')
  
  p4 = ggplot() + 
    geom_col(data = by_season[by_season$season == 20152016,],
             aes(x = avgShiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') + 
    ggtitle('2015-2016 Season') + theme_minimal(base_size = 14) +
    xlim(c(41,50)) + ylim(0,1) + xlab('Mean of Mean Player Shift Duration') + 
    ylab('Win Rate ')
  
  p5 = ggplot() +
    geom_col(data = by_season[by_season$season == 20162017,],
             aes(x = avgShiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') + 
    ggtitle('2016-2017 Season') + theme_minimal(base_size = 14) +
    xlim(c(41,50)) + ylim(0,1) + xlab('Mean of Mean Player Shift Duration') + 
    ylab('Win Rate ')
  
  p6 = ggplot() +
    geom_col(data = by_season[by_season$season == 20172018,],
             aes(x = avgShiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4')+ 
    ggtitle('2017-2018 Season') + theme_minimal(base_size = 14) +
    xlim(c(41,50)) + ylim(0,1) + xlab('Mean of Mean Player Shift Duration') + 
    ylab('Win Rate ')
  
  
  gridExtra::grid.arrange(p1,p2,p3,p4,p5,p6,ncol= 1)
}


team_avg_iceTime <- function(team_name){
  #Load all Data
  games_df = fread('app_data/upd_game_df.csv',drop = 1)
  
  ## Load data for team
  team_df = games_df[games_df$winner_name == team_name |
                       games_df$loser_name == team_name]
  
  ## Get data by team rather than by game
  team_df$outcome = 'win'
  team_df$outcome[team_df$loser_name == team_name] = 'lose'
  
  team_df$avgIceTime = team_df$winner_avgIceTime
  team_df$avgIceTime[team_df$outcome == 'lose'] =
    team_df$loser_avgIceTime[team_df$outcome == 'lose']
  
  team_df$bin = cut(team_df$avgIceTime, 
                    breaks=c(960,965,970,975,980,985,
                             990,995,1000), 
                    labels=c(960,965,970,975,980,985,
                             990,995)
                    )
  team_df$bin = unfactor(team_df$bin)

  ## Aggregate seasons by win and lose
  by_season = team_df %>% 
    group_by(season,bin,outcome) %>% 
    summarise('count' = n())
  
  by_season = na.exclude(dcast(by_season,
                               season + bin ~ outcome))
  by_season$count = by_season$lose + by_season$win
  by_season$win_rate = by_season$win / (by_season$win + by_season$lose)
                  
  ## Aggregate all seasons by win and lose
  all_seasons = team_df %>% group_by(bin,outcome) %>% summarise('count' = n())
  all_seasons = dcast(all_seasons,bin ~ outcome)
  all_seasons$win_rate = all_seasons$win / (all_seasons$win + all_seasons$lose)
  all_seasons = na.exclude(all_seasons)
  all_seasons$win_rate = as.numeric(all_seasons$win_rate)
  
  #Create Plots for Multiplot
  p1 = ggplot() + 
    geom_col(data = by_season[by_season$season == 20122013,],
             aes(x = bin,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = bin,y = win_rate),color = 'firebrick4') +
    ggtitle('2012-2013 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p2 = ggplot() + 
    geom_col(data = by_season[by_season$season == 20132014,],
             aes(x = bin,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = bin,y = win_rate),color = 'firebrick4') + 
    ggtitle('2013-2014 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p3 = ggplot() +
    geom_col(data = by_season[by_season$season == 20142015,],
             aes(x = bin,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = bin,y = win_rate),color = 'firebrick4') + 
    ggtitle('2014-2015 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p4 = ggplot() + 
    geom_col(data = by_season[by_season$season == 20152016,],
             aes(x = bin,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = bin,y = win_rate),color = 'firebrick4') + 
    ggtitle('2015-2016 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p5 = ggplot() +
    geom_col(data = by_season[by_season$season == 20162017,],
             aes(x = bin,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = bin,y = win_rate),color = 'firebrick4') + 
    ggtitle('2016-2017 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ')
  
  p6 = ggplot() +
    geom_col(data = by_season[by_season$season == 20172018,],
             aes(x = bin,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = bin,y = win_rate),color = 'firebrick4')+ 
    ggtitle('2017-2018 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  

  gridExtra::grid.arrange(p1,p2,p3,p4,p5,p6,ncol= 1)
}

league_avg_shift <- function(){
  #Load all Data
  team_df = fread('app_data/upd_game_df.csv',drop = 1)
  
  #Get Output for Each Season
  season_output = data.frame(season = integer(),win_cnt = integer(),loss_cnt = integer(),shiftLen = integer())
  for(shiftLen in list(41,42,43,44,45,46,47,48,49,50)){
    win_cnt = team_df[team_df$winner_avgShiftLen == shiftLen,] %>% 
      group_by(season) %>% summarise(n())
    
    loss_cnt = team_df[team_df$loser_avgShiftLen == shiftLen] %>% 
      group_by(season) %>% summarise(n())
    
    output = merge(win_cnt,loss_cnt,by = 'season')
    colnames(output) = c('season','win_cnt','loss_cnt')
    output$shiftLen = shiftLen
    season_output = rbind(season_output,output)
  }
  
  season_output$win_rate = season_output$win_cnt / (season_output$win_cnt + season_output$loss_cnt)
  
  #Aggregate for all seasons
  win_cnt = team_df %>%
    group_by(winner_avgShiftLen) %>% 
    summarise(n())
  colnames(win_cnt) = c('avgShiftLen','win')
  
  loss_cnt = team_df %>%
    group_by(loser_avgShiftLen) %>% 
    summarise(n())  
  colnames(loss_cnt) = c('avgShiftLen','loss')
  
  all_seasons = merge(win_cnt,loss_cnt,by = 'avgShiftLen')
  all_seasons$win_rate = all_seasons$win / (all_seasons$win + all_seasons$loss)
  
  
  #Create Plots for Multiplot
  p1 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20122013,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2012-2013 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  p2 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20132014,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2013-2014 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p3 = ggplot() +
    geom_col(data = season_output[season_output$season == 20142015,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2014-2015 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  p4 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20152016,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2015-2016 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  p5 = ggplot() +
    geom_col(data = season_output[season_output$season == 20162017,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2016-2017 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') +  
    ylab('Win Rate ')
  
  p6 = ggplot() +
    geom_col(data = season_output[season_output$season == 20172018,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2017-2018 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  
  gridExtra::grid.arrange(p1,p2,p3,p4,p5,p6,ncol= 1)
}

league_avg_shift_played <- function(){
  #Load all Data
  team_df = fread('app_data/upd_game_df.csv',drop = 1)
  
  #Get Output for Each Season
  season_output = data.frame(season = integer(),win_cnt = integer(),loss_cnt = integer(),shiftLen = integer())
  for(shiftLen in list(41,42,43,44,45,46,47,48,49,50)){
    win_cnt = team_df[team_df$winner_avgShiftLen == shiftLen,] %>% 
      group_by(season) %>% summarise(n())
    
    loss_cnt = team_df[team_df$loser_avgShiftLen == shiftLen] %>% 
      group_by(season) %>% summarise(n())
    
    output = merge(win_cnt,loss_cnt,by = 'season')
    colnames(output) = c('season','win_cnt','loss_cnt')
    output$shiftLen = shiftLen
    season_output = rbind(season_output,output)
  }
  
  season_output$win_rate = season_output$win_cnt / (season_output$win_cnt + season_output$loss_cnt)
  season_output$played = season_output$win_cnt + season_output$loss_cnt
  #Aggregate for all seasons
  win_cnt = team_df %>%
    group_by(winner_avgShiftLen) %>% 
    summarise(n())
  colnames(win_cnt) = c('avgShiftLen','win')
  
  loss_cnt = team_df %>%
    group_by(loser_avgShiftLen) %>% 
    summarise(n())  
  colnames(loss_cnt) = c('avgShiftLen','loss')
  
  all_seasons = merge(win_cnt,loss_cnt,by = 'avgShiftLen')
  all_seasons$win_rate = all_seasons$win / (all_seasons$win + all_seasons$loss)
  all_seasons$played = all_seasons$win_cnt + all_seasons$loss_cnt
  
  
  #Create Plots for Multiplot
  p1 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20122013,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2012-2013 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  p2 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20132014,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2013-2014 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p3 = ggplot() +
    geom_col(data = season_output[season_output$season == 20142015,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2014-2015 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  p4 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20152016,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2015-2016 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  p5 = ggplot() +
    geom_col(data = season_output[season_output$season == 20162017,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2016-2017 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') +  
    ylab('Win Rate ')
  
  p6 = ggplot() +
    geom_col(data = season_output[season_output$season == 20172018,],
             aes(x = shiftLen,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgShiftLen,y = win_rate),color = 'firebrick4') +
    ggtitle('2017-2018 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(41,50) + 
    xlab('Mean Player Shift Duration') + 
    ylab('Win Rate ') 
  
  
  gridExtra::grid.arrange(p1,p2,p3,p4,p5,p6,ncol= 1)
}


league_avg_iceTime <- function(){
  #Load all Data
  team_df = fread('app_data/upd_game_df.csv',drop = 1)
  
  ## Get data by team rather than by game
  team_df$winner_avgIceTime = cut(team_df$winner_avgIceTime, 
                                  breaks=c(960,965,970,975,980,985,
                                           990,995,1000), 
                                  labels=c(960,965,970,975,980,985,
                                           990,995)
                                  )
  
  team_df$loser_avgIceTime = cut(team_df$loser_avgIceTime, 
                                  breaks=c(960,965,970,975,980,985,
                                           990,995,1000), 
                                  labels=c(960,965,970,975,980,985,
                                           990,995)
                                  )
  
  team_df$loser_avgIceTime = unfactor(team_df$loser_avgIceTime)
  team_df$winner_avgIceTime = unfactor(team_df$winner_avgIceTime)
  
  #Get Output for Each Season
  season_output = data.frame(season = integer(),win_cnt = integer(),loss_cnt = integer(),iceTime = integer())
  for(iceTime in list(960,965,970,975,980,985,990,995)){
    win_cnt = team_df[team_df$winner_avgIceTime == iceTime,] %>% 
      group_by(season) %>% summarise(n())
    
    loss_cnt = team_df[team_df$loser_avgIceTime == iceTime] %>% 
      group_by(season) %>% summarise(n())
    
    output = merge(win_cnt,loss_cnt,by = 'season')
    colnames(output) = c('season','win_cnt','loss_cnt')
    output$iceTime = iceTime
    season_output = rbind(season_output,output)
  }
  season_output$win_rate = season_output$win_cnt / (season_output$win_cnt + season_output$loss_cnt)
  
  #Aggregate for all seasons
  win_cnt = team_df %>%
    group_by(winner_avgIceTime) %>% 
    summarise(n())
  colnames(win_cnt) = c('avgIceTime','win')
  
  loss_cnt = team_df %>%
    group_by(loser_avgIceTime) %>% 
    summarise(n())  
  colnames(loss_cnt) = c('avgIceTime','loss')
  
  all_seasons = merge(win_cnt,loss_cnt,by = 'avgIceTime')
  all_seasons$win_rate = all_seasons$win / (all_seasons$win + all_seasons$loss)
                                                    
  
  #Create Plots for Multiplot
  p1 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20122013,],
             aes(x = iceTime,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgIceTime,y = win_rate),color = 'firebrick4') +
    ggtitle('2012-2013 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p2 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20132014,],
             aes(x = iceTime,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgIceTime,y = win_rate),color = 'firebrick4') +
    ggtitle('2013-2014 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p3 = ggplot() +
    geom_col(data = season_output[season_output$season == 20142015,],
             aes(x = iceTime,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgIceTime,y = win_rate),color = 'firebrick4') +
    ggtitle('2014-2015 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p4 = ggplot() + 
    geom_col(data = season_output[season_output$season == 20152016,],
             aes(x = iceTime,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgIceTime,y = win_rate),color = 'firebrick4') +
    ggtitle('2015-2016 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  p5 = ggplot() +
    geom_col(data = season_output[season_output$season == 20162017,],
             aes(x = iceTime,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgIceTime,y = win_rate),color = 'firebrick4') +
    ggtitle('2016-2017 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ')
  
  p6 = ggplot() +
    geom_col(data = season_output[season_output$season == 20172018,],
             aes(x = iceTime,y = win_rate)) + 
    geom_line(data = all_seasons, aes(x = avgIceTime,y = win_rate),color = 'firebrick4') +
    ggtitle('2017-2018 Season') + theme_minimal(base_size = 14) +
    ylim(0,1) +
    xlim(960,1000) + 
    xlab('Mean Player Ice Time') + 
    ylab('Win Rate ') 
  
  
  gridExtra::grid.arrange(p1,p2,p3,p4,p5,p6,ncol= 1)
}
