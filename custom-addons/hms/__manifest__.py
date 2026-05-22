# __manifest__.py
{
    "name": "HMS",
    "version": "1.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/patient_views.xml",
    ],
    "installable": True,
}