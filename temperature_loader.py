def get_season_from_month(month):
    if month in (1, 2 , 12):
        return "Summer"
    if month in (3, 4, 5):
        return "Autumn"
    if month in (6, 7, 8):
        return "Winter"
    if month in (9, 10, 11):
        return "Spring"
    
print(get_season_from_month(1)) # Output: Summer
print(get_season_from_month(4)) # Output: Autumn
print(get_season_from_month(7)) # Output: Winter
print(get_season_from_month(9)) # Output: Spring