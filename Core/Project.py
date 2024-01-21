from .FileIO import readYaml,ScanDire
from .Library import Library
from .Code_Formatter import format_code
from .Resource import Resource
from .Templates_Manager import TemplateManager
from .Debug import Log
import os

class Project:
    def __init__(self,path):
        envpath = os.path.dirname(os.path.dirname(__file__))
        Log(f'[Project] Loading basic resources')
        self.resources = Resource()
        self.resources.loadResources(f'{envpath}\\Resources','')
        Log(f'[Project] Start to import pack {path}')
        data = readYaml(path)
        self.version = data['version']
        Log(f'[Project] Pack version: {self.version}')
        self.base_path = os.path.dirname(path)
        self.base_library = Library(readYaml(f"{self.base_path}\\Libraries\\library.yml"))
        self.resources.loadResources(f'{self.base_path}\\Resources','')
        self.pages = {}
        self.TemplateManager = TemplateManager(self.resources)
        for pair in ScanDire(f'{self.base_path}\\Pages',r'.*\.yml$'):
            print(pair)
            page = pair[0]
            self.pages.update({ page['name']:page })
            for alias in page['alias']:
                self.pages.update({ alias:page })
        Log(f'[Project] Loaded pack completely!')
    
    def get_page_xaml(self,page_alias):
        if page_alias not in self.pages.keys():
            # TODO PAGE NOT FOUND EXCEPTION
            pass
        xaml = ''
        for card_ref in self.pages[page_alias]['cards']:
            card = self.base_library.getCard(card_ref)
            card_xaml = self.TemplateManager.build(card)
            card_xaml = format_code(card_xaml,card,self.scripts)
            xaml += card_xaml
        return xaml