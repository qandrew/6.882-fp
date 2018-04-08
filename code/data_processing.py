# Returns a dictionary of reaction times S_j^x keyed by user id
# S_j^x = T_j^x - T_P(j)^x is the time of the user's tweet minus its parent

def generate_reaction_times(tweet_df):
  reaction_times = {}
  for index, row in tweet_df.iterrows():
    # if index > 0: # ignore root tweet
      reaction_time = row['Time'] - tweet_df.at[row['ParentDfIndex'],'Time']
      reaction_times[row['UserId']] = reaction_time
      tweet_df.loc[index,"ReactionTime"] = reaction_time
  return reaction_times

# modifies the dataframe to include M_j^x
# M_j^x for tweet x and user j is the number of j's followers who retweet x

def generate_number_of_follower_who_retweet(tweet_df):
    number_of_follower_who_retweet = {}
    
    for index, row in tweet_df.iterrows():
        parent_user_id = tweet_df.at[row['ParentDfIndex'], 'UserId']
        if parent_user_id not in number_of_follower_who_retweet:
            number_of_follower_who_retweet[parent_user_id] =1
        else:
            number_of_follower_who_retweet[parent_user_id] += 1
    
    # add to dataFrame
    for index, row in tweet_df.iterrows():
        if row['UserId'] in number_of_follower_who_retweet:
            count = number_of_follower_who_retweet[row['UserId']]
            tweet_df.loc[index,"FollowersRetweeted"] = count
        else: 
            tweet_df.loc[index,"FollowersRetweeted"] = 0

    return number_of_follower_who_retweet