from flask import g, Flask, request, send_file, redirect, session, jsonify
import os
import re
from werkzeug.utils import secure_filename

from flask import Response
from jinja2 import Template, FunctionLoader, Environment, BaseLoader
from flask import Flask
import mimetypes
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict
import zipfile
from flask_caching import Cache
from request_vars import *
from baselib import *
from database import *

# NOTE: Константы
APP_NAME=__name__

# NOTE: Переменные
app = Flask(APP_NAME)
config = {
    # "DEBUG": True,          # some Flask specific configs
    # "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

@cache.cached(timeout=500)
def fnIterCategories(oMW, iGroupID, aOpened, sCategoryFilter, aCategories=[], iLevel=0):
    if (iLevel==0):
        aQueryCategories = []

        aQueryCategories = oMW.fnGetCategories(iGroupID, sCategoryFilter)

        return fnIterCategories(oMW, iGroupID, aOpened, sCategoryFilter, aQueryCategories, 1)
    else:
        aNewCategories = []
        for oCategory in aCategories:
            sID = oCategory.id

            aQueryCategories = oMW.fnGetCategories(iGroupID, sCategoryFilter)
            
            aIterCategories = []
            if (sID in aOpened) and aQueryCategories and len(aQueryCategories)>0:
                aIterCategories = fnIterCategories(oMW, iGroupID, aOpened, sCategoryFilter, aQueryCategories, iLevel+1)
            
            iCnt = oMW.fnCountLinks(sID)

            oNewCategory = {}
            oNewCategory['id'] = oCategory.id
            oNewCategory['name'] = oCategory.name
            oNewCategory['level'] = (iLevel - 1) * "<span class='tree-spacer'></span>" + oNewCategory['name']
            oNewCategory['cnt'] = iCnt

            aNewCategories += [oNewCategory] + aIterCategories
        
        return aNewCategories

@app.route("/zip/static/<path:path>", methods=['GET', 'POST'])
def zip_static(path):
    oR = Response(readfile("static/"+path), mimetype=mimetypes.guess_type(path)[0])
    oR.headers['Cache-Control'] = 'max-age=60480000, stale-if-error=8640000, must-revalidate'
    return oR

@app.route("/", methods=['GET', 'POST'])
@cache.cached()
def index():
    oR = RequestVars()
    oR.sBaseURL = request.url

    fnPrepareArgs(oR)

    oMW = ModelsWrapper(oR)
    
    # session.update('sSelGroup','sSelLink')
    if (oR.sSelectGroup!="-1"):
        oR.aForGroupCategories = oMW.fnGetCategoryForCurrentGroup()
        if len(oR.aForGroupCategories)==0 and oR.sSelectCategory!="-1":
            oR.sSelectCategory = ''
    if (oR.sSelectCategory!="-1"):
        oR.aForCategoryLinks = oMW.fnGetLinkForCurrentCategory()
        if len(oR.aForCategoryLinks)==0 and oR.sSelectLink!="-1":
            oR.sSelectLink = ''

    # NOTE: Формы
    if f'cancel' in oR.oArgs:
        return redirect("/")
    for sName in ['group', 'category', 'link']:
        if f'search-clean-{sName}' in oR.oArgs:
            oR.oArgs[f'search-{sName}'] = ''
            setattr(oR, 's'+oR.aClasses[sName]+'Filter', '')
        if f'search-{sName}' in oR.oArgs:
            setattr(oR, 's'+oR.aClasses[sName]+'Filter', oR.oArgs[f'search-{sName}'])
        if f'accept-remove-{sName}' in oR.oArgs:
            oMW.fmDeleteByArgsList(sName)
            del oR.oArgs[f'accept-remove-{sName}']
            break
        if f'remove-{sName}' in oR.oArgs:
            return render_template(f'{sName}/alert_delete.html', aFields=oR.oArgs)        

        if f'save-{sName}' in oR.oArgs:
            oMW.fmUpdateFromFields(sName)
            del oR.oArgs[f'save-{sName}']
            if f'edit-{sName}' in oR.oArgs:
                del oR.oArgs[f'edit-{sName}']
            break
        if f'clean-{sName}' in oR.oArgs:
            break
        
    # FIXME: Дубль кода
    oR.oListAllGroups = oMW.fnGetAllGroups()
    oR.oListAllCategories = oMW.fnGetAllCategories()
    oR.aListAllGroups = []
    oR.aListAllCategories = []
    for oI in oR.oListAllGroups:
        oR.aListAllGroups += [oI]
    for oI in oR.oListAllCategories:
        oR.aListAllCategories += [oI]
    
    oR.aLinkFields['category']['list'] = oMW.fnGetAllCategories()
    oR.aLinkFields['category']['sel_value'] = oR.sSelectCategory

    if ((f'edit-category' in oR.oArgs) or (f'create-category' in oR.oArgs)):
        oR.aCategoryFields['group']['list'] = oMW.fnGetAllGroups()
        oR.aCategoryFields['group']['sel_value'] = oR.sSelectGroup
    if ((f'edit-link' in oR.oArgs) or (f'create-link' in oR.oArgs)):
        if (f'edit-link' in oR.oArgs):
            oR.dFormsFieldsList = fnPrepareFormFields(oR.aLinkFields, Link, oR.sSelectLink)
            # NOTE: Link - edit
            return render_template(f'link/edit.html',oR=oR)
        elif (f'create-Link' in oR.oArgs):
            oR.dFormsFieldsList = fnPrepareFormFields(oR.aLinkFields, Link, 0)
            # NOTE: Link - create
            return render_template(f'link/create.html', oR=oR)
    if f'create-group' in oR.oArgs:
        oR.dFormsFieldsList = {}
        oR.dFormsFieldsList = fnPrepareFormFields(oR.aGroupFields, Group, 0)
        return render_template(f'group/create.html',oR=oR)
    if f'create-category' in oR.oArgs:
        oR.dFormsFieldsList = {}
        oR.dFormsFieldsList = fnPrepareFormFields(oR.aCategoryFields, Category, 0)
        # NOTE: Group, Category - create
        return render_template(f'category/create.html',oR=oR)
    if f'edit-group' in oR.oArgs:
        oR.dFormsFieldsList = {}
        oR.dFormsFieldsList = fnPrepareFormFields(oR.aGroupFields, Group, oR.sSelectGroup)
        return render_template(f'group/edit.html',oR=oR)            
    if f'edit-category' in oR.oArgs:
        oR.dFormsFieldsList = {}
        oR.dFormsFieldsList = fnPrepareFormFields(oR.aCategoryFields, Category, oR.sSelectCategory)
        # NOTE: Group, Category - edit
        return render_template(f'category/edit.html',oR=oR)

    oR.oListAllGroups = oMW.fnGetAllGroupsWithFilter()
    oR.oListAllCategories = oMW.fnGetAllCategoryiesWithFilter()
    oR.aListAllGroups = []
    oR.aListAllCategories = []
    for oI in oR.oListAllGroups:
        oR.aListAllGroups += [oI]
    for oI in oR.oListAllCategories:
        oR.aListAllCategories += [oI]

    # NOTE: Группы
    oR.aGroups = [{'id':-1,'name':'Все','short':1}] + oR.aListAllGroups

    oR.aOpenedCategories = []
    if 'category' in oR.oArgsLists:
        oR.aOpenedCategories = oR.oArgsLists["category"]
    
    oR.aCategories = fnIterCategories(oMW, oR.sSelectGroup, oR.aOpenedCategories, oR.sCategoryFilter)
    oR.aCategories.insert(0, {'id':-1,'name':'Все','level':'Все','short':1})

    oR.aLinks=[]
    oR.aLinkFieldsList = []
    if oR.sSelectCategory != '':
        # oR.aLinks = oMW.fnGetAllLinksForCategory()
        oR.aLinks = oMW.fnGetAllLinksForCategoryPagination()

        # aLinkFields['group']['list'] = oR.aListAllGroups
        oR.aLinkFields['category']['list'] = oR.aListAllCategories
        oR.aLinkFieldsList = fnPrepareFormFields(oR.aLinkFields, Link, oR.sSelectLink)

    return render_template(
        'index.html', 
        oR=oR
    )

@app.route("/as_table", methods=['GET', 'POST'])
@cache.cached()
def as_table():
    oR = RequestVars()

    oMW = ModelsWrapper(oR)

    oR.oLinks = oMW.fnGetAllLinksPagination()

    return render_template(
        'table.html', 
        oR=oR
    )

def run():
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    run()