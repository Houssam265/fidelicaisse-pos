{
    'name': 'FideliCaisse',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Programme de fidélité intégré au Point de Vente',
    'description': """
        Module de fidélité client pour commerces de détail.
        Points cumulés automatiquement à chaque vente POS,
        récompenses au-delà d'un seuil, consultation du solde
        via un contrôleur web natif.
    """,
    'author': 'Houssam',
    'depends': ['base', 'point_of_sale', 'web'],
    'data': [
        'security/fideli_security.xml',
        'security/ir.model.access.csv',
        'views/loyalty_member_views.xml',
        'views/fideli_menus.xml',
        'views/fideli_public_page.xml',
        'reports/fideli_receipt_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}