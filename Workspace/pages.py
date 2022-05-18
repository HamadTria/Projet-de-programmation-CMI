def homepage(html):
    return [html.Div(className="banner",
        children=[
            html.Div(className="navbar",
            children=[
                html.Img(className="logo"),
                html.Ul(children=[
                    html.Li(children=[
                        html.A('Visualisations', href='https://qa.ostack.cn/qa/?qa=496065/', className="container")
                    ]),
                    html.Li(children=[
                        html.A('Data', className="container")
                    ])
                ])
            ]),
            html.Div(className="text-content",
            children=[
                html.H1('Croissance des arbres d’un ensemble de site dans les Pyrénées'),
                html.Div(className="box",
                children=[
                    html.Div(className="left",
                    children=[
                        html.H2('a'),
                        html.Hr(),
                        html.P()
                    ]),
                    html.Div(className="middle",
                    children=[
                        html.H2('a'),
                        html.Hr(),
                        html.P('''Flexbugs : une liste, maintenue par la communauté, des différents bugs des navigateurs relatifs aux boîtes flexibles et les éventuelles méthodes de contournements associées
                                Mixins multi-navigateurs pour flexbox : cet article fournit un ensemble de mixins pour obtenir l'effet des flexbox de façon homogène sur les différents navigateurs qui ne supportent pas la syntaxe moderne pour les boîtes flexibles''')
                    ]),
                    html.Div(className="right",
                    children=[
                        html.H2('a'),
                        html.Hr(),
                        html.P()
                    ])
                ])
            ])
        ])]