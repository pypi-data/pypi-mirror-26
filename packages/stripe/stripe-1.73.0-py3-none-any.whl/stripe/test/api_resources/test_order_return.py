

import stripe
from stripe.test.helper import StripeResourceTest


class OrderReturnTest(StripeResourceTest):

    def test_list_order_returns(self):
        stripe.OrderReturn.list()
        self.requestor_mock.request.assert_called_with(
            'get',
            '/v1/order_returns',
            {}
        )
