class TestAlert:
    def test_create_message(self, alert):
        message = alert.create_message('from@email.com', 'to@email.com', 50)
        expected = 'Subject: [Hawkeye] {0} Alert\nFrom: Hawkeye <{1}>\nTo: Hisham <{2}>\nYour {3} utilization has passed the {4} configured limit. It has reached {5}\n\n\rHappy monitoring!\n\rHawkeye '.format(alert.type, 'from@email.com', 'to@email.com', alert.type, alert.limit, 50)
        assert message == expected
