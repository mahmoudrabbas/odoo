{
    "name": "HMS",
    "version": "1.0",
    "author": "Mahmoud",
    "license": "LGPL-3",

    "depends": ["base", "contacts", "sale", "purchase"],

    "data": [
        "security/ir.model.access.csv",

        "views/department_views.xml",
        "views/doctor_views.xml",
        "views/patient_views.xml",
        "views/res_partner_views.xml",
    ],

    "installable": True,
}