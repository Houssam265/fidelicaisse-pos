from odoo.tests.common import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestFideliController(HttpCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Client Page Publique'})
        self.member = self.env['loyalty.member'].create({'partner_id': self.partner.id})
        self.env['loyalty.transaction'].create({
            'member_id': self.member.id,
            'type': 'gain',
            'points': 42,
        })

    def test_page_publique_affiche_le_solde(self):
        res = self.url_open('/fidelicaisse/carte?code=%s' % self.member.code_carte)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Client Page Publique', res.text)
        self.assertIn('42', res.text)

    def test_page_publique_code_inconnu(self):
        res = self.url_open('/fidelicaisse/carte?code=ZZZZZZZZ')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Carte introuvable', res.text)

    def test_page_publique_sans_code(self):
        res = self.url_open('/fidelicaisse/carte')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('Carte introuvable', res.text)