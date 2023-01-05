import os
from peewee import *
from playhouse.flask_utils import PaginatedQuery
import datetime
from baselib import *

UPLOAD_PATH_REL = "static/uploads"
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), UPLOAD_PATH_REL)
DATABASE = './wapp_Links_flask.database.db'

__DEMO__ = True

if (__DEMO__):
    os.unlink(DATABASE)

bFirstStart = not os.path.exists(DATABASE)
db = SqliteDatabase(DATABASE)
lClasses = []

# Link: Модели
class Group(Model):
    name = CharField()

    class Meta:
        database = db
lClasses.append(Group)

class Category(Model):
    name = CharField()
    group = ForeignKeyField(Group, backref='categories')
    parent = ForeignKeyField('self', backref='children', null=True)

    class Meta:
        database = db
lClasses.append(Category)

class Link(Model):
    name = CharField()
    category = ForeignKeyField(Category, backref='Links')
    created_at = DateField(default=datetime.datetime.now)
    updated_at = DateField(default=datetime.datetime.now)
    a_url = CharField(default="")
    a_desc = TextField(default="")

    class Meta:
        database = db
lClasses.append(Link)

class ModelsWrapper():
    oR = {}

    def __init__(self, oR) -> None:
        self.oR = oR

    def fmUpdateFromFields(self, sName):
        Klass = globals()[self.oR.aClasses[sName]]
        self.oR.aFields = getattr(self.oR, 'a'+self.oR.aClasses[sName]+'Fields', '')
        oF = {}
        for sK, oV in self.oR.aFields.items():
            sFK = 'field-'+str(sName)+'-'+str(sK)
            try:
                oF[sK] = self.oR.oArgs[sFK]
            except:
                pass
        if 'id' in oF:
            sID = oF['id']
            del oF['id']
            Klass.update(oF).where(Klass.id==sID).execute()
        else:
            Klass.create(**oF).save()        

    def fmDeleteByArgsList(self, sName):
        Klass = globals()[self.oR.aClasses[sName]]
        for sID in self.oR.oArgsLists[sName]:
            Klass.delete().where(Klass.id == sID).execute()


    def fnGetAllGroup(self):
        return Group.select().where(Group.name ** f"%{self.oR.sGroupFilter}%")

    def fnGetCategoryForCurrentGroup(self):
        return Category.select().where(Category.group==self.oR.sSelectGroup,Category.id==self.oR.sSelectCategory)

    def fnGetLinkForCurrentCategory(self):
        return Link.select().where(Link.category==self.oR.sSelectCategory,Link.id==self.oR.sSelectLink)

    def fnGetAllGroups(self):
        return Group.select()

    def fnGetAllCategories(self):
        return Category.select()

    def fnGetAllGroupsWithFilter(self):
        return Group.select().where(Group.name ** f"%{self.oR.sGroupFilter}%")

    def fnGetAllCategoryiesWithFilter(self):
        return Category.select().where(Category.name ** f"%{self.oR.sCategoryFilter}%")

    def fnGetAllLinksForCategory(self):
        return Link.select().where(Link.category==self.oR.sSelectCategory, Link.name ** f"%{self.oR.sFilterName}%", Link.a_url ** f"%{self.oR.sFilterUrl}%")

    def fnGetAllLinksForCategoryPagination(self):
        self.oR.oLinks = self.fnGetAllLinksForCategory()
        return PaginatedQuery(self.oR.oLinks, 20, 'page-link')

    def fnGetAllLinks(self):
        return Link.select()

    def fnGetAllLinksPagination(self):
        self.oR.oLinks = self.fnGetAllLinks()
        return PaginatedQuery(self.oR.oLinks, 20)

    def fnCountLinks(self, sCategoryID):
        return Link.select().where(Link.category == sCategoryID).count()

    def fnGetCategories(self, iGroupID, sCategoryFilter):
        if str(iGroupID)=="-1":
            aQueryCategories = Category.select().where(Category.name ** f"%{sCategoryFilter}%", Category.parent == None)
        else: 
            aQueryCategories = Category.select().where(Category.name ** f"%{sCategoryFilter}%", Category.parent == None, Category.group == iGroupID)
        return aQueryCategories

db.connect()

# Link: DEMO
if (bFirstStart):
    db.create_tables(lClasses)

    if (__DEMO__):
        group01 = Group.create(name='Разное')
        group02 = Group.create(name='Гос сервисы')
        group03 = Group.create(name='Почта')
        group04 = Group.create(name='Интернет-магазины')

        category01 = Category.create(name="google", group=group01)

        category0101 = Category.create(name="gmail", group=group01, parent=category01.id)
        category0102 = Category.create(name="api", group=group01, parent=category01.id)

        category0103 = Category.create(name="secret 1", group=group01, parent=category0101.id)
        category0103 = Category.create(name="secret 2", group=group01, parent=category0101.id)

        category0103 = Category.create(name="secret 3", group=group01, parent=category0102.id)
        category0103 = Category.create(name="secret 4", group=group01, parent=category0102.id)

        category02 = Category.create(name="yandex", group=group03)
        category03 = Category.create(name="yandex", group=group04)

        for iI in range(0, 100):
            Link.create(name=f"google {iI}", category=category01, a_url="http://ya.ru", a_desc=f"<h1>test {iI}</h1>")
        


        