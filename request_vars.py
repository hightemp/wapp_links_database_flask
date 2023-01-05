

class RequestVars:
    aGroupFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
    }

    aCategoryFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'group': {
            'name': 'Группа',
            'type': 'select',
            'field_name': 'group',
            'list': [],
            'value': '',
            'sel_value': '',
        },
    }

    aLinkFields = {
        'title': {
            'name': 'Заголовок',
            'type': 'title',
            'field_name': 'name',
            'value': '',
        },
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'category': {
            'name': 'Категория',
            'type': 'select',
            'field_name': 'category',
            'list': [],
            'value': '',
            'sel_value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'a_url': {
            'name': 'url',
            'type': 'url',
            'field_name': 'a_url',
            'value': '',
        },
        'a_desc': {
            'name': 'Описание',
            'type': 'textarea',
            'field_name': 'a_desc',
            'value': '',
        },
    }

    aClasses = {
        'group': 'Group',
        'category': 'Category',
        'link': 'Link',
    }

    sBaseURL = ''

    oArgs = []
    oArgsLists = []

    sSelectGroup = ''
    sSelectCategory = ''
    sSelectLink = ''

    sGroupFilter = ''
    sCategoryFilter = ''
    sLinkFilter = ''

    aListAllGroups = []
    aListAllCategories = []

    oListAllGroups = []
    oListAllCategories = []

    aFields=[]
    aGroups=[]
    aLinks=[]

    oLinks=[]

    aLinkFieldsList=[]
    aOpenedCategories = []
    aCategories = []

    dFormsFieldsList=[]

    sGroupFilter = ''
    sCategoryFilter = ''
    sLinkFilter = ''

    sFilterName = ''
    sFilterUrl = ''
    
    aForGroupCategories = []
    aForCategoryLinks = []

class SessionVars:
    sSelectProject = ""
    sSelectGroup = ""
    sSelectTask = ""
    sSelectFile = ""