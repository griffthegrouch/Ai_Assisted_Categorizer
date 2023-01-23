import xlsxwriter

def save_results(categorized_games):
    workbook = xlsxwriter.Workbook('game_categories.xlsx')
    for category in categorized_games:
        worksheet = workbook.add_worksheet(category)
        row = 0
        col = 0
        for game in categorized_games[category]:
            worksheet.write(row, col, game)
            row += 1
    workbook.close()
