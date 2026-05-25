{
    "name": "HMS",
    "version": "1.0",
    "author": "Mahmoud",
    "license": "LGPL-3",

    "depends": ["base", "contacts", "sale", "purchase"],

    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/record_rules.xml",

        "views/department_views.xml",
        "views/doctor_views.xml",
        "views/patient_views.xml",
        "views/res_partner_views.xml",

        "reports/patient_report.xml",
    ],

    "installable": True,
}