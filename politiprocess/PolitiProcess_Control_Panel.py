import sys
sys.path.append('/Users/o19mobile/Politiprocess Dev/Politiprocess2/politiprocess')

from datetime import datetime

from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from Paramerator import Parameters
from Mongo import Connect
from Scraper import Scraper
from Processing import Processing
from Topic_Modeler import Topic_Modeler


ui, base = loadUiType('Politiprocess.ui')

class Control_Panel(base, ui):

    def __init__(self):
        super(Control_Panel, self).__init__()

        self.p = Parameters()

        self.connection = None

        self.setupUi(self)

        self.ParamFileModel = QtWidgets.QFileSystemModel(self.ParamList)
        self.ParamFileModel.setReadOnly(True)
        self.ParamFileModel.removeColumns(1,2)

        root = self.ParamFileModel.setRootPath('save/params')
        self.ParamList.setModel(self.ParamFileModel)
        self.ParamList.setRootIndex(root)

        self.ParamList.clicked.connect(lambda: self.ParamLoadButton.setEnabled(True))
        
        # Connections
        self.ParamLoadButton.clicked.connect(lambda: self.load_params())
        self.ParamTree.itemChanged.connect(lambda: self.update_value())
        self.ConnectButton.clicked.connect(lambda: self.mongo_update())
        self.ScraperLoad.clicked.connect(lambda: self.scraper_config_load())
        self.ScraperDepthSlider.sliderReleased.connect(lambda: self.depth_slider())
        self.UseLocalCheckBox.toggled.connect(lambda: self.use_local_check_box())
        self.UpsertCheckBox.toggled.connect(lambda: self.upsert_check_box())
        self.ScraperButton.clicked.connect(lambda: self.run_scraper())
        self.NewlineCheckBox.toggled.connect(lambda: self.newline_check_box())
        self.PunctuationCheckBox.toggled.connect(lambda: self.puncuation_check_box())
        self.EmailsCheckBox.toggled.connect(lambda: self.emails_check_box())
        self.ContradictionsCheckBox.toggled.connect(lambda: self.contradictions_check_box())
        self.AccentsCheckBox.toggled.connect(lambda: self.accents_check_box())
        self.CurrencyCheckBox.toggled.connect(lambda: self.currency_check_box())
        self.FixUnicodeCheckBox.toggled.connect(lambda: self.unicode_check_box())
        self.LowercaseCheckBox.toggled.connect(lambda: self.lowercase_check_box())
        self.VisualizeButton.clicked.connect(lambda: self.visualizer_start())

    # Functions
    def load_params(self):

        self.ParamTree.clear()

        file = self.ParamFileModel.data(self.ParamList.selectedIndexes()[0])
        
        self.p.loader(f"save/params/{file}", 'params')

        self.ParamTree.setEnabled(True)
        self.ParamLoadedLabel.setText(f"{file}")
        self.ParamTree.setHeaderLabels(['Section', 'Value'])

        for section, value in self.p.params_dict.items():
            # print(key)

            root = QtWidgets.QTreeWidgetItem(self.ParamTree, [section])
            root.setExpanded(True)
            
            for key, val in value.items():
                if isinstance(val, list):
                    item = QtWidgets.QTreeWidgetItem([key])
                    
                    for thing in val:
                        item2 = QtWidgets.QTreeWidgetItem()
                        item2.setData(1,2, str(thing))
                        item2.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                        item.addChild(item2)
                    
                    root.addChild(item)
                    continue

                item = QtWidgets.QTreeWidgetItem([key])
                item.setData(1,2, val)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                root.addChild(item)

    def update_value(self):
        # if self.ParamTree.currentItem().
        value = self.ParamTree.currentItem().data(1,2)
        name = self.ParamTree.currentItem().text(0)
        parent = self.ParamTree.currentItem().parent().text(0)

        self.ParamTree.currentItem().setForeground(1,QtGui.QBrush(QtGui.QColor("red")))

        self.p.params_dict[parent][name] = value

    def mongo_update(self):
        if not self.connection:
            self.connection = Connect()   

        total = self.connection.count()
        red_count = self.connection.collection.count(query={'target': True})
        blue_count = self.connection.collection.count(query={'target': False})
        article_count = self.connection.collection.count(query={'is article': True})
        latest_article = self.connection.collection.find_one(sort=[('date', -1)])['date']
        if self.connection.added_count:
            self.AddedCount.display(self.connection.added_count)

        self.LatestArticleDate.setText(datetime.ctime(latest_article))
        self.ConnectButton.setStyleSheet('background-color: green')
        self.ConnectButton.setText('CONNECTED')

        self.TotalCount.display(total)
        self.RedCount.display(red_count)
        self.BlueCount.display(blue_count)
        self.ArticleCount.display(article_count)

    def scraper_config_load(self):

        self.p.loader(f"dat/scraper.cfg", 'scraper')
        
        self.ScraperDepthSlider.setEnabled(True)
        self.ScraperDepthNumber.setEnabled(True)
        self.UseLocalCheckBox.setEnabled(True)
        self.UpsertCheckBox.setEnabled(True)
        self.ScraperButton.setEnabled(True)
        self.ScraperLists.setEnabled(True)
        self.NewlineCheckBox.setEnabled(True)
        self.PunctuationCheckBox.setEnabled(True)
        self.EmailsCheckBox.setEnabled(True)
        self.ContradictionsCheckBox.setEnabled(True)
        self.AccentsCheckBox.setEnabled(True)
        self.CurrencyCheckBox.setEnabled(True)
        self.FixUnicodeCheckBox.setEnabled(True)
        self.LowercaseCheckBox.setEnabled(True)


        self.ScraperDepthSlider.setValue(self.p.scraper_dict['Reddit_Params']['Scraper_Depth_Limit'])
        self.UseLocalCheckBox.setChecked(self.p.scraper_dict['Options']['Set_Local'])
        self.UpsertCheckBox.setChecked(self.p.scraper_dict['Options']['Upsert'])
        
        self.NewlineCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['Remove_Newline'])
        self.PunctuationCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['Remove_Punctuation'])
        self.EmailsCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['Remove_Emails'])
        self.ContradictionsCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['Remove_Contradictions'])
        self.AccentsCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['Remove_Accents'])
        self.CurrencyCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['Replace_Currency'])
        self.FixUnicodeCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['Fix_Unicode'])
        self.LowercaseCheckBox.setChecked(self.p.scraper_dict['Pre_Processing']['All_Lowercase'])

        self.scraper_lists()


    def depth_slider(self):

        self.p.scraper_dict['Reddit_Params']['Scraper_Depth_Limit'] = self.ScraperDepthSlider.value()

    def use_local_check_box(self):
        if self.UseLocalCheckBox.checkState() == 2:
            self.p.scraper_dict['Options']['Set_Local'] = True
        else:
            self.p.scraper_dict['Options']['Set_Local'] = False

    def upsert_check_box(self):
        if self.UseLocalCheckBox.checkState() == 2:
            self.p.scraper_dict['Options']['Set_Local'] = True
        else:
            self.p.scraper_dict['Options']['Set_Local'] = False

    def newline_check_box(self):
        if self.NewlineCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['Remove_Newline'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['Remove_Newline'] == False

    def puncuation_check_box(self):
        if self.PunctuationCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['Remove_Punctuation'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['Remove_Punctuation'] == False

    def emails_check_box(self):
        if self.EmailsCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['Remove_Emails'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['Remove_Emails'] == False

    def contradictions_check_box(self):
        if self.ContradictionsCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['Remove_Contradictions'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['Remove_Contradictions'] == False

    def accents_check_box(self):
        if self.AccentsCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['Remove_Accents'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['Remove_Accents'] == False

    def currency_check_box(self):
        if self.CurrencyCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['Replace_Currency'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['Replace_Currency'] == False

    def unicode_check_box(self):
        if self.FixUnicodeCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['Fix_Unicode'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['Fix_Unicode'] == False

    def lowercase_check_box(self):
        if self.LowercaseCheckBox.checkState() == 2:
            self.p.scraper_dict['Pre_Processing']['All_Lowercase'] == True
        else:
            self.p.scraper_dict['Pre_Processing']['All_Lowercase'] == False

    def scraper_lists(self):

        self.ScraperLists.clear()
        
        for x in self.p.scraper_dict:
            for section, value in self.p.scraper_dict[x].items():
                if isinstance(value, list):
                    root = QtWidgets.QTreeWidgetItem(self.ScraperLists, [section])
                    root.setExpanded(False)
                    
                    for thing in value:
                        item = QtWidgets.QTreeWidgetItem()
                        item.setData(1,2, str(thing))
                        root.addChild(item)

    def run_scraper(self):
        self.p.linker(self.p.scraper_dict, 'scraper')
        
        scraper = Scraper(self.p.scraper)
        processing = Processing(self.p.scraper)

        scraper.run()

        self.ProgressBar.setValue(25)

        processing.pre_processor(scraper.scraper_df) 

        self.ProgressBar.setValue(50)

        processing.spacy_processor(scraper.scraper_df)

        self.ProgressBar.setValue(75)

        self.connection = Connect(settings=None, mongo_cfg=self.p.scraper)
        self.connection.update_from_df(scraper.scraper_df)

        self.mongo_update()

        self.ProgressBar.setValue(100)

        # self.AddedCount.

    def visualizer_start(self):
        self.p.linker(self.p.params_dict, 'params')
        
        self.connection.settings = self.p.params
        self.connection.query()

        if self.connection.settings.Query.Red_Blue_or_All == 'All':
            red_topics = Topic_Modeler(self.connection.red_df, self.p.params)
            red_topics.topic_modeler()
            red_topics.visualizer()

            image1 = QtGui.QPixmap(red_topics.save)
            image1 = image1.scaledToWidth(600, QtCore.Qt.SmoothTransformation)
            self.RedPlotView.resize(600, image1.height())
            self.RedPlotView.setPixmap(image1)
            
            blue_topics = Topic_Modeler(self.connection.blue_df, self.p.params)
            blue_topics.topic_modeler()
            blue_topics.visualizer()

            image2 = QtGui.QPixmap(blue_topics.save)
            image2 = image2.scaledToWidth(600, QtCore.Qt.SmoothTransformation)
            self.BluePlotView.resize(600, image2.height())
            self.BluePlotView.setPixmap(image2)




app = QtWidgets.QApplication(sys.argv)
c = Control_Panel()
c.show()
sys.exit(app.exec_())