def timeCalculate (elapsed_time:float):
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    current_time = f"{hours:02}:{minutes:02}:{seconds:02}"

    return  current_time