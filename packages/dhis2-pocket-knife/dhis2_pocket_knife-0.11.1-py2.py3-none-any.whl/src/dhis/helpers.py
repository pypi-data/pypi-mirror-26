d = {
    'userGroups': ['usergroups', 'ug', 'usergroup'],
    'sqlViews': ['sqlviews', 'sqlview'],
    'constants': ['constants', 'constant'],
    'optionSets': ['optionsets', 'os'],
    'optionGroups': ['optiongroups', 'optiongroup'],
    'optionGroupSets': ['optiongroupsets', 'optiongroupset'],
    'legendSets': ['legendsets', 'legendset'],
    'organisationUnitGroups': ['organisationunitgroups', 'oug', 'orgunitgroups', 'ougroups', 'orgunitgroup', 'ougroup'],
    'organisationUnitGroupSets': ['organisationunitgroupsets', 'ougs', 'orgunitgroupsets', 'ougroupsets',
                                  'orgunitgroupset', 'ougroupset'],
    'categoryOptions': ['categoryoptions', 'catoptions', 'catoption', 'categoryoption'],
    'categoryOptionGroups': ['categoryoptiongroups', 'catoptiongroups', 'catoptiongroup', 'categoryoptiongroup'],
    'categoryOptionGroupSets': ['categoryoptiongroupsets', 'catoptiongroupsets', 'catoptiongroupset',
                                'categoryoptiongroupset'],
    'categories': ['categories', 'cat', 'cats' 'category'],
    'categoryCombos': ['categorycombos', 'catcombos', 'catcombo', 'categorycombo', 'categorycombination',
                       'categorycombinations'],
    'dataElements': ['dataelements', 'de', 'des', 'dataelement'],
    'dataElementGroups': ['dataelementgroups', 'deg', 'degroups', 'degroup', 'dataelementgroup'],
    'dataElementGroupSets': ['dataelementgroupsets', 'degs', 'degroupsets', 'degroupset', 'dataelementgroupset'],
    'indicators': ['indicators', 'i', 'ind', 'indicator'],
    'indicatorGroups': ['indicatorgroups', 'ig', 'indgroups', 'indicatorgroup'],
    'indicatorGroupSets': ['indicatorgroupsets', 'igs', 'indgroupsets', 'indicatorgroupset'],
    'dataSets': ['datasets', 'ds', 'dataset'],
    'dataApprovalLevels': ['dataapprovallevels', 'datasetapprovallevel'],
    'validationRules': ['validationrules', 'validationrule'],
    'validationRuleGroups': ['validationrulegroups', 'validationrulegroup'],
    'interpretations': ['interpretations', 'interpretation'],
    'trackedEntityAttributes': ['trackedentityattributes', 'trackedentityattribute', 'tea', 'teas'],
    'programs': ['programs', 'program'],
    'eventCharts': ['eventcharts', 'eventchart'],
    'eventReports': ['eventreports', 'eventtables', 'eventreport'],
    'programIndicators': ['programindicators', 'pi', 'programindicator'],
    'maps': ['maps', 'map'],
    'documents': ['documents', 'document'],
    'reports': ['reports', 'report'],
    'charts': ['charts', 'chart', 'datavisualization', 'datavisualizations', 'datavizualisation', 'datavizualizations'],
    'reportTables': ['pivottable', 'pivottables', 'reporttables', 'reporttable'],
    'dashboards': ['dashboards', 'dashboard']
}


def object_types():
    """Reverse dictionary from  key:list  to  each_listitem: key and sort it"""
    return dict((v, k) for k in d for v in d[k])


properties_to_remove = {
    'created',
    'user',
    'lastUpdated',
    'publicAccess',
    'userGroupAccesses',
    'userAccesses',
    'href',
    'url'
}

csv_import_objects = {
    'dataElements',
    'dataElementGroups',
    'categoryOptions',
    'categoryOptionGroups',
    'organisationUnits',
    'organisationUnitGroups',
    'validationRules',
    'translations',
    'optionSets'
}
