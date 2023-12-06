from progress.bar import *
import logging, csv
sys.path.insert(1, '../')
from compare import choose
from parser4 import find_next_update
from stage2 import get_stage2_link
from exceptions import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

FORMAT = "%(asctime)s %(funcName)s %(levelname)s %(message)s"

handler = logging.FileHandler(f"logs/manipulator.log", mode='w') 
formatter = logging.Formatter(FORMAT)

handler.setFormatter(formatter)
logger.addHandler(handler)


with open('svod.csv') as file:
    reader = csv.DictReader(file)
    bar = ChargingBar("Done: ", max=2800)
    request_counter = 0
    succes_counter = 1
    untracked = 0
    update_ids = set()
    data = dict()

    for row in reader:
        request_counter += 1
        logger.debug("-------NEW ROW-------")
        try:
            link = choose(row['CVE'], row['OS'], row['PO'])
            logger.debug(f'   {link}')
            update_id = get_stage2_link(link)
            logger.debug(f'   {update_id}')
            update_id = find_next_update(update_id)
            logger.debug(f'   {update_id}')
            update_ids.add(update_id)

        except IndexError:
            logger.error("FIND NEXT UPDATE ERROR")

        except EmptyTableError:
            logger.warning("EMPTY TABLE ERROR")

        except NoLinkFoundError:
            logger.warning("NO LINK FOUND ERROR")

        except NoMatchingLink:
            logger.warning("NO MATCHING LINK ERROR")

        except NoStage2DataError:
            logger.error("NO STAGE 2 DATA ERROR")
        
        except:
            logger.critical("UNTRACKED ERROR")
            untracked += 1

        else:
            logger.debug("succes")
            succes_counter += 1
            if update_id not in data.keys():
                data[update_id] = []

            if f"{row['OS']} {row['PO']}" not in data[update_id]:
                data[update_id].append(f"{row['OS']} {row['PO']}")
                logger.info(f"pair: {row['OS']} {row['PO']} : {update_id}")

        bar.next()
        logger.info(f'    ids found: {succes_counter} unique ids: {len(list(update_ids))} compressed: {len(list(update_ids)) / (succes_counter) * 100} %')
        logger.info(f'    untracked errors: {untracked}, iteration: {request_counter}')

    print(data)
