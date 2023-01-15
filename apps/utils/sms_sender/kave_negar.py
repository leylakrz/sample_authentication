import logging

import kavenegar

from prj.settings import KAVENEGAR_APIKEY, KAVENEGAR_TEMPLATE, KAVENEGAR_TEMPLATE_LOGIN, KAVENEGAR_PHONE_SENDER

from apps.utils.sms_sender import SmsSender

logger = logging.getLogger(__name__)


class KaveNegar(SmsSender):
    kave_negar = kavenegar.KavenegarAPI(KAVENEGAR_APIKEY)

    def send_login_sms(self, code: str, number: str, hash_str: str = '') -> None:
        self.send_sms(template=KAVENEGAR_TEMPLATE_LOGIN,
                      code=code, receptor_number=number, hash_str=hash_str)

    def send_signup_sms(self, code: str, number: str, hash_str: str = '') -> None:
        self.send_sms(template=KAVENEGAR_TEMPLATE,
                      code=code, receptor_number=number, hash_str=hash_str)

    def send_sms(self, template, code, receptor_number, hash_str):
        try:
            r = self.kave_negar.verify_lookup(
                self.set_kavenegar_args(template=template, code=code, receptor_number=receptor_number,
                                        hash_str=hash_str))[0]
            return True
        except Exception as e:
            logging.error(e)
            return False

    def set_kavenegar_args(self, template: str, receptor_number: str, code: str, hash_str: str):
        return {
            'receptor': receptor_number,
            'template': template,
            'token': code,
            'token2': hash_str,
            'type': 'sms',
            'sender': KAVENEGAR_PHONE_SENDER
        }

    def send_custom_sms(self, number: str, text_message: str) -> bool:
        try:
            self.kave_negar.sms_send(params={'receptor': number,'message': text_message, })
            return True
        except (kavenegar.HTTPException, kavenegar.APIException) as error:
            logger.error(f'{type(error)}: {str(error)}')
            return False

