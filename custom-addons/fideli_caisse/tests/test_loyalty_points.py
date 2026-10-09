from odoo.tests.common import TransactionCase


class TestLoyaltyPoints(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Client Test Fidélité',
        })
        self.member = self.env['loyalty.member'].create({
            'partner_id': self.partner.id,
        })

    def test_code_carte_genere_automatiquement(self):
        """Un membre créé doit avoir un code carte généré automatiquement."""
        self.assertTrue(self.member.code_carte)
        self.assertEqual(len(self.member.code_carte), 8)

    def test_solde_initial_a_zero(self):
        """Un nouveau membre doit démarrer avec un solde de 0 point."""
        self.assertEqual(self.member.solde_points, 0)
        self.assertEqual(self.member.niveau, 'bronze')

    def test_points_attribues_sur_transaction(self):
        """Créer une transaction de type 'gain' doit augmenter le solde."""
        self.env['loyalty.transaction'].create({
            'member_id': self.member.id,
            'type': 'gain',
            'points': 15,
        })
        self.assertEqual(self.member.solde_points, 15)

    def test_niveau_passe_a_argent(self):
        """Le niveau doit passer à Argent à partir de 200 points."""
        self.env['loyalty.transaction'].create({
            'member_id': self.member.id,
            'type': 'gain',
            'points': 250,
        })
        self.assertEqual(self.member.niveau, 'argent')

    def test_utilisation_diminue_le_solde(self):
        """Une transaction de type 'utilisation' doit diminuer le solde."""
        self.env['loyalty.transaction'].create({
            'member_id': self.member.id,
            'type': 'gain',
            'points': 100,
        })
        self.env['loyalty.transaction'].create({
            'member_id': self.member.id,
            'type': 'utilisation',
            'points': 30,
        })
        self.assertEqual(self.member.solde_points, 70)