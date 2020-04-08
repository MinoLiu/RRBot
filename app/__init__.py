import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[
                        logging.FileHandler('robot.log', 'w', 'utf-8'),
                        logging.StreamHandler()
                    ])

LOG = logging.getLogger(__name__)
