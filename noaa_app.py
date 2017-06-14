from spyre import server

import pandas as pd
import matplotlib.pyplot as plt

class noaaApp(server.App):
    title = 'Лабораторная работа №2'

    inputs = [{'type': 'dropdown',
               'label': 'Индекс',
               'options': [{'label': 'VCI', 'value': 'VCI'},
                           {'label': 'TCI', 'value': 'TCI'},
                           {'label': 'VHI', 'value': 'VHI'},],
               'key': 'index',
               'action_id': 'update_data'},

              {'type': 'dropdown',
               'label': 'Область',
               'options': [{'label': 'Винница', 'value': '01'},
                           {'label': 'Волынь', 'value': '02'},
                           {'label': 'Днепр', 'value': '03'},
                           {'label': 'Донецк', 'value': '04'},
                           {'label': 'Житомир', 'value': '05'},
                           {'label': 'Закарпатье', 'value': '06'},
                           {'label': 'Запорожье', 'value': '07'},
                           {'label': 'Ивано-Франковск', 'value': '08'},
                           {'label': 'Киев', 'value': '09'},
                           {'label': 'Кировоград', 'value': '10'},
                           {'label': 'Луганск', 'value': '11'},
                           {'label': 'Львов', 'value': '12'},
                           {'label': 'Николаев', 'value': '13'},
                           {'label': 'Одесса', 'value': '14'},
                           {'label': 'Полтава', 'value': '15'},
                           {'label': 'Ровно', 'value': '16'},
                           {'label': 'Сумы', 'value': '17'},
                           {'label': 'Тернополь', 'value': '18'},
                           {'label': 'Харьков', 'value': '19'},
                           {'label': 'Херсон', 'value': '20'},
                           {'label': 'Хмельницкий', 'value': '21'},
                           {'label': 'Черкасы', 'value': '22'},
                           {'label': 'Черновцы', 'value': '23'},
                           {'label': 'Чернигов', 'value': '24'},
                           {'label': 'Республика Крым', 'value': '25'},
                           {'label': 'Киев (город)', 'value': '26'},
                           {'label': 'Севастополь', 'value': '27'}],
               'key': 'region',
               'action_id': 'update_data'},

              {'input_type': 'text',
               'variable_name': 'year',
               'label': 'Год',
               'value': 1981,
               'key': 'year',
               'action_id': 'update_data'},

              {'type':'slider',
               'label': 'Первая неделя',
               'min': 1, 'max': 52, 'value': 1,
               'key': 'first',
               'action_id': 'update_data'},

              {'type': 'slider',
               'label': 'Последняя неделя',
               'min': 1, 'max': 52, 'value': 52,
               'key': 'last',
               'action_id': 'update_data'},

              {'type': 'slider',
               'label': 'Процент площади',
               'min': 0, 'max': 100, 'value': 50,
               'key': 'percent',
               'action_id': 'update_data'},

              {'type': 'slider',
               'label': 'Минимум VHI',
               'min': 0, 'max' :100, 'value': 0,
               'key': 'minimum',
                'action_id': 'update_data'},

              {'type': 'slider',
               'label': 'Максимум VHI',
               'min': 0, 'max': 100, 'value': 100,
               'key': 'maximum',
               'action_id': 'update_data'},]

    controls = [{'type': 'hidden',
                 'id': 'update_data'}]

    tabs = ['Описание', 'Индекс', 'Экстремумы', 'Засухи', 'График']

    outputs = [{'type': 'plot',
                'id': 'plot',
                'control_id': 'update_data',
                'tab': 'График'},
               {'type': 'table',
                'id': 'table',
                'control_id': 'update_data',
                'tab': 'Индекс'},
               {'type': 'html',
                'id': 'drought',
                'control_id': 'update_data',
                'tab': 'Засухи'},
               {'type': 'table',
                'id': 'table1',
                'control_id': 'update_data',
                'tab': 'Экстремумы'},
               {'type': 'html',
                'id': 'HTML_id',
                'tab': 'Описание'},]

    def table(self, params):
        index = params['index']
        region = params['region']
        year = params['year']
        first = params['first']
        last = params['last']

        path = 'C:/Users/Vova/clean/2016_04_09-11h_vhi_id_{}.csv'.\
            format(region)

        df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'SMN', 'SMT',
                            'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
        df1 = df[(df['year'] == float(year)) & (df['week'] >= float(first)) &
                                           (df['week'] <= float(last))]
        df1 = df1[['week', index]]
        return df1

    def getPlot(self, params):
        index = params['index']
        year = params['year']
        first = params['first']
        last = params['last']
        df = self.table(params).set_index('week')
        plt_obj = df.plot(figsize=[15, 10])
        plt_obj.set_ylabel(index)
        plt_obj.set_title('Index {index} for {year} from {first} to {last}'\
                          'weeks'.format(index=index, year=float(year),
                          first=float(first), last=float(last)))
        fig = plt_obj.get_figure()
        return fig

    def drought(self, params):
        region = params['region']
        minimum = params['minimum']
        maximum = params['maximum']
        percent = params['percent']

        path = 'C:/Users/Vova/clean/2016_04_09-11h_vhi_id_{}.csv'.\
                format(region)
        df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'SMN', 'SMT',
                            'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
        df1 = df[(df['VHI'] < int(maximum)) & (df['VHI'] > int(minimum)) &
                                              (df['VHI<15'] > int(percent))]
        df1 = df1[['year', 'VHI', 'VHI<15']]
        return 'Годы экстремальных засух на {percent}% площади области:'\
               '{years}'.format(percent=int(percent),
                                years=pd.unique(df1.year.ravel()))

    def table1(self, params):
        index = params['index']
        region = params['region']
        year = params['year']

        path = 'C:/Users/Vova/clean/2016_04_09-11h_vhi_id_{}.csv'.\
                format(region)

        df = pd.read_csv(path, index_col=False, header=9,
                       names=['year', 'week', 'SMN', 'SMT',
                              'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
        return df.loc[pd.concat((df.groupby(['year'])['VHI'].idxmax(),
                                 df.groupby(['year'])['VHI'].idxmin()))]

    def HTML_id(self, params):
        return "<h1>Наука про данные: обмен результатами и предварительный"\
"анализ</h1><p style='margin: 20px; font-size: 20px'><b>Цель работы:</b>"\
"ознакомиться с системой контроля версий GitHub, научиться создавать простые"\
"вебприложения<br>для обмена результатами исследований с использованием"\
"модуля spyre<br><br><a href='https://github.com'>Ссылка</a> на созданный"\
"репозиторий.</p><br>"

app = noaaApp()
app.launch()
