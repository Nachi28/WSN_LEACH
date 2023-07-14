import wsn_final as go
import openpyxl
import pandas as pd

# go.run(200)


def to_excel(data):
    workbook = openpyxl.load_workbook("WSN\hi.xlsx")
    # Load an existing file
    worksheet = workbook['Sheet1']
    worksheet.append(data)
    workbook.save('WSN\hi.xlsx')


to_excel(["No. of Nodes", "Total rounds", "PDR", "EtoE_Delay"])

for i in range(100, 500, 25):
    print("///////////")
    print(f"For nodes => {i}")
    go.run(i)
