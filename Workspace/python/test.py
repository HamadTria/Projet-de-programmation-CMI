''' --------------------->>> NE PAS SUPPRIMER !!!!!!!!!!!!!
def figure(con):
    df = pd.read_sql('SELECT oneacorn, Year FROM harvest;', con)
    df = df.groupby(by=['Year'])['oneacorn'].agg(['max', 'min', ('mean oneacorn', 'mean')])
    df['max'] = df['max'] - df['mean oneacorn']
    df['min'] = df['mean oneacorn'] - df['min']
    fig = px.scatter(df, x=df.index, y="mean oneacorn", error_y="max", error_y_minus="min", animation_frame=df.index, range_x=[2010,2021], range_y=[-1,7])
    return fig

def real_figure(con):
    df = pd.read_sql('SELECT oneacorn, Year FROM harvest;', con)
    df = df.groupby(by=['Year'])['oneacorn'].agg(['max', 'min', ('mean oneacorn', 'mean')])
    df['max'] = df['max'] - df['mean oneacorn']
    df['min'] = df['mean oneacorn'] - df['min']

    fig = go.Figure(
        data=[go.Scatter(x = [-1], y = [-1], line=dict(width=1.5))],
        layout = go.Layout(
            xaxis = dict(range=[2010,2021], autorange=False, zeroline=False, title='Year'),
            yaxis = dict(range=[-1,7], autorange=False, zeroline=False, title='Mean oneacorn'),
            title_text = "OMG!", hovermode="closest",

            updatemenus = [
                dict(
                    type="buttons",
                    active=0,
                    buttons=[
                        dict(label="Animation", method="animate", 
                        args=[None, {'frame':{'duration':40}, 'transition':{'duration':0}, 'fromcurrent':True, 'execute':True}])])]),
                        
        frames = [
            go.Frame(
                data = [go.Scatter(
                    x = (df.index).tolist()[:k] if k != 0 else [(df.index).tolist()[k]],
                    y = df['mean oneacorn'].iloc[:k] if k != 0 else [df['mean oneacorn'].iloc[k]],
                    error_y = dict(
                        type = 'data',
                        symmetric = False,
                        array = df['max'].iloc[:k] if k != 0 else [df['max'].iloc[k]],
                        arrayminus = df['min'].iloc[:k] if k != 0 else [df['min'].iloc[k]]
                    ))]) for k in range(len(df['mean oneacorn'])+1)]
    )
    return fig
'''