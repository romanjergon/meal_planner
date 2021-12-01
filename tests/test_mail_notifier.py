import mock

from meal_planner.mail_notifier import MailNotifier


@mock.patch("meal_planner.mail_notifier.smtplib.SMTP")
def test_send_notif_mail(mocker):
    def test_send_notif_mail_decorator(mocked_smtp):
        notifier = MailNotifier(
            smtp_host="smtp.gmail.com",
            smtp_port=587,
            notification_mailbox="test@test.te",
            mail_password="string password",
            personal_mailbox="second_test@test.te",
        )

        result = notifier.send_notif_mail(
            "This is testing mail for mail notifier class", "Lorem Ipsum"
        )
        assert (
            len(result) == 0
        ), "should be zero as no recipient should be rejected by the server"

        mocked_method = mocked_smtp.return_value.__enter__.return_value.sendmail
        mocked_method.assert_called_once()
