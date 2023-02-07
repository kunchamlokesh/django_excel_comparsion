from django.shortcuts import render
import pandas as pd

def compare_excel(request):
    if request.method == 'POST':
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        if file1 and file2:
            df1 = pd.read_excel(file1)
            df2 = pd.read_excel(file2)

            # Ensure both DataFrames have the same columns
            columns = df1.columns
            df2 = df2.reindex(columns=columns, fill_value=None)

            # Perform the comparison
            differences = (df1 != df2) & ~(df1.isna() & df2.isna())

            # Color the differences
            highlighted = differences.style.applymap(
                lambda x: "background-color: yellow" if x else ""
            )
            highlighted = highlighted.applymap(
                lambda x: "background-color: red" if pd.isna(x) else ""
            )

            context = {'old_data': df1.to_html(), 'new_data': df2.to_html(), 'differences': highlighted.render()}
            return render(request, 'compare.html', context)

    return render(request, 'compare.html')

