from sources.python_weekly import PythonWeekly

if __name__ == '__main__':
    issues = [1, 2, 3, 4, 5]
    for i in issues:
        print('******************************')
        p = PythonWeekly(issue_number=i)

        for column in p.issue.columns:
            print(column.title)
            print(column.description)
            print('----------------------------------')
