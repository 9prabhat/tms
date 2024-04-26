import unittest
from app import app, db, Plan

class TestAddPlanAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:tms.db:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_plan(self):
        # Make a POST request to add a new plan
        response = self.app.post('/add_plan', json={
            'name': 'Silver',
            'cost': 199,
            'validity': 90,
            'status': 'Active'
        })

        # Check if the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Check if the plan was added to the database
        new_plan = Plan.query.filter_by(name='Silver').first()
        self.assertIsNotNone(new_plan)
        self.assertEqual(new_plan.cost, 199)
        self.assertEqual(new_plan.validity, 90)
        self.assertEqual(new_plan.status, 'Active')

if __name__ == '__main__':
    unittest.main()
