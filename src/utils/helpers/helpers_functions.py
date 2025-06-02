import logging
import sys
from os import environ
from datetime import datetime
from pytz import timezone
import logging
import sys

class HelperFunctions:
    """
        Esta classe agrupa as funções de funções auxiliares.
    """

    logger = None

    @staticmethod
    def get_time(time_zone: str = 'America/Sao_Paulo'):

        """
            Retorna a hora atual pra timezone
        """

        try:
            return datetime.now().astimezone(timezone(time_zone))
        except Exception as error:
            pass
    
    @staticmethod
    def timetz(*args):
        """
            Retorna a hora atual para o fuso horário fornecido default='America/Sao_Paulo'

        Returns:
            datetime: fuso horário atual
        """
        tz = timezone('America/Sao_Paulo')
        return datetime.now(tz).timetuple()

    @staticmethod
    def get_logger(name: str = "clients-wishlist-api") -> logging.Logger:
        """
        Configura e retorna um logger global com um nome fornecido.

        Args:
            name (str): O nome do registrador a ser exibido nas saídas do console.

        Returns:
            logging.Logger: A instância do logger configurada.
        """
        
        if not HelperFunctions.logger:
            HelperFunctions.logger = logging.getLogger(name)
            
            formatter = logging.Formatter(
                "%(asctime)s — %(name)s — %(funcName)s:%(lineno)d — %(levelname)s — %(message)s"
            )
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            
            HelperFunctions.logger.addHandler(console_handler)
            
            HelperFunctions.logger.setLevel(logging.getLevelName(environ.get("LOG_LEVEL", "INFO")))

        return HelperFunctions.logger