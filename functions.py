def get_crr(innings_runs, over, ball):
  total_balls = (over * 6) + ball
  if total_balls > 0:
    crr = (innings_runs / total_balls) * 6
    return round(crr,2)
  else:
    return 0.0
  

def get_rrr(runs_left, ball_left):
    if ball_left > 0:
        rrr= (runs_left/ ball_left)*6
        return round(rrr,2)
    else:
        return runs_left
    

def wicket_left(wickets):
    left= 10 - wickets
    return left


def get_balls(over, ball):
    total_balls = ((over - 1) * 6) + ball
    return (120 - total_balls)